import sqlite3
import hashlib
import os
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

# Database file path
DB_FILE = 'bills_tracker.db'

# Users table schema
USERS_SCHEMA = '''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active INTEGER DEFAULT 1,
    is_admin INTEGER DEFAULT 0
);
'''

# User sessions table schema
SESSIONS_SCHEMA = '''
CREATE TABLE IF NOT EXISTS user_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    session_token TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    is_active INTEGER DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
'''

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_auth_database():
    """Initialize authentication tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute(USERS_SCHEMA)
    
    # Create sessions table
    cursor.execute(SESSIONS_SCHEMA)
    
    # Create admin user if not exists
    admin_username = "admin"
    cursor.execute("SELECT id FROM users WHERE username = ?", (admin_username,))
    if not cursor.fetchone():
        # Create default admin user
        password = "admin123"  # Default password - should be changed
        salt = generate_salt()
        password_hash = hash_password(password, salt)
        
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, salt, is_admin)
            VALUES (?, ?, ?, ?, ?)
        ''', (admin_username, "admin@billstracker.com", password_hash, salt, 1))
        
        print("✓ Default admin user created (username: admin, password: admin123)")
    
    conn.commit()
    conn.close()

def generate_salt(length: int = 32) -> str:
    """Generate a random salt for password hashing"""
    return secrets.token_hex(length)

def hash_password(password: str, salt: str) -> str:
    """Hash password with salt using SHA-256"""
    salted_password = password + salt
    return hashlib.sha256(salted_password.encode()).hexdigest()

def verify_password(password: str, stored_hash: str, stored_salt: str) -> bool:
    """Verify password against stored hash and salt"""
    return hash_password(password, stored_salt) == stored_hash

def create_user(username: str, email: str, password: str, is_admin: bool = False) -> Dict[str, Any]:
    """Create a new user account"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if username or email already exists
        cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
        if cursor.fetchone():
            conn.close()
            return {"success": False, "error": "Username or email already exists"}
        
        # Generate salt and hash password
        salt = generate_salt()
        password_hash = hash_password(password, salt)
        
        # Insert new user
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, salt, is_admin)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, email, password_hash, salt, 1 if is_admin else 0))
        
        user_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "user_id": user_id,
            "username": username,
            "email": email,
            "is_admin": is_admin
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def authenticate_user(username: str, password: str) -> Dict[str, Any]:
    """Authenticate user with username and password"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get user by username
        cursor.execute('''
            SELECT id, username, email, password_hash, salt, is_admin, is_active
            FROM users WHERE username = ?
        ''', (username,))
        
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            return {"success": False, "error": "Invalid username or password"}
        
        if not user['is_active']:
            conn.close()
            return {"success": False, "error": "Account is deactivated"}
        
        # Verify password
        if not verify_password(password, user['password_hash'], user['salt']):
            conn.close()
            return {"success": False, "error": "Invalid username or password"}
        
        # Update last login
        cursor.execute('''
            UPDATE users SET last_login = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (user['id'],))
        
        # Create session
        session_token = secrets.token_hex(32)
        expires_at = datetime.now() + timedelta(hours=24)  # 24 hour session
        
        cursor.execute('''
            INSERT INTO user_sessions (user_id, session_token, expires_at)
            VALUES (?, ?, ?)
        ''', (user['id'], session_token, expires_at.strftime('%Y-%m-%d %H:%M:%S')))
        
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "user_id": user['id'],
            "username": user['username'],
            "email": user['email'],
            "is_admin": bool(user['is_admin']),
            "session_token": session_token,
            "expires_at": expires_at
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def validate_session(session_token: str) -> Optional[Dict[str, Any]]:
    """Validate session token and return user info"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get session and user info
        cursor.execute('''
            SELECT u.id, u.username, u.email, u.is_admin, s.expires_at
            FROM users u
            JOIN user_sessions s ON u.id = s.user_id
            WHERE s.session_token = ? AND s.is_active = 1 AND s.expires_at > CURRENT_TIMESTAMP
        ''', (session_token,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                "user_id": result['id'],
                "username": result['username'],
                "email": result['email'],
                "is_admin": bool(result['is_admin']),
                "expires_at": result['expires_at']
            }
        
        return None
        
    except Exception:
        return None

def logout_user(session_token: str) -> bool:
    """Logout user by deactivating session"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE user_sessions SET is_active = 0
            WHERE session_token = ?
        ''', (session_token,))
        
        conn.commit()
        conn.close()
        
        return True
        
    except Exception:
        return False

def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Get user information by ID"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, email, created_at, last_login, is_admin, is_active
            FROM users WHERE id = ?
        ''', (user_id,))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                "id": user['id'],
                "username": user['username'],
                "email": user['email'],
                "created_at": user['created_at'],
                "last_login": user['last_login'],
                "is_admin": bool(user['is_admin']),
                "is_active": bool(user['is_active'])
            }
        
        return None
        
    except Exception:
        return None

def change_password(user_id: int, current_password: str, new_password: str) -> Dict[str, Any]:
    """Change user password"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get current user info
        cursor.execute('''
            SELECT password_hash, salt FROM users WHERE id = ?
        ''', (user_id,))
        
        user = cursor.fetchone()
        if not user:
            conn.close()
            return {"success": False, "error": "User not found"}
        
        # Verify current password
        if not verify_password(current_password, user['password_hash'], user['salt']):
            conn.close()
            return {"success": False, "error": "Current password is incorrect"}
        
        # Generate new salt and hash
        new_salt = generate_salt()
        new_password_hash = hash_password(new_password, new_salt)
        
        # Update password
        cursor.execute('''
            UPDATE users SET password_hash = ?, salt = ?
            WHERE id = ?
        ''', (new_password_hash, new_salt, user_id))
        
        conn.commit()
        conn.close()
        
        return {"success": True}
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def cleanup_expired_sessions():
    """Clean up expired sessions"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE user_sessions SET is_active = 0
            WHERE expires_at <= CURRENT_TIMESTAMP
        ''')
        
        conn.commit()
        conn.close()
        
    except Exception:
        pass

if __name__ == "__main__":
    initialize_auth_database()
    print("Authentication database initialized successfully!") 