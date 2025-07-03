import sqlite3
import os
from datetime import datetime

DB_FILE = 'bills_tracker.db'

# Schema definitions
BILLS_SCHEMA = '''
CREATE TABLE IF NOT EXISTS bills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    due_date TEXT NOT NULL,
    billing_cycle TEXT,
    reminder_days INTEGER,
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
);
'''

TEMPLATES_SCHEMA = '''
CREATE TABLE IF NOT EXISTS templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    due_date TEXT,
    billing_cycle TEXT,
    reminder_days INTEGER,
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
);
'''

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(BILLS_SCHEMA)
    cursor.execute(TEMPLATES_SCHEMA)
    conn.commit()
    conn.close()

def fetch_all_bills():
    """Fetch all bills from the database and return as a list of dicts."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bills ORDER BY due_date')
    rows = cursor.fetchall()
    bills = []
    for row in rows:
        bill = dict(row)
        bill['paid'] = bool(bill.get('paid', 0))
        bills.append(bill)
    conn.close()
    return bills

if __name__ == "__main__":
    initialize_database()
    print(f"Database '{DB_FILE}' initialized with bills and templates tables.") 