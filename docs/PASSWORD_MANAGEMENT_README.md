# Password Management Features

## Overview

Bills Tracker includes comprehensive password management features to ensure the security of your financial data while providing recovery options when needed.

## 🔑 Master Password System

### Initial Setup
- **First Launch**: When you first run Bills Tracker, you'll be prompted to set a master password
- **Requirements**: Minimum 6 characters
- **Storage**: Password is hashed using PBKDF2 with SHA-256 and stored securely
- **Protection**: Required to access the application

### Password Verification
- **Attempt Limits**: 5 attempts before application exit
- **Security**: Uses secure hashing with salt
- **Session**: Password is verified once per session

## 🔄 Change Master Password

### Features
- **Current Password Verification**: Must enter current password to change
- **New Password Validation**: Minimum 6 characters, must be different from current
- **Automatic Backup**: Creates backup of current password before changing
- **Re-encryption**: Automatically re-encrypts all bill passwords with new master password
- **Rollback Protection**: Can restore previous password if change fails

### Process
1. Access Password Management menu (Option 11)
2. Select "Change master password"
3. Enter current password (3 attempts allowed)
4. Enter new password and confirmation
5. System creates backup and updates password
6. All encrypted bill passwords are re-encrypted with new key

### Security Features
- **Backup Creation**: Automatic backup before password change
- **Verification**: Current password must be verified
- **Validation**: New password must meet requirements
- **Re-encryption**: All data re-encrypted with new key
- **Error Recovery**: Automatic rollback on failure

## 🔄 Reset Master Password

### Use Cases
- **Forgotten Password**: When you can't remember your master password
- **Security Breach**: If you suspect password compromise
- **Fresh Start**: Complete password reset for new security

### Process
1. Access Password Management menu
2. Select "Reset master password"
3. Confirm the action (destructive operation)
4. System creates comprehensive backup
5. Removes current password files
6. Prompts for new password on next startup

### Backup Strategy
- **Automatic Backup**: Creates timestamped backup directory
- **Complete Backup**: Includes all data files and configuration
- **File Preservation**: Backs up bills, templates, and encryption files
- **Recovery Ready**: Backup can be used to restore data

### Important Notes
- **Data Loss Risk**: Encrypted passwords may become inaccessible
- **Backup Essential**: Always create backup before reset
- **Manual Recovery**: May need to re-enter bill passwords
- **Fresh Start**: Application behaves like first-time setup

## 📋 Password Recovery Options

### Recovery Strategies
1. **Password Hints**: Check for written password hints
2. **Common Passwords**: Try passwords you commonly use
3. **Password Reset**: Use reset function if you have access
4. **Backup Restoration**: Restore from previous backup

### Available Tools
- **Password Reset**: Remove current password and set new one
- **Data Export**: Export bills to CSV (decrypted)
- **Backup Management**: View and restore from backups
- **Recovery Guidance**: Step-by-step recovery instructions

### Security Recommendations
- **Strong Passwords**: Use complex, memorable passwords
- **Password Manager**: Consider using a password manager
- **Password Hints**: Write down hints (not the password)
- **Regular Backups**: Create backups frequently
- **Secure Storage**: Store backups in secure location

## 📤 Export for Recovery

### Purpose
- **Data Preservation**: Export all bills in readable format
- **Password Recovery**: Access data even if master password is lost
- **Migration**: Move data to other applications
- **Backup**: Additional backup in CSV format

### Features
- **Decrypted Export**: All passwords are decrypted in export
- **Complete Data**: Includes all bill information
- **CSV Format**: Standard format for data portability
- **Timestamped Files**: Automatic file naming with timestamps

### Security Warning
⚠️ **Important**: Exported files contain decrypted passwords. Keep these files secure and delete them after recovery.

### Export Contents
- Bill names and due dates
- Payment status and billing cycles
- Website URLs and login information
- **Decrypted passwords** (security risk)
- Contact information and account numbers
- All custom fields and notes

## 📁 Backup Management

### Backup Types
1. **Automatic Backups**: Created before each save operation
2. **Password Reset Backups**: Created before password reset
3. **Manual Backups**: User-created backups
4. **Recovery Backups**: Created before data restoration

