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

def insert_bill(bill_data):
    """Insert a new bill into the database. bill_data is a dict."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bills (
            name, due_date, billing_cycle, reminder_days, web_page,
            login_info, password, paid, company_email, support_phone, billing_phone,
            customer_service_hours, account_number, reference_id, support_chat_url, mobile_app
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        bill_data.get('name', ''),
        bill_data.get('due_date', ''),
        bill_data.get('billing_cycle', ''),
        bill_data.get('reminder_days', 7),
        bill_data.get('web_page', ''),
        bill_data.get('login_info', ''),
        bill_data.get('password', ''),
        1 if bill_data.get('paid', False) else 0,
        bill_data.get('company_email', ''),
        bill_data.get('support_phone', ''),
        bill_data.get('billing_phone', ''),
        bill_data.get('customer_service_hours', ''),
        bill_data.get('account_number', ''),
        bill_data.get('reference_id', ''),
        bill_data.get('support_chat_url', ''),
        bill_data.get('mobile_app', '')
    ))
    conn.commit()
    conn.close()

def update_bill(bill_id, bill_data):
    """Update a bill in the database by id. bill_data is a dict."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE bills SET
            name = ?,
            due_date = ?,
            billing_cycle = ?,
            reminder_days = ?,
            web_page = ?,
            login_info = ?,
            password = ?,
            paid = ?,
            company_email = ?,
            support_phone = ?,
            billing_phone = ?,
            customer_service_hours = ?,
            account_number = ?,
            reference_id = ?,
            support_chat_url = ?,
            mobile_app = ?
        WHERE id = ?
    ''', (
        bill_data.get('name', ''),
        bill_data.get('due_date', ''),
        bill_data.get('billing_cycle', ''),
        bill_data.get('reminder_days', 7),
        bill_data.get('web_page', ''),
        bill_data.get('login_info', ''),
        bill_data.get('password', ''),
        1 if bill_data.get('paid', False) else 0,
        bill_data.get('company_email', ''),
        bill_data.get('support_phone', ''),
        bill_data.get('billing_phone', ''),
        bill_data.get('customer_service_hours', ''),
        bill_data.get('account_number', ''),
        bill_data.get('reference_id', ''),
        bill_data.get('support_chat_url', ''),
        bill_data.get('mobile_app', ''),
        bill_id
    ))
    conn.commit()
    conn.close()

def delete_bill(bill_id):
    """Delete a bill from the database by id."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM bills WHERE id = ?', (bill_id,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
    print(f"Database '{DB_FILE}' initialized with bills and templates tables.") 