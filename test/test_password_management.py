#!/usr/bin/env python3
"""
Test suite for Bills Tracker Password Management Features

This module tests the password management functionality including:
- Master password setup and verification
- Password change functionality
- Password reset and recovery
- Backup management
- Encryption and re-encryption
"""

import os
import sys
import json
import tempfile
import shutil
import hashlib
import time
from datetime import datetime
from unittest.mock import patch, MagicMock

# Add the parent directory to the path to import the main module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the main module functions
try:
    from bills_tracker import (
        set_master_password, verify_master_password, change_master_password,
        reset_master_password, show_password_recovery_options,
        export_bills_for_recovery, view_backup_files,
        re_encrypt_passwords_with_new_master, password_management_menu
    )
    # Import other necessary functions and classes
    from bills_tracker import (
        MASTER_PASSWORD_FILE, SALT_FILE, ENCRYPTION_KEY_FILE,
        BILLS_FILE, TEMPLATES_FILE, BACKUP_DIR
    )
except ImportError as e:
    print(f"Error importing bills_tracker module: {e}")
    print("Make sure you're running this from the correct directory")
    sys.exit(1)

class TestPasswordManagement:
    """Test class for password management features."""
    
    def setup_method(self):
        """Set up test environment before each test."""
        # Create temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Create necessary directories
        os.makedirs(BACKUP_DIR, exist_ok=True)
        
        # Mock global variables
        self.mock_bills = [
            {
                'name': 'Test Bill 1',
                'due_date': '2024-02-15',
                'password': 'test_password_1',
                'paid': False
            },
            {
                'name': 'Test Bill 2',
                'due_date': '2024-02-20',
                'password': 'test_password_2',
                'paid': True
            }
        ]
        
        self.mock_templates = [
            {
                'name': 'Test Template',
                'password': 'template_password',
                'billing_cycle': 'monthly'
            }
        ]
        
        # Mock the global bills and bill_templates
        import bills_tracker
        bills_tracker.bills = self.mock_bills
        bills_tracker.bill_templates = self.mock_templates
        
        # Mock cryptography availability
        bills_tracker.CRYPTOGRAPHY_AVAILABLE = True
        
        # Create mock encryption instance
        bills_tracker.password_encryption = MagicMock()
        bills_tracker.password_encryption.fernet = MagicMock()
        bills_tracker.password_encryption.derive_key_from_password = MagicMock(return_value=b'test_key')
        bills_tracker.password_encryption.generate_salt = MagicMock(return_value=b'test_salt')
    
    def teardown_method(self):
        """Clean up test environment after each test."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_set_master_password(self):
        """Test setting a new master password."""
        with patch('builtins.input', side_effect=['testpass123', 'testpass123']):
            with patch('getpass.getpass', side_effect=['testpass123', 'testpass123']):
                result = set_master_password()
                
                assert result == 'testpass123'
                assert os.path.exists(MASTER_PASSWORD_FILE)
                
                # Verify password file contains salt and hash
                with open(MASTER_PASSWORD_FILE, 'rb') as f:
                    data = f.read()
                    assert len(data) > 16  # Salt + hash
    
    def test_set_master_password_mismatch(self):
        """Test setting password with mismatched confirmation."""
        with patch('getpass.getpass', side_effect=['testpass123', 'differentpass']):
            with patch('builtins.input', side_effect=['testpass123', 'differentpass']):
                # This should raise an exception or handle the mismatch
                try:
                    result = set_master_password()
                    # If it doesn't raise an exception, it should retry
                    assert result is None or result == 'testpass123'
                except Exception:
                    # Expected behavior for password mismatch
                    pass
    
    def test_set_master_password_too_short(self):
        """Test setting password that's too short."""
        with patch('getpass.getpass', side_effect=['123', '123']):
            with patch('builtins.input', side_effect=['123', '123']):
                try:
                    result = set_master_password()
                    # Should handle short password gracefully
                    assert result is None or result == '123'
                except Exception:
                    # Expected behavior for short password
                    pass
    
    def test_verify_master_password_success(self):
        """Test successful password verification."""
        # First set a password
        with patch('getpass.getpass', side_effect=['testpass123', 'testpass123']):
            set_master_password()
        
        # Then verify it
        with patch('getpass.getpass', return_value='testpass123'):
            result = verify_master_password()
            assert result == 'testpass123'
    
    def test_verify_master_password_failure(self):
        """Test failed password verification."""
        # First set a password
        with patch('getpass.getpass', side_effect=['testpass123', 'testpass123']):
            set_master_password()
        
        # Then try to verify with wrong password
        with patch('getpass.getpass', return_value='wrongpass'):
            with patch('builtins.exit') as mock_exit:
                try:
                    result = verify_master_password()
                    # Should exit after 5 failed attempts
                    mock_exit.assert_called()
                except SystemExit:
                    # Expected behavior
                    pass
    
    def test_change_master_password(self):
        """Test changing master password."""
        # First set initial password
        with patch('getpass.getpass', side_effect=['oldpass123', 'oldpass123']):
            set_master_password()
        
        # Then change it
        with patch('getpass.getpass', side_effect=['oldpass123', 'newpass123', 'newpass123']):
            with patch('builtins.input', return_value=''):
                change_master_password()
                
                # Verify new password works
                with patch('getpass.getpass', return_value='newpass123'):
                    result = verify_master_password()
                    assert result == 'newpass123'
    
    def test_change_master_password_wrong_current(self):
        """Test changing password with wrong current password."""
        # First set initial password
        with patch('getpass.getpass', side_effect=['oldpass123', 'oldpass123']):
            set_master_password()
        
        # Then try to change with wrong current password
        with patch('getpass.getpass', side_effect=['wrongpass', 'wrongpass', 'wrongpass']):
            with patch('builtins.input', return_value=''):
                change_master_password()
                # Should handle gracefully without changing password
    
    def test_reset_master_password(self):
        """Test resetting master password."""
        # First set initial password
        with patch('getpass.getpass', side_effect=['oldpass123', 'oldpass123']):
            set_master_password()
        
        # Create some test data
        with open(BILLS_FILE, 'w') as f:
            json.dump(self.mock_bills, f)
        
        # Then reset password
        with patch('builtins.input', return_value='yes'):
            reset_master_password()
            
            # Verify password file is removed
            assert not os.path.exists(MASTER_PASSWORD_FILE)
            
            # Verify backup was created
            backup_dirs = [d for d in os.listdir('.') if d.startswith('password_reset_backup_')]
            assert len(backup_dirs) > 0
    
    def test_export_bills_for_recovery(self):
        """Test exporting bills for recovery."""
        # Create test bills file
        with open(BILLS_FILE, 'w') as f:
            json.dump(self.mock_bills, f)
        
        # Mock the export function
        with patch('builtins.input', return_value='test_export.csv'):
            with patch('builtins.open', create=True) as mock_open:
                mock_file = MagicMock()
                mock_open.return_value.__enter__.return_value = mock_file
                
                export_bills_for_recovery()
                
                # Verify CSV was written
                mock_file.write.assert_called()
    
    def test_view_backup_files(self):
        """Test viewing backup files."""
        # Create some test backup files
        test_backup = os.path.join(BACKUP_DIR, 'bills_backup_20240215_120000.json')
        with open(test_backup, 'w') as f:
            json.dump(self.mock_bills, f)
        
        # Mock the view function
        with patch('builtins.input', return_value='4'):  # Back option
            view_backup_files()
            # Should handle gracefully
    
    def test_re_encrypt_passwords_with_new_master(self):
        """Test re-encrypting passwords with new master password."""
        # Mock cryptography imports
        with patch('bills_tracker.Fernet') as mock_fernet:
            mock_fernet_instance = MagicMock()
            mock_fernet.return_value = mock_fernet_instance
            mock_fernet_instance.encrypt.return_value = b'encrypted_data'
            mock_fernet_instance.decrypt.return_value = b'decrypted_data'
            
            # Mock base64
            with patch('bills_tracker.base64') as mock_base64:
                mock_base64.urlsafe_b64decode.return_value = b'encrypted_bytes'
                mock_base64.urlsafe_b64encode.return_value = b'encoded_data'
                
                # Test re-encryption
                re_encrypt_passwords_with_new_master('oldpass', 'newpass')
                
                # Verify encryption was called
                mock_fernet_instance.encrypt.assert_called()
                mock_fernet_instance.decrypt.assert_called()
    
    def test_password_management_menu(self):
        """Test password management menu."""
        # Mock menu navigation
        with patch('builtins.input', return_value='6'):  # Back option
            password_management_menu()
            # Should handle gracefully
    
    def test_show_password_recovery_options(self):
        """Test showing password recovery options."""
        with patch('builtins.input', return_value=''):
            show_password_recovery_options()
            # Should display recovery information
    
    def test_backup_creation_during_password_change(self):
        """Test that backup is created during password change."""
        # First set initial password
        with patch('getpass.getpass', side_effect=['oldpass123', 'oldpass123']):
            set_master_password()
        
        # Then change password
        with patch('getpass.getpass', side_effect=['oldpass123', 'newpass123', 'newpass123']):
            with patch('builtins.input', return_value=''):
                change_master_password()
                
                # Verify backup was created
                backup_files = [f for f in os.listdir('.') if f.startswith('.master_password.backup.')]
                assert len(backup_files) > 0
    
    def test_encryption_file_management(self):
        """Test encryption file creation and management."""
        # Set password
        with patch('getpass.getpass', side_effect=['testpass123', 'testpass123']):
            set_master_password()
        
        # Verify encryption files exist
        assert os.path.exists(MASTER_PASSWORD_FILE)
        
        # Test that salt and key files are created when needed
        if os.path.exists(SALT_FILE):
            assert os.path.getsize(SALT_FILE) > 0
        
        if os.path.exists(ENCRYPTION_KEY_FILE):
            assert os.path.getsize(ENCRYPTION_KEY_FILE) > 0
    
    def test_password_hash_security(self):
        """Test that password hashing is secure."""
        # Set password
        with patch('getpass.getpass', side_effect=['testpass123', 'testpass123']):
            set_master_password()
        
        # Read password file
        with open(MASTER_PASSWORD_FILE, 'rb') as f:
            data = f.read()
        
        # Verify structure (salt + hash)
        assert len(data) == 16 + 32  # 16 bytes salt + 32 bytes hash
        
        # Verify hash is not plain text
        salt = data[:16]
        hash_value = data[16:]
        
        # Hash should not be the same as the password
        assert hash_value != b'testpass123'
        
        # Verify hash can be verified
        test_hash = hashlib.pbkdf2_hmac('sha256', 'testpass123'.encode(), salt, 100_000)
        assert test_hash == hash_value

def run_tests():
    """Run all password management tests."""
    print("🧪 Running Password Management Tests...")
    print("=" * 50)
    
    test_instance = TestPasswordManagement()
    test_methods = [method for method in dir(test_instance) if method.startswith('test_')]
    
    passed = 0
    failed = 0
    
    for method_name in test_methods:
        try:
            print(f"Testing {method_name}...", end=" ")
            test_instance.setup_method()
            getattr(test_instance, method_name)()
            test_instance.teardown_method()
            print("✅ PASSED")
            passed += 1
        except Exception as e:
            print(f"❌ FAILED: {e}")
            failed += 1
            try:
                test_instance.teardown_method()
            except:
                pass
    
    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All password management tests passed!")
        return True
    else:
        print("⚠️  Some tests failed. Please review the implementation.")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1) 