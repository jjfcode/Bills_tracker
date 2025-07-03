#!/usr/bin/env python3
"""
Migration script to move data from JSON files to SQLite database.
"""

import json
import os
import sys
from db import get_db_connection, initialize_database

# JSON file paths
BILLS_FILE = 'bills.json'
TEMPLATES_FILE = 'bill_templates.json'

def migrate_bills_to_sqlite():
    """Migrate bills from JSON to SQLite."""
    if not os.path.exists(BILLS_FILE):
        print(f"⚠️  {BILLS_FILE} not found. Skipping bills migration.")
        return 0
    
    try:
        with open(BILLS_FILE, 'r') as f:
            bills_data = json.load(f)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        migrated_count = 0
        for bill in bills_data:
            cursor.execute('''
                INSERT INTO bills (
                    name, due_date, billing_cycle, reminder_days, web_page,
                    login_info, password, paid, company_email, support_phone,
                    billing_phone, customer_service_hours, account_number,
                    reference_id, support_chat_url, mobile_app
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                bill.get('name', ''),
                bill.get('due_date', ''),
                bill.get('billing_cycle', 'monthly'),
                bill.get('reminder_days', 7),
                bill.get('web_page', ''),
                bill.get('login_info', ''),
                bill.get('password', ''),
                1 if bill.get('paid', False) else 0,
                bill.get('company_email', ''),
                bill.get('support_phone', ''),
                bill.get('billing_phone', ''),
                bill.get('customer_service_hours', ''),
                bill.get('account_number', ''),
                bill.get('reference_id', ''),
                bill.get('support_chat_url', ''),
                bill.get('mobile_app', '')
            ))
            migrated_count += 1
        
        conn.commit()
        conn.close()
        
        print(f"✅ Migrated {migrated_count} bills to SQLite database.")
        return migrated_count
        
    except Exception as e:
        print(f"❌ Error migrating bills: {e}")
        return 0

def migrate_templates_to_sqlite():
    """Migrate templates from JSON to SQLite."""
    if not os.path.exists(TEMPLATES_FILE):
        print(f"⚠️  {TEMPLATES_FILE} not found. Skipping templates migration.")
        return 0
    
    try:
        with open(TEMPLATES_FILE, 'r') as f:
            templates_data = json.load(f)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        migrated_count = 0
        for template in templates_data:
            cursor.execute('''
                INSERT INTO templates (
                    name, due_date, billing_cycle, reminder_days, web_page,
                    login_info, password, company_email, support_phone,
                    billing_phone, customer_service_hours, account_number,
                    reference_id, support_chat_url, mobile_app
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                template.get('name', ''),
                template.get('due_date', ''),
                template.get('billing_cycle', 'monthly'),
                template.get('reminder_days', 7),
                template.get('web_page', ''),
                template.get('login_info', ''),
                template.get('password', ''),
                template.get('company_email', ''),
                template.get('support_phone', ''),
                template.get('billing_phone', ''),
                template.get('customer_service_hours', ''),
                template.get('account_number', ''),
                template.get('reference_id', ''),
                template.get('support_chat_url', ''),
                template.get('mobile_app', '')
            ))
            migrated_count += 1
        
        conn.commit()
        conn.close()
        
        print(f"✅ Migrated {migrated_count} templates to SQLite database.")
        return migrated_count
        
    except Exception as e:
        print(f"❌ Error migrating templates: {e}")
        return 0

def main():
    """Main migration function."""
    print("🔄 Starting migration from JSON to SQLite...")
    print("=" * 50)
    
    # Initialize database
    print("📊 Initializing SQLite database...")
    initialize_database()
    
    # Migrate bills
    print("\n📋 Migrating bills...")
    bills_count = migrate_bills_to_sqlite()
    
    # Migrate templates
    print("\n📋 Migrating templates...")
    templates_count = migrate_templates_to_sqlite()
    
    print("\n" + "=" * 50)
    print(f"🎉 Migration completed!")
    print(f"   • Bills migrated: {bills_count}")
    print(f"   • Templates migrated: {templates_count}")
    print(f"   • Database file: bills_tracker.db")
    
    if bills_count > 0 or templates_count > 0:
        print("\n⚠️  IMPORTANT: After verifying the migration, you can:")
        print("   • Rename or delete the old JSON files")
        print("   • Update bills-tracker.py to use SQLite instead of JSON")
        print("   • Test all functionality to ensure it works correctly")

if __name__ == "__main__":
    main() 