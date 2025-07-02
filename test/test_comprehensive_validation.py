#!/usr/bin/env python3
"""
Comprehensive test suite for the validation module.
Tests all validation functions with various input scenarios.
"""

import sys
import os
import unittest
from datetime import datetime, timedelta

# Add the current directory to the path so we can import validation
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from validation import DataValidator, ValidationError, validate_url, validate_email, validate_future_date, validate_reminder_days

class TestDataValidator(unittest.TestCase):
    """Test cases for DataValidator class."""
    
    def test_validate_bill_name(self):
        """Test bill name validation."""
        # Valid names
        self.assertEqual(DataValidator.validate_bill_name("Netflix"), (True, None))
        self.assertEqual(DataValidator.validate_bill_name("Electric Bill"), (True, None))
        self.assertEqual(DataValidator.validate_bill_name("A" * 100), (True, None))  # Max length
        
        # Invalid names
        self.assertNotEqual(DataValidator.validate_bill_name(""), (True, None))
        self.assertNotEqual(DataValidator.validate_bill_name("   "), (True, None))
        self.assertNotEqual(DataValidator.validate_bill_name("A" * 101), (True, None))  # Too long
        self.assertNotEqual(DataValidator.validate_bill_name("Bill<name>"), (True, None))  # Invalid chars
    
    def test_validate_due_date(self):
        """Test due date validation."""
        today = datetime.now()
        
        # Valid dates
        valid_date = today.strftime('%Y-%m-%d')
        self.assertEqual(DataValidator.validate_due_date(valid_date), (True, None))
        
        future_date = (today + timedelta(days=30)).strftime('%Y-%m-%d')
        self.assertEqual(DataValidator.validate_due_date(future_date), (True, None))
        
        past_date = (today - timedelta(days=30)).strftime('%Y-%m-%d')
        self.assertEqual(DataValidator.validate_due_date(past_date), (True, None))
        
        # Invalid dates
        self.assertNotEqual(DataValidator.validate_due_date(""), (True, None))
        self.assertNotEqual(DataValidator.validate_due_date("invalid-date"), (True, None))
        self.assertNotEqual(DataValidator.validate_due_date("2023-13-01"), (True, None))  # Invalid month
        
        # Too far in past
        too_old = (today - timedelta(days=400)).strftime('%Y-%m-%d')
        self.assertNotEqual(DataValidator.validate_due_date(too_old), (True, None))
        
        # Too far in future
        too_future = (today + timedelta(days=4000)).strftime('%Y-%m-%d')
        self.assertNotEqual(DataValidator.validate_due_date(too_future), (True, None))
    
    def test_validate_billing_cycle(self):
        """Test billing cycle validation."""
        # Valid cycles
        valid_cycles = ["weekly", "bi-weekly", "monthly", "quarterly", "semi-annually", "annually", "one-time"]
        for cycle in valid_cycles:
            self.assertEqual(DataValidator.validate_billing_cycle(cycle), (True, None))
        
        # Invalid cycles
        self.assertNotEqual(DataValidator.validate_billing_cycle(""), (True, None))
        self.assertNotEqual(DataValidator.validate_billing_cycle("invalid"), (True, None))
        # Note: Billing cycle validation is case-insensitive, so "WEEKLY" should be valid
        self.assertEqual(DataValidator.validate_billing_cycle("WEEKLY"), (True, None))  # Case insensitive
    
    def test_validate_reminder_days(self):
        """Test reminder days validation."""
        # Valid days
        for days in [1, 7, 30, 365]:
            self.assertEqual(DataValidator.validate_reminder_days(days), (True, None))
            self.assertEqual(DataValidator.validate_reminder_days(str(days)), (True, None))
        
        # Invalid days
        self.assertNotEqual(DataValidator.validate_reminder_days(0), (True, None))
        self.assertNotEqual(DataValidator.validate_reminder_days(-1), (True, None))
        self.assertNotEqual(DataValidator.validate_reminder_days(366), (True, None))
        self.assertNotEqual(DataValidator.validate_reminder_days("invalid"), (True, None))
    
    def test_validate_url(self):
        """Test URL validation."""
        # Valid URLs
        valid_urls = [
            "https://example.com",
            "http://www.example.com",
            "example.com",  # Should be corrected to https://
            "https://sub.example.com/path?param=value",
            "https://example.co.uk"
        ]
        
        for url in valid_urls:
            is_valid, error_msg, cleaned_url = DataValidator.validate_url(url)
            self.assertTrue(is_valid, f"URL should be valid: {url}")
            self.assertIsNotNone(cleaned_url)
        
        # Invalid URLs
        invalid_urls = [
            "not-a-url",
            "ftp://example.com",  # Unsupported protocol
            "https://",  # Missing domain
            "https://.com",  # Invalid domain
            "https://example",  # Missing TLD
        ]
        
        for url in invalid_urls:
            is_valid, error_msg, cleaned_url = DataValidator.validate_url(url)
            self.assertFalse(is_valid, f"URL should be invalid: {url}")
            self.assertIsNotNone(error_msg)
    
    def test_validate_email(self):
        """Test email validation."""
        # Valid emails
        valid_emails = [
            "user@example.com",
            "user.name@example.com",
            "user+tag@example.com",
            "user@sub.example.com",
            "user@example.co.uk",
            "user123@example.com"
        ]
        
        for email in valid_emails:
            is_valid, error_msg = DataValidator.validate_email(email)
            self.assertTrue(is_valid, f"Email should be valid: {email}")
        
        # Invalid emails
        invalid_emails = [
            "invalid-email",
            "@example.com",
            "user@",
            "user@@example.com",
            "user@.com",
            "user@example",
            "a" * 255 + "@example.com"  # Too long
        ]
        
        for email in invalid_emails:
            is_valid, error_msg = DataValidator.validate_email(email)
            self.assertFalse(is_valid, f"Email should be invalid: {email}")
    
    def test_validate_phone(self):
        """Test phone number validation."""
        # Valid phone numbers
        valid_phones = [
            "1234567890",
            "+1234567890",
            "(123) 456-7890",
            "123-456-7890",
            "123.456.7890",
            "+1 (123) 456-7890"
        ]
        
        for phone in valid_phones:
            is_valid, error_msg = DataValidator.validate_phone(phone)
            self.assertTrue(is_valid, f"Phone should be valid: {phone}")
        
        # Invalid phone numbers
        invalid_phones = [
            "123",  # Too short
            "1234567890123456",  # Too long
            "123-abc-7890",  # Contains letters
            "123<456>7890",  # Contains invalid chars
        ]
        
        for phone in invalid_phones:
            is_valid, error_msg = DataValidator.validate_phone(phone)
            self.assertFalse(is_valid, f"Phone should be invalid: {phone}")
    
    def test_validate_bill_data(self):
        """Test complete bill data validation."""
        # Valid bill data
        valid_bill = {
            'name': 'Test Bill',
            'due_date': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
            'billing_cycle': 'monthly',
            'reminder_days': 7,
            'web_page': 'example.com',
            'login_info': 'testuser',
            'password': 'testpass',
            'company_email': 'support@example.com',
            'support_phone': '123-456-7890',
            'paid': False
        }
        
        is_valid, error_msg, cleaned_data = DataValidator.validate_bill_data(valid_bill)
        self.assertTrue(is_valid, f"Bill data should be valid: {error_msg}")
        self.assertIsNotNone(cleaned_data)
        self.assertEqual(cleaned_data['name'], 'Test Bill')
        
        # Invalid bill data
        invalid_bill = {
            'name': '',  # Empty name
            'due_date': 'invalid-date',
            'billing_cycle': 'invalid-cycle',
            'reminder_days': -1
        }
        
        is_valid, error_msg, cleaned_data = DataValidator.validate_bill_data(invalid_bill)
        self.assertFalse(is_valid)
        self.assertIsNotNone(error_msg)
    
    def test_validate_template_data(self):
        """Test template data validation."""
        # Valid template data
        valid_template = {
            'name': 'Test Template',
            'billing_cycle': 'monthly',
            'reminder_days': 7,
            'web_page': 'example.com',
            'login_info': 'testuser',
            'password': 'testpass',
            'company_email': 'support@example.com'
        }
        
        is_valid, error_msg, cleaned_data = DataValidator.validate_template_data(valid_template)
        self.assertTrue(is_valid, f"Template data should be valid: {error_msg}")
        self.assertIsNotNone(cleaned_data)
        self.assertNotIn('due_date', cleaned_data)  # Should not be in template
        self.assertNotIn('paid', cleaned_data)  # Should not be in template
        
        # Test template with due_date and paid (should be removed)
        template_with_bill_fields = valid_template.copy()
        template_with_bill_fields['due_date'] = '2024-01-01'
        template_with_bill_fields['paid'] = True
        
        is_valid, error_msg, cleaned_data = DataValidator.validate_template_data(template_with_bill_fields)
        self.assertTrue(is_valid, f"Template data should be valid: {error_msg}")
        self.assertNotIn('due_date', cleaned_data)  # Should be removed
        self.assertNotIn('paid', cleaned_data)  # Should be removed

