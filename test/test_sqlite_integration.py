#!/usr/bin/env python3
"""
Test script to verify SQLite integration is working correctly.
"""

import sys
import os

# Add the current directory to the path so we can import bills-tracker
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_sqlite_integration():
    """Test that the SQLite integration is working correctly."""
    try:
        # Import the functions we need to test
        import importlib.util
        spec = importlib.util.spec_from_file_location("bills_tracker", "bills-tracker.py")
        bills_tracker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(bills_tracker)
        
        print("🔍 Testing SQLite Integration")
        print("=" * 40)
        
        # Test database initialization
        print("1. Testing database initialization...")
        bills_tracker.initialize_database()
        print("   ✅ Database initialized successfully")
        
        # Test loading bills
        print("2. Testing bill loading...")
        bills_tracker.load_bills()
        print(f"   ✅ Loaded {len(bills_tracker.bills)} bills from database")
        
        # Test loading templates
        print("3. Testing template loading...")
        bills_tracker.load_templates()
        print(f"   ✅ Loaded {len(bills_tracker.bill_templates)} templates from database")
        
        # Test saving bills
        print("4. Testing bill saving...")
        bills_tracker.save_bills()
        print("   ✅ Bills saved to database successfully")
        
        # Test saving templates
        print("5. Testing template saving...")
        bills_tracker.save_templates()
        print("   ✅ Templates saved to database successfully")
        
        # Show sample data
        if bills_tracker.bills:
            print("\n📋 Sample bills from database:")
            for i, bill in enumerate(bills_tracker.bills[:3], 1):
                status = "✓ Paid" if bill.get('paid', False) else "○ Unpaid"
                print(f"   {i}. {bill['name']} - {bill['due_date']} [{status}]")
        
        if bills_tracker.bill_templates:
            print("\n📋 Sample templates from database:")
            for i, template in enumerate(bills_tracker.bill_templates[:3], 1):
                print(f"   {i}. {template['name']} ({template.get('billing_cycle', 'monthly')})")
        
        print("\n🎉 All SQLite integration tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ SQLite integration test failed: {e}")
        return False

def test_database_connection():
    """Test direct database connection."""
    try:
        from db import get_db_connection, initialize_database
        
        print("\n🔍 Testing Direct Database Connection")
        print("-" * 40)
        
        # Initialize database
        initialize_database()
        print("   ✅ Database initialized")
        
        # Test connection
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"   ✅ Found {len(tables)} tables: {[table[0] for table in tables]}")
        
        # Check bill count
        cursor.execute("SELECT COUNT(*) FROM bills")
        bill_count = cursor.fetchone()[0]
        print(f"   ✅ Bills table contains {bill_count} records")
        
        # Check template count
        cursor.execute("SELECT COUNT(*) FROM templates")
        template_count = cursor.fetchone()[0]
        print(f"   ✅ Templates table contains {template_count} records")
        
        conn.close()
        print("   ✅ Database connection closed successfully")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Database connection test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🧪 SQLite Integration Test Suite")
    print("=" * 50)
    
    # Test direct database connection
    db_ok = test_database_connection()
    
    # Test application integration
    app_ok = test_sqlite_integration()
    
    print("\n" + "=" * 50)
    if db_ok and app_ok:
        print("🎉 All tests passed! SQLite integration is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the details above.")

if __name__ == "__main__":
    main() 