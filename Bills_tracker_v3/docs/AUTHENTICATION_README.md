# 🔐 Authentication System - Bills Tracker v3

## Overview

Bills Tracker v3 now includes a comprehensive authentication system that allows multiple users to securely access the application with their own accounts. The system provides user registration, login, logout, and profile management features.

## Features

### ✅ **User Registration**
- Create new user accounts with username and email
- Password validation and secure hashing
- Duplicate username/email prevention
- Admin and regular user roles

### ✅ **User Login**
- Secure authentication with username and password
- Session management with automatic expiration
- Remember login state
- Invalid credential handling

### ✅ **User Logout**
- Secure session termination
- Automatic cleanup of expired sessions
- Return to login screen

### ✅ **Profile Management**
- View account information
- Change password functionality
- Account creation date and last login tracking
- Role-based access control

### ✅ **Security Features**
- SHA-256 password hashing with salt
- Session token management
- Automatic session expiration (24 hours)
- SQL injection prevention

## Database Schema

### Users Table
```sql
CREATE TABLE users (
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
```

### User Sessions Table
```sql
CREATE TABLE user_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    session_token TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    is_active INTEGER DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

## Installation & Setup

### 1. Run Migration Script
```bash
cd Bills_tracker_v3
python migrations/migrate_auth_tables.py
```

This will:
- Create authentication tables in your database
- Create a default admin account (username: `admin`, password: `admin123`)
- Optionally create a test user account

### 2. Start the Application
```bash
python main_desktop.py
```

The application will now show a login screen before accessing the main interface.

## Usage

### First Time Setup
1. **Login as Admin**: Use the default admin account
   - Username: `admin`
   - Password: `admin123`

2. **Change Admin Password**: Click on "👤 Profile" in the sidebar to change the default password

3. **Create User Accounts**: Users can create their own accounts through the signup dialog

### User Registration
1. Click "Create Account" on the login screen
2. Fill in the registration form:
   - Username (3-20 characters, alphanumeric with underscores/hyphens)
   - Email (valid email format)
   - Password (minimum 6 characters)
   - Confirm password
3. Click "Create Account"

### User Login
1. Enter username and password
2. Click "Login"
3. The application will remember your session for 24 hours

### Profile Management
1. Click "👤 Profile" in the sidebar
2. View account information
3. Change password if needed:
   - Enter current password
   - Enter new password (minimum 6 characters)
   - Confirm new password
   - Click "Change Password"

### Logout
1. Click "🚪 Logout" in the sidebar
2. You'll be returned to the login screen
3. Your session will be terminated

## Security Features

### Password Security
- **Hashing**: Passwords are hashed using SHA-256 with a random salt
- **Salt Generation**: Each password uses a unique 32-byte salt
- **Verification**: Secure password verification without storing plain text

### Session Security
- **Token Generation**: 32-byte random session tokens
- **Expiration**: Sessions automatically expire after 24 hours
- **Cleanup**: Expired sessions are automatically cleaned up
- **Logout**: Sessions are immediately invalidated on logout

### Database Security
- **SQL Injection Prevention**: All queries use parameterized statements
- **Input Validation**: Username, email, and password validation
- **Unique Constraints**: Username and email uniqueness enforced

## API Reference

### Core Functions

#### `create_user(username, email, password, is_admin=False)`
Create a new user account.

**Parameters:**
- `username` (str): Unique username (3-20 characters)
- `email` (str): Valid email address
- `password` (str): Password (minimum 6 characters)
- `is_admin` (bool): Whether user has admin privileges

**Returns:**
```python
{
    "success": True/False,
    "user_id": int,  # if successful
    "username": str,  # if successful
    "email": str,    # if successful
    "is_admin": bool, # if successful
    "error": str     # if failed
}
```

#### `authenticate_user(username, password)`
Authenticate user credentials and create session.

**Parameters:**
- `username` (str): User's username
- `password` (str): User's password

**Returns:**
```python
{
    "success": True/False,
    "user_id": int,      # if successful
    "username": str,     # if successful
    "email": str,        # if successful
    "is_admin": bool,    # if successful
    "session_token": str, # if successful
    "expires_at": datetime, # if successful
    "error": str         # if failed
}
```

#### `validate_session(session_token)`
Validate a session token and return user information.

**Parameters:**
- `session_token` (str): Session token to validate

**Returns:**
```python
{
    "user_id": int,
    "username": str,
    "email": str,
    "is_admin": bool,
    "expires_at": str
}
# or None if invalid
```

#### `logout_user(session_token)`
Logout user by invalidating session.

**Parameters:**
- `session_token` (str): Session token to invalidate

**Returns:**
- `bool`: True if logout successful, False otherwise

#### `change_password(user_id, current_password, new_password)`
Change user password.

**Parameters:**
- `user_id` (int): User ID
- `current_password` (str): Current password
- `new_password` (str): New password

**Returns:**
```python
{
    "success": True/False,
    "error": str  # if failed
}
```

#### `get_user_by_id(user_id)`
Get user profile information.

**Parameters:**
- `user_id` (int): User ID

**Returns:**
```python
{
    "id": int,
    "username": str,
    "email": str,
    "created_at": str,
    "last_login": str,
    "is_admin": bool,
    "is_active": bool
}
# or None if user not found
```

## Testing

### Run Authentication Tests
```bash
cd Bills_tracker_v3
python tests/test_authentication.py
```

### Run Authentication Demo
```bash
cd Bills_tracker_v3
python demo/demo_authentication.py
```

## Troubleshooting

### Common Issues

#### "Database file not found"
- Ensure you've run the main application at least once to create the database
- Run the migration script: `python migrations/migrate_auth_tables.py`

#### "Authentication tables already exist"
- This is normal if you've already run the migration
- The script will skip table creation if they already exist

#### "Invalid username or password"
- Check that you're using the correct credentials
- For first login, use admin/admin123
- Try creating a new account if needed

#### "Username or email already exists"
- Choose a different username or email
- Usernames and emails must be unique

### Password Requirements
- Minimum 6 characters
- No special requirements (but consider using strong passwords)

### Username Requirements
- 3-20 characters long
- Alphanumeric characters, underscores, and hyphens only
- Must be unique

### Email Requirements
- Valid email format (e.g., user@example.com)
- Must be unique

## Future Enhancements

### Planned Features
- [ ] Password reset functionality
- [ ] Email verification
- [ ] Two-factor authentication
- [ ] Remember me functionality
- [ ] Account deactivation
- [ ] User roles and permissions
- [ ] Session persistence across app restarts

### Security Improvements
- [ ] Password strength requirements
- [ ] Account lockout after failed attempts
- [ ] Session timeout configuration
- [ ] Audit logging
- [ ] Encryption at rest

## Support

If you encounter any issues with the authentication system:

1. Check the troubleshooting section above
2. Run the test suite to verify functionality
3. Check the console for error messages
4. Ensure the database is properly initialized

For additional help, refer to the main README.md file or create an issue in the project repository. 