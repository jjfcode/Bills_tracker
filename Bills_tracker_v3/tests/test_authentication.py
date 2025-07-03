#!/usr/bin/env python3
"""
Test script for Bills Tracker v3 Authentication System

This script tests all authentication features to ensure they work correctly.
"""

import sys
import os
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.auth import (
    initialize_auth_database,
    create_user,
    authenticate_user,
    validate_session,
    logout_user,
    change_password,
    get_user_by_id,
    cleanup_expired_sessions,
    generate_salt,
    hash_password,
    verify_password
)

class TestAuthentication(unittest.TestCase):
    """Test cases for authentication system"""
    
    def setUp(self):
        """Set up test environment"""
        # Initialize database for testing
        initialize_auth_database()
    
    def test_password_hashing(self):
        """Test password hashing and verification"""
        password = "test_password_123"
        salt = generate_salt()
        hashed = hash_password(password, salt)
        
        # Test correct password
        self.assertTrue(verify_password(password, hashed, salt))
        
        # Test wrong password
        self.assertFalse(verify_password("wrong_password", hashed, salt))
        
        # Test different salt
        different_salt = generate_salt()
        self.assertFalse(verify_password(password, hashed, different_salt))
    
    def test_user_creation(self):
        """Test user creation"""
        # Test valid user creation with unique username/email
        import time
        timestamp = int(time.time())
        unique_username = f"testuser_{timestamp}"
        unique_email = f"test_{timestamp}@example.com"
        
        result = create_user(unique_username, unique_email, "password123")
        self.assertTrue(result["success"])
        self.assertEqual(result["username"], unique_username)
        self.assertEqual(result["email"], unique_email)
        self.assertFalse(result["is_admin"])
        
        # Test duplicate username
        result = create_user(unique_username, "different@example.com", "password456")
        self.assertFalse(result["success"])
        self.assertIn("already exists", result["error"])
        
        # Test duplicate email
        result = create_user("differentuser", unique_email, "password456")
        self.assertFalse(result["success"])
        self.assertIn("already exists", result["error"])
    
    def test_user_authentication(self):
        """Test user authentication"""
        # Create a test user with unique credentials
        import time
        timestamp = int(time.time())
        unique_username = f"authuser_{timestamp}"
        unique_email = f"auth_{timestamp}@example.com"
        
        create_user(unique_username, unique_email, "authpass123")
        
        # Test correct credentials
        result = authenticate_user(unique_username, "authpass123")
        self.assertTrue(result["success"])
        self.assertEqual(result["username"], unique_username)
        self.assertEqual(result["email"], unique_email)
        self.assertIn("session_token", result)
        self.assertIn("expires_at", result)
        
        # Test wrong password
        result = authenticate_user(unique_username, "wrongpassword")
        self.assertFalse(result["success"])
        self.assertIn("Invalid", result["error"])
        
        # Test non-existent user
        result = authenticate_user("nonexistent", "password")
        self.assertFalse(result["success"])
        self.assertIn("Invalid", result["error"])
    
    def test_session_validation(self):
        """Test session validation"""
        # Create and authenticate user with unique credentials
        import time
        timestamp = int(time.time())
        unique_username = f"sessionuser_{timestamp}"
        unique_email = f"session_{timestamp}@example.com"
        
        create_user(unique_username, unique_email, "sessionpass123")
        auth_result = authenticate_user(unique_username, "sessionpass123")
        
        # Test valid session
        user_info = validate_session(auth_result["session_token"])
        self.assertIsNotNone(user_info)
        self.assertEqual(user_info["username"], unique_username)
        self.assertEqual(user_info["email"], unique_email)
        
        # Test invalid session
        invalid_info = validate_session("invalid_token")
        self.assertIsNone(invalid_info)
    
    def test_user_logout(self):
        """Test user logout"""
        # Create and authenticate user with unique credentials
        import time
        timestamp = int(time.time())
        unique_username = f"logoutuser_{timestamp}"
        unique_email = f"logout_{timestamp}@example.com"
        
        create_user(unique_username, unique_email, "logoutpass123")
        auth_result = authenticate_user(unique_username, "logoutpass123")
        
        # Test logout
        success = logout_user(auth_result["session_token"])
        self.assertTrue(success)
        
        # Verify session is invalidated
        user_info = validate_session(auth_result["session_token"])
        self.assertIsNone(user_info)
    
    def test_password_change(self):
        """Test password change"""
        # Create and authenticate user with unique credentials
        import time
        timestamp = int(time.time())
        unique_username = f"passuser_{timestamp}"
        unique_email = f"pass_{timestamp}@example.com"
        
        create_user(unique_username, unique_email, "oldpass123")
        auth_result = authenticate_user(unique_username, "oldpass123")
        
        # Test password change
        result = change_password(auth_result["user_id"], "oldpass123", "newpass456")
        self.assertTrue(result["success"])
        
        # Test login with new password
        new_auth = authenticate_user(unique_username, "newpass456")
        self.assertTrue(new_auth["success"])
        
        # Test login with old password (should fail)
        old_auth = authenticate_user(unique_username, "oldpass123")
        self.assertFalse(old_auth["success"])
        
        # Test wrong current password
        result = change_password(auth_result["user_id"], "wrongpass", "newpass789")
        self.assertFalse(result["success"])
        self.assertIn("incorrect", result["error"])
    
    def test_user_profile(self):
        """Test user profile retrieval"""
        # Create and authenticate user with unique credentials
        import time
        timestamp = int(time.time())
        unique_username = f"profileuser_{timestamp}"
        unique_email = f"profile_{timestamp}@example.com"
        
        create_user(unique_username, unique_email, "profilepass123")
        auth_result = authenticate_user(unique_username, "profilepass123")
        
        # Get user profile
        user_info = get_user_by_id(auth_result["user_id"])
        self.assertIsNotNone(user_info)
        self.assertEqual(user_info["username"], unique_username)
        self.assertEqual(user_info["email"], unique_email)
        self.assertFalse(user_info["is_admin"])
        self.assertTrue(user_info["is_active"])
        self.assertIsNotNone(user_info["created_at"])
    
    def test_admin_user(self):
        """Test admin user creation and privileges"""
        # Create admin user with unique credentials
        import time
        timestamp = int(time.time())
        unique_username = f"adminuser_{timestamp}"
        unique_email = f"admin_{timestamp}@example.com"
        
        # Create admin user
        result = create_user(unique_username, unique_email, "adminpass123", is_admin=True)
        self.assertTrue(result["success"])
        self.assertTrue(result["is_admin"])
        
        # Authenticate admin user
        auth_result = authenticate_user(unique_username, "adminpass123")
        self.assertTrue(auth_result["success"])
        self.assertTrue(auth_result["is_admin"])
    
    def test_session_cleanup(self):
        """Test session cleanup functionality"""
        # This test verifies that cleanup doesn't crash
        # In a real scenario, you'd need to create expired sessions
        try:
            cleanup_expired_sessions()
            # If we get here, cleanup didn't crash
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Session cleanup failed: {e}")

def run_tests():
    """Run all authentication tests"""
    print("🧪 Bills Tracker v3 - Authentication Tests")
    print("=" * 60)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAuthentication)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"  ❌ {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"  ❌ {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\n🎉 All tests passed!")
        return True
    else:
        print("\n❌ Some tests failed!")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1) 