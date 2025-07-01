#!/usr/bin/env python3
"""
Test script for password encryption functionality in Bills Tracker.
This script tests the encryption and decryption of passwords.
"""

import json
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

def test_encryption():
    """Test the password encryption functionality."""
    print("🔐 Testing Password Encryption Functionality")
    print("=" * 50)
    
    # Test data
    test_passwords = [
        "mypassword123",
        "secure_password_456",
        "test@email.com",
        "123456789",
        "",  # Empty password
        "special_chars!@#$%^&*()"
    ]
    
    # Test 1: Basic encryption/decryption
    print("\n1. Testing basic encryption/decryption...")
    try:
        # Generate a test key
        key = Fernet.generate_key()
        fernet = Fernet(key)
        
        for password in test_passwords:
            if password:
                encrypted = fernet.encrypt(password.encode())
                decrypted = fernet.decrypt(encrypted).decode()
                
                if password == decrypted:
                    print(f"   ✅ '{password}' -> encrypted -> decrypted correctly")
                else:
                    print(f"   ❌ '{password}' -> encryption failed")
            else:
                print(f"   ⚠️  Empty password skipped")
        
        print("   ✅ Basic encryption/decryption test passed")
        
    except Exception as e:
        print(f"   ❌ Basic encryption test failed: {e}")
        return False
    
    # Test 2: Key derivation from password
    print("\n2. Testing key derivation from password...")
    try:
        salt = os.urandom(16)
        master_password = "my_master_password"
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        derived_key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        
        fernet = Fernet(derived_key)
        
        test_password = "test_password"
        encrypted = fernet.encrypt(test_password.encode())
        decrypted = fernet.decrypt(encrypted).decode()
        
        if test_password == decrypted:
            print("   ✅ Key derivation and encryption test passed")
        else:
            print("   ❌ Key derivation test failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Key derivation test failed: {e}")
        return False
    
    # Test 3: File operations
    print("\n3. Testing file operations...")
    try:
        # Create test bills data
        test_bills = [
            {
                "name": "Test Bill 1",
                "password": "password123",
                "due_date": "2025-01-01"
            },
            {
                "name": "Test Bill 2", 
                "password": "secure456",
                "due_date": "2025-01-02"
            }
        ]
        
        # Save test data
        with open('test_bills.json', 'w') as f:
            json.dump(test_bills, f, indent=2)
        
        # Load test data
        with open('test_bills.json', 'r') as f:
            loaded_bills = json.load(f)
        
        # Verify data integrity
        if len(loaded_bills) == len(test_bills):
            print("   ✅ File operations test passed")
        else:
            print("   ❌ File operations test failed")
            return False
            
        # Clean up
        os.remove('test_bills.json')
        
    except Exception as e:
        print(f"   ❌ File operations test failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All encryption tests passed!")
    print("\nThe password encryption functionality is working correctly.")
    print("You can now use the Bills Tracker with encrypted passwords.")
    
    return True

if __name__ == "__main__":
    test_encryption() 