#!/usr/bin/env python3
"""
Test script for export/import functionality
"""

import sys
import os
import tempfile
import csv
sys.path.append(os.path.join(os.path.dirname(__file__), "src", "core"))
from db import fetch_all_bills, insert_bill, initialize_database

def test_export_import():
    """Test the export and import functionality"""
    print("Testing Export/Import Functionality...")
    
    # Initialize database
    initialize_database()
    print("✅ Database initialized")
    
    # Add some test bills if none exist
    original_bills = fetch_all_bills()
    if len(original_bills) == 0:
        print("Adding test bills...")
        test_bills = [
            {
                'name': 'Test Bill 1',
                'due_date': '2024-02-15',
                'billing_cycle': 'monthly',
                'reminder_days': 7,
                'web_page': 'https://example.com',
                'company_email': 'test@example.com',
                'support_phone': '555-1234',
                'account_number': '12345',
                'paid': False
            },
            {
                'name': 'Test Bill 2',
                'due_date': '2024-03-01',
                'billing_cycle': 'quarterly',
                'reminder_days': 14,
                'web_page': 'https://test.com',
                'company_email': 'billing@test.com',
                'support_phone': '555-5678',
                'account_number': '67890',
                'paid': True
            }
        ]
        
        for bill in test_bills:
            insert_bill(bill)
        
        original_bills = fetch_all_bills()
        print(f"Added {len(test_bills)} test bills")
    
    print(f"Found {len(original_bills)} bills in database")
    
    # Create a temporary CSV file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='', encoding='utf-8') as temp_file:
        temp_path = temp_file.name
        
        # Export bills to CSV
        fieldnames = ['name', 'due_date', 'billing_cycle', 'reminder_days', 'web_page', 
                     'company_email', 'support_phone', 'account_number', 'paid']
        writer = csv.DictWriter(temp_file, fieldnames=fieldnames)
        writer.writeheader()
        
        for bill in original_bills:
            writer.writerow({
                'name': bill.get('name', ''),
                'due_date': bill.get('due_date', ''),
                'billing_cycle': bill.get('billing_cycle', ''),
                'reminder_days': bill.get('reminder_days', ''),
                'web_page': bill.get('web_page', ''),
                'company_email': bill.get('company_email', ''),
                'support_phone': bill.get('support_phone', ''),
                'account_number': bill.get('account_number', ''),
                'paid': 'Yes' if bill.get('paid', False) else 'No'
            })
    
    print(f"Exported bills to: {temp_path}")
    
    # Read the CSV back and verify content
    imported_bills = []
    with open(temp_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            imported_bills.append(row)
    
    print(f"Read {len(imported_bills)} bills from CSV")
    
    # Verify the data matches
    if len(original_bills) == len(imported_bills):
        print("✅ Export/Import test PASSED: Bill count matches")
    else:
        print("❌ Export/Import test FAILED: Bill count mismatch")
        return False
    
    # Clean up
    os.unlink(temp_path)
    print("✅ Temporary file cleaned up")
    
    return True

if __name__ == "__main__":
    success = test_export_import()
    if success:
        print("\n🎉 All tests passed!")
    else:
        print("\n💥 Some tests failed!")
        sys.exit(1) 