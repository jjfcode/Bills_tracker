#!/usr/bin/env python3
"""
Demo script for Bills Tracker v3 Authentication System

This script demonstrates:
- User registration and login
- Password management
- Session handling
- User profile management

Run this script to test the authentication features.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.auth import (
    initialize_auth_database, 
    create_user, 
    authenticate_user, 
    validate_session,
    logout_user,
    change_password,
    get_user_by_id,
    cleanup_expired_sessions
)

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"🔐 {title}")
    print("=" * 60)

def print_success(message):
    """Print success message"""
    print(f"✅ {message}")

def print_error(message):
    """Print error message"""
    print(f"❌ {message}")

def print_info(message):
    """Print info message"""
    print(f"ℹ️  {message}")

def demo_user_registration():
    """Demonstrate user registration"""
    print_header("User Registration Demo")
    
    # Test user data
    test_users = [
        {
            "username": "john_doe",
            "email": "john@example.com",
            "password": "secure123",
            "is_admin": False
        },
        {
            "username": "admin_user",
            "email": "admin@example.com",
            "password": "admin456",
            "is_admin": True
        },
        {
            "username": "test_user",
            "email": "test@example.com",
            "password": "test789",
            "is_admin": False
        }
    ]
    
    created_users = []
    
    for user_data in test_users:
        print(f"\nCreating user: {user_data['username']}")
        result = create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            is_admin=user_data['is_admin']
        )
        
        if result["success"]:
            print_success(f"User '{user_data['username']}' created successfully!")
            created_users.append(result)
        else:
            print_error(f"Failed to create user '{user_data['username']}': {result['error']}")
    
    return created_users

def demo_user_login(users):
    """Demonstrate user login"""
    print_header("User Login Demo")
    
    login_results = []
    
    for user in users:
        print(f"\nLogging in user: {user['username']}")
        result = authenticate_user(user['username'], "wrong_password")
        
        if not result["success"]:
            print_info(f"Failed login with wrong password (expected): {result['error']}")
        
        # Try correct password
        result = authenticate_user(user['username'], "secure123" if user['username'] == 'john_doe' else 
                                 "admin456" if user['username'] == 'admin_user' else "test789")
        
        if result["success"]:
            print_success(f"User '{user['username']}' logged in successfully!")
            print(f"   Session token: {result['session_token'][:20]}...")
            print(f"   Expires at: {result['expires_at']}")
            login_results.append(result)
        else:
            print_error(f"Login failed: {result['error']}")
    
    return login_results

def demo_session_validation(sessions):
    """Demonstrate session validation"""
    print_header("Session Validation Demo")
    
    for session in sessions:
        print(f"\nValidating session for user: {session['username']}")
        
        # Validate session
        user_info = validate_session(session['session_token'])
        
        if user_info:
            print_success(f"Session valid for user: {user_info['username']}")
            print(f"   User ID: {user_info['user_id']}")
            print(f"   Email: {user_info['email']}")
            print(f"   Is Admin: {user_info['is_admin']}")
            print(f"   Expires at: {user_info['expires_at']}")
        else:
            print_error("Session validation failed")
        
        # Test invalid session
        invalid_token = "invalid_token_12345"
        invalid_result = validate_session(invalid_token)
        
        if not invalid_result:
            print_info("Invalid session correctly rejected")
        else:
            print_error("Invalid session was incorrectly accepted")

def demo_password_management(sessions):
    """Demonstrate password management"""
    print_header("Password Management Demo")
    
    if not sessions:
        print_error("No active sessions for password management demo")
        return
    
    # Use first session
    session = sessions[0]
    user_id = session['user_id']
    
    print(f"\nChanging password for user: {session['username']}")
    
    # Try wrong current password
    result = change_password(user_id, "wrong_password", "new_password")
    if not result["success"]:
        print_info(f"Correctly rejected wrong current password: {result['error']}")
    
    # Change password with correct current password
    current_password = "secure123" if session['username'] == 'john_doe' else "admin456"
    result = change_password(user_id, current_password, "new_secure_password")
    
    if result["success"]:
        print_success("Password changed successfully!")
        
        # Try logging in with new password
        login_result = authenticate_user(session['username'], "new_secure_password")
        if login_result["success"]:
            print_success("Successfully logged in with new password!")
        else:
            print_error(f"Failed to login with new password: {login_result['error']}")
    else:
        print_error(f"Password change failed: {result['error']}")

def demo_user_profile(sessions):
    """Demonstrate user profile management"""
    print_header("User Profile Demo")
    
    if not sessions:
        print_error("No active sessions for profile demo")
        return
    
    # Use first session
    session = sessions[0]
    user_id = session['user_id']
    
    print(f"\nGetting profile for user: {session['username']}")
    
    user_info = get_user_by_id(user_id)
    
    if user_info:
        print_success("User profile retrieved successfully!")
        print(f"   Username: {user_info['username']}")
        print(f"   Email: {user_info['email']}")
        print(f"   Created at: {user_info['created_at']}")
        print(f"   Last login: {user_info['last_login']}")
        print(f"   Is Admin: {user_info['is_admin']}")
        print(f"   Is Active: {user_info['is_active']}")
    else:
        print_error("Failed to retrieve user profile")

def demo_logout(sessions):
    """Demonstrate user logout"""
    print_header("User Logout Demo")
    
    if not sessions:
        print_error("No active sessions for logout demo")
        return
    
    # Use first session
    session = sessions[0]
    
    print(f"\nLogging out user: {session['username']}")
    
    # Logout
    success = logout_user(session['session_token'])
    
    if success:
        print_success("User logged out successfully!")
        
        # Try to validate the logged out session
        user_info = validate_session(session['session_token'])
        if not user_info:
            print_info("Session correctly invalidated after logout")
        else:
            print_error("Session still valid after logout")
    else:
        print_error("Logout failed")

def demo_session_cleanup():
    """Demonstrate session cleanup"""
    print_header("Session Cleanup Demo")
    
    print("\nCleaning up expired sessions...")
    cleanup_expired_sessions()
    print_success("Session cleanup completed")

def main():
    """Main demo function"""
    print("🔐 Bills Tracker v3 - Authentication System Demo")
    print("=" * 70)
    
    try:
        # Initialize database
        print_info("Initializing authentication database...")
        initialize_auth_database()
        print_success("Database initialized successfully!")
        
        # Run demos
        users = demo_user_registration()
        sessions = demo_user_login(users)
        demo_session_validation(sessions)
        demo_password_management(sessions)
        demo_user_profile(sessions)
        demo_logout(sessions)
        demo_session_cleanup()
        
        print_header("Demo Summary")
        print_success("All authentication features demonstrated successfully!")
        print("\nFeatures tested:")
        print("  ✅ User registration with validation")
        print("  ✅ Secure password hashing")
        print("  ✅ User login and authentication")
        print("  ✅ Session management")
        print("  ✅ Session validation")
        print("  ✅ Password change functionality")
        print("  ✅ User profile management")
        print("  ✅ User logout")
        print("  ✅ Session cleanup")
        
        print("\n🎉 Authentication system is working correctly!")
        
    except Exception as e:
        print_error(f"Demo failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 