class TestLegacyFunctions(unittest.TestCase):
    """Test legacy validation functions for backward compatibility."""
    
    def test_legacy_validate_url(self):
        """Test legacy URL validation function."""
        # Should return cleaned URL for valid URLs
        self.assertEqual(validate_url("example.com"), "https://example.com")
        self.assertEqual(validate_url("https://example.com"), "https://example.com")
        
        # Should return None for invalid URLs
        self.assertIsNone(validate_url("not-a-url"))
        self.assertIsNone(validate_url("https://"))
    
    def test_legacy_validate_email(self):
        """Test legacy email validation function."""
        # Should return cleaned email for valid emails
        self.assertEqual(validate_email("USER@EXAMPLE.COM"), "user@example.com")
        self.assertEqual(validate_email("user@example.com"), "user@example.com")
        
        # Should return None for invalid emails
        self.assertIsNone(validate_email("invalid-email"))
        self.assertIsNone(validate_email("@example.com"))
    
    def test_legacy_validate_future_date(self):
        """Test legacy future date validation function."""
        today = datetime.now()
        valid_date = (today + timedelta(days=30)).strftime('%Y-%m-%d')
        
        # Should return (True, None) for valid dates
        self.assertEqual(validate_future_date(valid_date), (True, None))
        
        # Should return (False, error_msg) for invalid dates
        self.assertNotEqual(validate_future_date("invalid-date"), (True, None))
    
    def test_legacy_validate_reminder_days(self):
        """Test legacy reminder days validation function."""
        # Should return True for valid days
        self.assertTrue(validate_reminder_days("7"))
        self.assertTrue(validate_reminder_days("30"))
        
        # Should return False for invalid days
        self.assertFalse(validate_reminder_days("-1"))
        self.assertFalse(validate_reminder_days("invalid"))

def run_validation_tests():
    """Run all validation tests and return results."""
    print("🧪 Running Comprehensive Validation Tests")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestDataValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestLegacyFunctions))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("🎉 All validation tests passed!")
        return True
    else:
        print(f"❌ {len(result.failures)} tests failed, {len(result.errors)} tests had errors")
        return False

if __name__ == "__main__":
    success = run_validation_tests()
    sys.exit(0 if success else 1) 