### Backup Locations
- **Bills Backups**: `backups/` directory
- **Password Reset Backups**: `password_reset_backup_YYYYMMDD_HHMMSS/`
- **Recovery Backups**: Root directory with timestamp

### Backup Management Features
- **View Contents**: See what's in each backup
- **Restore Data**: Restore bills from backup
- **Delete Backups**: Remove old backup files
- **Backup Information**: Size, date, and type details

### Backup Operations
1. **View Backups**: List all available backup files
2. **View Contents**: See bills contained in backup
3. **Restore**: Overwrite current data with backup
4. **Delete**: Remove backup files to save space

## 🔐 Encryption System

### Bill Password Encryption
- **Fernet Algorithm**: Industry-standard encryption
- **Master Password Derived**: Encryption key derived from master password
- **Salt Protection**: Unique salt for each installation
- **Automatic Migration**: Plain text passwords automatically encrypted

### Re-encryption Process
When master password is changed:
1. **Decrypt**: All passwords decrypted with old key
2. **Re-encrypt**: Passwords encrypted with new key
3. **Update Files**: New salt and key files saved
4. **Preserve Data**: All data remains accessible

### Encryption Files
- **`.master_password`**: Hashed master password
- **`.encryption_key`**: Derived encryption key
- **`.salt`**: Salt for key derivation
- **`bills.json`**: Encrypted bill data
- **`bill_templates.json`**: Encrypted template data

## 🛡️ Security Best Practices

### Password Security
- **Strong Passwords**: Use complex passwords with mixed characters
- **Unique Passwords**: Don't reuse passwords from other accounts
- **Regular Changes**: Change master password periodically
- **Secure Storage**: Don't write down passwords in plain text

### Data Protection
- **Regular Backups**: Create backups before major changes
- **Secure Backups**: Store backups in secure location
- **Encryption**: Keep encryption files secure
- **Access Control**: Limit access to application directory

### Recovery Planning
- **Multiple Backups**: Keep several backup copies
- **Off-site Storage**: Store backups in different locations
- **Test Recovery**: Periodically test backup restoration
- **Documentation**: Keep recovery procedures documented

## 🚨 Emergency Procedures

### Forgotten Master Password
1. **Don't Panic**: Data is likely recoverable
2. **Check Backups**: Look for recent backup files
3. **Export Data**: Use recovery export if possible
4. **Password Reset**: Use reset function if you have access
5. **Manual Recovery**: Restore from backup files

### Corrupted Data
1. **Stop Using**: Don't continue using corrupted data
2. **Find Backup**: Locate most recent working backup
3. **Restore Data**: Use backup restoration feature
4. **Verify Data**: Check that restoration was successful
5. **Create New Backup**: Make fresh backup after restoration

### Security Breach
1. **Change Password**: Immediately change master password
2. **Check Access**: Review recent access logs
3. **Export Data**: Create secure export of data
4. **Reset System**: Consider complete password reset
5. **Monitor**: Watch for suspicious activity

## 📞 Support and Troubleshooting

### Common Issues
- **Password Not Accepted**: Check caps lock and keyboard layout
- **Encryption Errors**: May need to reset encryption keys
- **Backup Failures**: Check disk space and permissions
- **Import Problems**: Verify CSV format and encoding

### Recovery Steps
1. **Identify Problem**: Determine what went wrong
2. **Check Backups**: Look for recent backup files
3. **Try Recovery**: Use built-in recovery tools
4. **Manual Fix**: Edit files manually if necessary
5. **Prevent Future**: Implement better backup strategy

### Getting Help
- **Documentation**: Review this guide thoroughly
- **Backup Files**: Check for automatic backups
- **Export Data**: Use recovery export feature
- **Fresh Start**: Reset password and start over if needed

## 🔄 Future Enhancements

### Planned Features
- **Two-Factor Authentication**: Additional security layer
- **Password Strength Requirements**: Enforce stronger passwords
- **Audit Logging**: Track access and changes
- **Cloud Backup**: Automatic cloud storage integration
- **Biometric Authentication**: Fingerprint/face recognition

### Security Improvements
- **Hardware Security**: TPM integration
- **Encrypted Communication**: Secure data transmission
- **Access Logs**: Detailed security audit trails
- **Remote Wipe**: Secure data removal capabilities

---

*This documentation is updated as new password management features are added to Bills Tracker.* 