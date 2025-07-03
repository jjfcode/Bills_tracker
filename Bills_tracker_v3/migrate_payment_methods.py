#!/usr/bin/env python3
"""
Migration script to add payment methods support to the Bills Tracker database.
This script will:
1. Create the payment_methods table
2. Add payment_method_id column to bills table
3. Insert default payment methods
4. Update existing bills to have NULL payment_method_id
"""

import sqlite3
import os

DB_FILE = 'bills_tracker.db'

def migrate_payment_methods():
    """Migrate the database to support payment methods."""
    if not os.path.exists(DB_FILE):
        print(f"Database file '{DB_FILE}' not found. Please run the main application first.")
        return False
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        # Check if payment_methods table already exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='payment_methods'")
        if cursor.fetchone():
            print("Payment methods table already exists.")
        else:
            # Create payment_methods table
            cursor.execute('''
                CREATE TABLE payment_methods (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    description TEXT,
                    is_automatic INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            print("Created payment_methods table.")
            
            # Insert default payment methods
            default_payment_methods = [
                ("Auto-Pay", "Automatic payment from bank account", 1),
                ("Manual Bank Transfer", "Manual bank transfer or online payment", 0),
                ("Credit Card", "Payment via credit card", 0),
                ("Check", "Payment by check", 0),
                ("Cash", "Cash payment", 0),
                ("Digital Wallet", "Apple Pay, Google Pay, etc.", 0),
                ("Direct Debit", "Direct debit from account", 1),
                ("Other", "Other payment methods", 0)
            ]
            
            for name, description, is_automatic in default_payment_methods:
                cursor.execute('''
                    INSERT OR IGNORE INTO payment_methods (name, description, is_automatic) 
                    VALUES (?, ?, ?)
                ''', (name, description, is_automatic))
            print("Inserted default payment methods.")
        
        # Check if payment_method_id column exists in bills table
        cursor.execute("PRAGMA table_info(bills)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'payment_method_id' not in columns:
            # Add payment_method_id column to bills table
            cursor.execute('ALTER TABLE bills ADD COLUMN payment_method_id INTEGER')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_bills_payment_method 
                ON bills(payment_method_id)
            ''')
            print("Added payment_method_id column to bills table.")
        else:
            print("payment_method_id column already exists in bills table.")
        
        conn.commit()
        print("Migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"Migration failed: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def verify_migration():
    """Verify that the migration was successful."""
    if not os.path.exists(DB_FILE):
        print(f"Database file '{DB_FILE}' not found.")
        return False
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        # Check payment_methods table
        cursor.execute("SELECT COUNT(*) FROM payment_methods")
        payment_method_count = cursor.fetchone()[0]
        print(f"Payment methods table has {payment_method_count} records.")
        
        # Check bills table structure
        cursor.execute("PRAGMA table_info(bills)")
        columns = [column[1] for column in cursor.fetchall()]
        if 'payment_method_id' in columns:
            print("✓ payment_method_id column exists in bills table.")
        else:
            print("✗ payment_method_id column missing from bills table.")
            return False
        
        # Check sample payment methods
        cursor.execute("SELECT name, is_automatic FROM payment_methods LIMIT 5")
        methods = cursor.fetchall()
        print("Sample payment methods:")
        for name, is_automatic in methods:
            auto_status = "Automatic" if is_automatic else "Manual"
            print(f"  - {name} ({auto_status})")
        
        return True
        
    except Exception as e:
        print(f"Verification failed: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    print("Bills Tracker - Payment Methods Migration")
    print("=" * 50)
    
    success = migrate_payment_methods()
    if success:
        print("\nVerifying migration...")
        verify_migration()
    else:
        print("Migration failed. Please check the error messages above.") 