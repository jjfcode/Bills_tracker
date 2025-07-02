#!/usr/bin/env python3
"""
Test suite for Data Integrity Checker.
Tests data consistency verification and repair capabilities.
"""

import os
import sqlite3
import tempfile
import shutil
from datetime import datetime, timedelta
import sys
import unittest

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from integrity_checker import DataIntegrityChecker
from validation import DataValidator

class TestDataIntegrityChecker(unittest.TestCase):
    """Test cases for DataIntegrityChecker."""
    
    def setUp(self):
        """Set up test database."""
        # Create temporary database file
        self.temp_dir = tempfile.mkdtemp()
        self.db_file = os.path.join(self.temp_dir, 'test_bills_tracker.db')
        
        # Create test database
        self.create_test_database()
        
        # Initialize integrity checker
        self.checker = DataIntegrityChecker(self.db_file)
    
    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def create_test_database(self):
        """Create a test database with some data."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Create bills table
        cursor.execute('''
            CREATE TABLE bills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                due_date TEXT NOT NULL,
                billing_cycle TEXT DEFAULT 'monthly',
                reminder_days INTEGER DEFAULT 7,
                web_page TEXT,
                login_info TEXT,
                password TEXT,
                paid INTEGER DEFAULT 0,
                company_email TEXT,
                support_phone TEXT,
                billing_phone TEXT,
                customer_service_hours TEXT,
                account_number TEXT,
                reference_id TEXT,
                support_chat_url TEXT,
                mobile_app TEXT
            )
        ''')
        
        # Create templates table
        cursor.execute('''
            CREATE TABLE templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                due_date TEXT,
                billing_cycle TEXT DEFAULT 'monthly',
                reminder_days INTEGER DEFAULT 7,
                web_page TEXT,
                login_info TEXT,
                password TEXT,
                company_email TEXT,
                support_phone TEXT,
                billing_phone TEXT,
                customer_service_hours TEXT,
                account_number TEXT,
                reference_id TEXT,
                support_chat_url TEXT,
                mobile_app TEXT
            )
        ''')
        
        # Insert valid test data
        cursor.execute('''
            INSERT INTO bills (name, due_date, billing_cycle, reminder_days, web_page, company_email)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('Test Bill 1', '2024-12-31', 'monthly', 7, 'https://example.com', 'test@example.com'))
        
        cursor.execute('''
            INSERT INTO bills (name, due_date, billing_cycle, reminder_days, web_page, company_email)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('Test Bill 2', '2024-11-15', 'quarterly', 14, 'https://test.com', 'billing@test.com'))
        
        cursor.execute('''
            INSERT INTO templates (name, billing_cycle, reminder_days, web_page, company_email)
            VALUES (?, ?, ?, ?, ?)
        ''', ('Test Template 1', 'monthly', 7, 'https://template.com', 'template@example.com'))
        
        conn.commit()
        conn.close()
    
    def test_check_database_integrity_healthy(self):
        """Test integrity check on healthy database."""
        is_healthy, issues = self.checker.check_database_integrity()
        
        self.assertTrue(is_healthy)
        self.assertEqual(len(issues), 0)
        self.assertEqual(self.checker.stats['bills_checked'], 2)
        self.assertEqual(self.checker.stats['templates_checked'], 1)
        self.assertEqual(self.checker.stats['issues_found'], 0)
    
    def test_check_database_structure(self):
        """Test database structure validation."""
        # This should pass with our test database
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Check if required tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        self.assertIn('bills', tables)
        self.assertIn('templates', tables)
        
        # Check bills table structure
        cursor.execute("PRAGMA table_info(bills)")
        bills_columns = {row[1] for row in cursor.fetchall()}
        required_columns = {
            'id', 'name', 'due_date', 'billing_cycle', 'reminder_days',
            'web_page', 'login_info', 'password', 'paid', 'company_email',
            'support_phone', 'billing_phone', 'customer_service_hours',
            'account_number', 'reference_id', 'support_chat_url', 'mobile_app'
        }
        
        missing_columns = required_columns - bills_columns
        self.assertEqual(len(missing_columns), 0, f"Missing columns: {missing_columns}")
        
        conn.close()
    
    def test_invalid_billing_cycle_detection(self):
        """Test detection of invalid billing cycles."""
        # Add a bill with invalid billing cycle
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO bills (name, due_date, billing_cycle, reminder_days)
            VALUES (?, ?, ?, ?)
        ''', ('Invalid Cycle Bill', '2024-12-31', 'invalid-cycle', 7))
        
        conn.commit()
        conn.close()
        
        # Run integrity check
        is_healthy, issues = self.checker.check_database_integrity()
        
        self.assertFalse(is_healthy)
        self.assertGreater(len(issues), 0)
        
        # Check if invalid billing cycle issue is detected
        invalid_cycle_issues = [issue for issue in issues if 'Invalid billing cycle' in issue]
        self.assertGreater(len(invalid_cycle_issues), 0)
    
    def test_invalid_reminder_days_detection(self):
        """Test detection of invalid reminder days."""
        # Add a bill with invalid reminder days
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO bills (name, due_date, billing_cycle, reminder_days)
            VALUES (?, ?, ?, ?)
        ''', ('Invalid Reminder Bill', '2024-12-31', 'monthly', 400))
        
        conn.commit()
        conn.close()
        
        # Run integrity check
        is_healthy, issues = self.checker.check_database_integrity()
        
        self.assertFalse(is_healthy)
        
        # Check if invalid reminder days issue is detected
        invalid_reminder_issues = [issue for issue in issues if 'Invalid reminder days' in issue]
        self.assertGreater(len(invalid_reminder_issues), 0)
    
    def test_missing_required_fields_detection(self):
        """Test detection of missing required fields."""
        # Add a bill with missing due date (name is required by DB constraint)
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO bills (name, billing_cycle, reminder_days)
            VALUES (?, ?, ?)
        ''', ('Missing Date Bill', 'monthly', 7))
        
        conn.commit()
        conn.close()
        
        # Run integrity check
        is_healthy, issues = self.checker.check_database_integrity()
        
        self.assertFalse(is_healthy)
        
        # Check if missing due date issue is detected
        missing_date_issues = [issue for issue in issues if 'Missing required field' in issue and 'due_date' in issue]
        self.assertGreater(len(missing_date_issues), 0)
    
    def test_repair_issues(self):
        """Test automatic repair functionality."""
        # Add invalid data
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO bills (name, due_date, billing_cycle, reminder_days)
            VALUES (?, ?, ?, ?)
        ''', ('Repair Test Bill', '2024-12-31', 'invalid-cycle', 400))
        
        conn.commit()
        conn.close()
        
        # Run integrity check to identify issues
        is_healthy, issues = self.checker.check_database_integrity()
        self.assertFalse(is_healthy)
        
        # Attempt repairs
        repairs = self.checker.repair_issues(auto_repair=True)
        
        # Check that repairs were made
        self.assertGreater(len(repairs), 0)
        
        # Run integrity check again
        is_healthy, issues = self.checker.check_database_integrity()
        
        # Should be healthy now (or at least fewer issues)
        self.assertLess(len(issues), 2)  # Allow for some remaining issues
    
    def test_duplicate_bill_names_detection(self):
        """Test detection of duplicate bill names."""
        # Add duplicate bill names
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO bills (name, due_date, billing_cycle, reminder_days)
            VALUES (?, ?, ?, ?)
        ''', ('Test Bill 1', '2024-10-15', 'monthly', 7))
        
        conn.commit()
        conn.close()
        
        # Run integrity check
        is_healthy, issues = self.checker.check_database_integrity()
        
        self.assertFalse(is_healthy)
        
        # Check if duplicate names issue is detected
        duplicate_issues = [issue for issue in issues if 'Duplicate bill names' in issue]
        self.assertGreater(len(duplicate_issues), 0)
    
    def test_data_consistency_checks(self):
        """Test data consistency checks."""
        # Add a bill marked as paid but with future due date
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        future_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        cursor.execute('''
            INSERT INTO bills (name, due_date, billing_cycle, reminder_days, paid)
            VALUES (?, ?, ?, ?, ?)
        ''', ('Future Paid Bill', future_date, 'monthly', 7, 1))
        
        conn.commit()
        conn.close()
        
        # Run integrity check
        is_healthy, issues = self.checker.check_database_integrity()
        
        # Check if consistency issue is detected
        consistency_issues = [issue for issue in issues if 'Marked as paid but due date is in the future' in issue]
        self.assertGreater(len(consistency_issues), 0)
    
    def test_get_integrity_report(self):
        """Test integrity report generation."""
        # Run integrity check
        is_healthy, issues = self.checker.check_database_integrity()
        
        # Get report
        report = self.checker.get_integrity_report()
        
        # Check report structure
        self.assertIn('database_file', report)
        self.assertIn('check_timestamp', report)
        self.assertIn('is_healthy', report)
        self.assertIn('total_issues', report)
        self.assertIn('stats', report)
        self.assertIn('issues', report)
        
        # Check report values
        self.assertEqual(report['database_file'], self.db_file)
        self.assertEqual(report['is_healthy'], is_healthy)
        self.assertEqual(report['total_issues'], len(issues))
        self.assertEqual(report['issues'], issues)
    
    def test_nonexistent_database(self):
        """Test behavior with nonexistent database."""
        nonexistent_db = os.path.join(self.temp_dir, 'nonexistent.db')
        checker = DataIntegrityChecker(nonexistent_db)
        
        is_healthy, issues = checker.check_database_integrity()
        
        self.assertFalse(is_healthy)
        self.assertGreater(len(issues), 0)
        
        # Check if database not found issue is detected
        not_found_issues = [issue for issue in issues if 'not found' in issue]
        self.assertGreater(len(not_found_issues), 0)

def run_integrity_checker_tests():
    """Run all integrity checker tests."""
    print("🧪 Running Data Integrity Checker Tests...")
    print("=" * 50)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDataIntegrityChecker)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print("\n❌ Errors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\n✅ All tests passed!")
        return True
    else:
        print("\n❌ Some tests failed!")
        return False

if __name__ == "__main__":
    run_integrity_checker_tests() 