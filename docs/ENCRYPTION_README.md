# Password Encryption Feature

## Overview

The Bills Tracker application now includes **password encryption** using the Fernet symmetric encryption algorithm from the `cryptography` library. This ensures that all stored passwords are encrypted and secure.

## Features

### 🔐 Automatic Password Encryption
- All passwords are automatically encrypted when saved to disk
- Passwords are decrypted when displayed or edited
- Seamless integration with existing functionality
- Backward compatibility with existing plain text passwords

### 🔑 Key Management
- Automatic key generation on first use
- Secure key storage in `.encryption_key` file
- Salt-based key derivation for additional security
- Keys are automatically excluded from version control

### 🔄 Migration Support
- Existing plain text passwords are automatically migrated to encrypted format
- No data loss during migration
- Transparent to the user

## Installation

### Prerequisites
Install the required cryptography library:

```bash
pip install cryptography
```

### Automatic Setup
The encryption system is automatically initialized when you first run the application. No additional setup required.

## How It Works

### 1. Key Generation
On first run, the system generates:
- A random encryption key (`.encryption_key`)
- A random salt (`.salt`) for key derivation

### 2. Password Encryption
When saving bills or templates:
- Plain text passwords are encrypted using Fernet
- Encrypted passwords are stored in JSON files
- Original passwords are never stored in plain text

### 3. Password Decryption
When displaying or editing:
- Encrypted passwords are automatically decrypted
- Users see the original passwords during editing
- Passwords are displayed as asterisks for security

### 4. Migration Process
When loading existing data:
- System detects plain text passwords
- Automatically encrypts them
- Saves the encrypted versions
- Provides feedback about migration

## Security Features

### Encryption Algorithm
- **Fernet**: Symmetric encryption with authenticated encryption
- **Key Derivation**: PBKDF2 with SHA256 and 100,000 iterations
- **Salt**: 16-byte random salt for each key derivation

### File Security
- Encryption keys are stored in separate files
- Keys are excluded from version control (`.gitignore`)
- Backup files also contain encrypted passwords

### Data Protection
- Passwords are never logged or displayed in plain text
- Memory is cleared after decryption operations
- Graceful fallback if cryptography library is unavailable

## Usage

### Normal Operation
The encryption is completely transparent to users:

1. **Adding Bills**: Enter passwords normally - they're encrypted automatically
2. **Viewing Bills**: Passwords appear as asterisks (****)
3. **Editing Bills**: Original passwords are shown for editing
4. **Templates**: Passwords in templates are also encrypted

### Error Handling
If the cryptography library is not available:
- Application continues to work
- Passwords are stored in plain text
- Warning message is displayed
- No data loss occurs

## File Structure

```
Bills_tracker/
├── bills-tracker.py          # Main application
├── bills.json               # Encrypted bill data
├── bill_templates.json      # Encrypted template data
├── .encryption_key          # Encryption key (auto-generated)
├── .salt                    # Salt for key derivation (auto-generated)
├── .gitignore              # Excludes encryption files
└── test_encryption.py      # Test script for encryption
```

## Testing

Run the test script to verify encryption functionality:

```bash
python test_encryption.py
```

This will test:
- Basic encryption/decryption
- Key derivation from passwords
- File operations with encrypted data

## Troubleshooting

### Common Issues

1. **"cryptography library not available"**
   - Install: `pip install cryptography`
   - Application will work with plain text passwords

2. **"Failed to initialize encryption"**
   - Check file permissions
   - Ensure write access to application directory
   - Restart the application

3. **"Corrupted bills file"**
   - Restore from backup in `backups/` directory
   - Passwords will be re-encrypted automatically

### Recovery

If encryption keys are lost:
1. Delete `.encryption_key` and `.salt` files
2. Restart the application
3. New keys will be generated
4. Existing encrypted passwords will need to be re-entered

## Security Best Practices

1. **Keep encryption keys secure**
   - Don't share `.encryption_key` and `.salt` files
   - Back up these files securely
   - Don't commit them to version control

2. **Regular backups**
   - Backup both data files and encryption keys
   - Store backups in secure locations
   - Test backup restoration periodically

3. **System security**
   - Use strong system passwords
   - Keep the application directory secure
   - Regularly update the cryptography library

## Technical Details

### Encryption Process
```python
# Key derivation
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
)
key = base64.urlsafe_b64encode(kdf.derive(password.encode()))

# Encryption
fernet = Fernet(key)
encrypted = fernet.encrypt(plaintext.encode())
```

### File Format
Encrypted passwords are stored as base64-encoded Fernet tokens:
```
gAAAAA... (base64 encoded encrypted data)
```

### Migration Detection
Plain text passwords are detected by checking if they start with the Fernet token prefix (`gAAAAA`).

## Future Enhancements

- [ ] Master password protection
- [ ] Session timeout with re-authentication
- [ ] Secure backup encryption
- [ ] Multi-user support with individual keys
- [ ] Hardware key integration

---

**Note**: This encryption feature provides strong protection for stored passwords. However, it's important to maintain good security practices on the system level as well. 