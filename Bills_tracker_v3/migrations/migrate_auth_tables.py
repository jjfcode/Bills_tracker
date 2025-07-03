#!/usr/bin/env python3
"""
Migration script to add authentication tables to Bills Tracker v3 database.

This script adds:
- users table (user accounts with encrypted passwords)
- user_sessions table (active user sessions)

Run this script to enable user authentication features.
"""

import sqlite3
import hashlib
import secrets
import os
import sys

# Add src to path to import modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.auth import initialize_auth_database, generate_salt, hash_password

def check_database_exists():
    """Check if the database file exists"""
    db_file = 'bills_tracker.db'
    if not os.path.exists(db_file):
        print(f"❌ Database file '{db_file}' not found!")
        print("Please run the main application first to create the database.")
        return False
    return True

def backup_database():
    """Create a backup of the current database"""
    import shutil
    from datetime import datetime
    
    db_file = 'bills_tracker.db'
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f'bills_tracker_backup_{timestamp}.db'
    
    try:
        shutil.copy2(db_file, backup_file)
        print(f"✓ Database backed up to: {backup_file}")
        return True
    except Exception as e:
        print(f"❌ Failed to create backup: {e}")
        return False

def check_existing_tables():
    """Check if auth tables already exist"""
    conn = sqlite3.connect('bills_tracker.db')
    cursor = conn.cursor()
    
    # Check if users table exists
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='users'
    """)
    users_exists = cursor.fetchone() is not None
    
    # Check if user_sessions table exists
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='user_sessions'
    """)
    sessions_exists = cursor.fetchone() is not None
    
    conn.close()
    
    return users_exists, sessions_exists

def migrate_auth_tables():
    """Migrate authentication tables to existing database"""
    print("🔐 Bills Tracker v3 - Authentication Migration")
    print("=" * 50)
    
    # Check if database exists
    if not check_database_exists():
        return False
    
    # Check existing tables
    users_exists, sessions_exists = check_existing_tables()
    
    if users_exists and sessions_exists:
        print("✓ Authentication tables already exist!")
        print("Migration not needed.")
        return True
    
    print(f"Current state:")
    print(f"  - users table: {'✓' if users_exists else '❌'}")
    print(f"  - user_sessions table: {'✓' if sessions_exists else '❌'}")
    print()
    
    # Create backup
    print("Creating database backup...")
    if not backup_database():
        response = input("Continue without backup? (y/N): ").lower()
        if response != 'y':
            print("Migration cancelled.")
            return False
    
    # Initialize auth database
    print("\nInitializing authentication tables...")
    try:
        initialize_auth_database()
        print("✓ Authentication tables created successfully!")
        
        # Verify tables were created
        users_exists_new, sessions_exists_new = check_existing_tables()
        
        if users_exists_new and sessions_exists_new:
            print("\n✓ Migration completed successfully!")
            print("\nDefault admin account created:")
            print("  Username: admin")
            print("  Password: admin123")
            print("\n⚠️  IMPORTANT: Change the admin password after first login!")
            return True
        else:
            print("❌ Migration failed - tables not created properly")
            return False
            
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def create_test_user():
    """Create a test user account"""
    print("\n" + "=" * 50)
    print("Create Test User Account")
    print("=" * 50)
    
    try:
        from core.auth import create_user
        
        # Create test user
        result = create_user(
            username="testuser",
            email="test@example.com",
            password="test123",
            is_admin=False
        )
        
        if result["success"]:
            print("✓ Test user created successfully!")
            print(f"  Username: {result['username']}")
            print(f"  Email: {result['email']}")
            print(f"  Password: test123")
            return True
        else:
            print(f"❌ Failed to create test user: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
        return False

def main():
    """Main migration function"""
    print("Bills Tracker v3 - Authentication Migration Tool")
    print("=" * 60)
    
    # Run migration
    if migrate_auth_tables():
        print("\n" + "=" * 60)
        print("Migration Summary:")
        print("✓ Authentication tables added to database")
        print("✓ Default admin account created")
        print("✓ Session management enabled")
        
        # Ask if user wants to create a test account
        response = input("\nCreate a test user account? (y/N): ").lower()
        if response == 'y':
            create_test_user()
        
        print("\n🎉 Migration completed successfully!")
        print("\nYou can now:")
        print("  1. Run the main application")
        print("  2. Login with admin/admin123")
        print("  3. Create new user accounts")
        print("  4. Change the admin password")
        
    else:
        print("\n❌ Migration failed!")
        print("Please check the error messages above and try again.")

if __name__ == "__main__":
    main() 