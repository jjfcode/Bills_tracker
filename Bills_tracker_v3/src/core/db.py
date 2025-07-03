import sqlite3
import os
from datetime import datetime

DB_FILE = 'bills_tracker.db'

# Schema definitions
CATEGORIES_SCHEMA = '''
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    color TEXT DEFAULT '#1f538d',
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
'''

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
    mobile_app TEXT,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories (id)
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
    cursor.execute(CATEGORIES_SCHEMA)
    cursor.execute(BILLS_SCHEMA)
    cursor.execute(TEMPLATES_SCHEMA)
    
    # Insert default categories if they don't exist
    default_categories = [
        ("Utilities", "#ff6b6b", "Electricity, water, gas, internet"),
        ("Housing", "#4ecdc4", "Rent, mortgage, property taxes"),
        ("Transportation", "#45b7d1", "Car payment, insurance, fuel"),
        ("Insurance", "#96ceb4", "Health, life, auto insurance"),
        ("Entertainment", "#feca57", "Streaming, games, hobbies"),
        ("Food & Dining", "#ff9ff3", "Groceries, restaurants"),
        ("Healthcare", "#54a0ff", "Medical bills, prescriptions"),
        ("Education", "#5f27cd", "Tuition, books, courses"),
        ("Shopping", "#00d2d3", "Clothing, electronics, general"),
        ("Other", "#c8d6e5", "Miscellaneous expenses")
    ]
    
    for name, color, description in default_categories:
        cursor.execute('''
            INSERT OR IGNORE INTO categories (name, color, description) 
            VALUES (?, ?, ?)
        ''', (name, color, description))
    
    conn.commit()
    conn.close()

def fetch_all_bills():
    """Fetch all bills from the database and return as a list of dicts."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT b.*, c.name as category_name, c.color as category_color 
        FROM bills b 
        LEFT JOIN categories c ON b.category_id = c.id 
        ORDER BY b.due_date
    ''')
    rows = cursor.fetchall()
    bills = []
    for row in rows:
        bill = dict(row)
        bill['paid'] = bool(bill.get('paid', 0))
        if not bill.get('category_name'):
            bill['category_name'] = 'Uncategorized'
            bill['category_color'] = '#c8d6e5'
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
            customer_service_hours, account_number, reference_id, support_chat_url, mobile_app, category_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        bill_data.get('category_id', None)
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
            mobile_app = ?,
            category_id = ?
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
        bill_data.get('category_id', None),
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

# Category functions
def fetch_all_categories():
    """Fetch all categories from the database and return as a list of dicts."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM categories ORDER BY name')
    rows = cursor.fetchall()
    categories = [dict(row) for row in rows]
    conn.close()
    return categories

def insert_category(category_data):
    """Insert a new category into the database. category_data is a dict."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO categories (name, color, description) 
        VALUES (?, ?, ?)
    ''', (
        category_data.get('name', ''),
        category_data.get('color', '#1f538d'),
        category_data.get('description', '')
    ))
    conn.commit()
    conn.close()

def update_category(category_id, category_data):
    """Update a category in the database by id. category_data is a dict."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE categories SET
            name = ?,
            color = ?,
            description = ?
        WHERE id = ?
    ''', (
        category_data.get('name', ''),
        category_data.get('color', '#1f538d'),
        category_data.get('description', ''),
        category_id
    ))
    conn.commit()
    conn.close()

def delete_category(category_id):
    """Delete a category from the database by id."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM categories WHERE id = ?', (category_id,))
    conn.commit()
    conn.close()

def get_category_name(category_id):
    """Get category name by id."""
    if not category_id:
        return "Uncategorized"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM categories WHERE id = ?', (category_id,))
    row = cursor.fetchone()
    conn.close()
    return row['name'] if row else "Uncategorized"

if __name__ == "__main__":
    initialize_database()
    print(f"Database '{DB_FILE}' initialized with bills and templates tables.") 