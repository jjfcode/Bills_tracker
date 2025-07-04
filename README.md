# Bills Tracker 🏠💳

A comprehensive bill management system with both **command-line (v2)** and **desktop GUI (v3)** versions. Features include flexible billing cycles, custom reminder periods, bill templates, contact information management, CSV import/export, search, sorting, pagination, colored output, automatic backups, data compression, and a modern category system.

## 🚀 **Two Versions Available**

### 📱 **Desktop GUI Version (v3)** - *Recommended*
- **Modern GUI** built with CustomTkinter
- **Category System** with visual organization
- **Smart Checkbox System** for bill payment tracking
- **Advanced Search & Filtering**
- **Export/Import functionality**
- **Automatic next cycle generation**

**[→ Go to Desktop Version (v3)](Bills_tracker_v3/README.md)**

### 💻 **Command-Line Version (v2)** - *Legacy*
- **Console-based interface**
- **Advanced features** like data compression and encryption
- **Bill templates** and contact management
- **CSV import/export** with validation
- **Comprehensive search** and sorting

**[→ Go to Command-Line Version (v2)](src/README.md)**

## ✨ Features

### Core Functionality
- **Add Bills** - Create new bills with name, due date, website, login info, password, custom billing cycles, and comprehensive contact information
- **View Bills** - Display all bills with color-coded status, due date information, contact details, and pagination
- **Edit Bills** - Modify existing bill information including billing cycles, reminder periods, and contact details
- **Delete Bills** - Remove bills with confirmation
- **Pay Bills** - Mark bills as paid and automatically update due dates based on billing cycles
- **🗄️ SQLite Database** - Fast and reliable data storage with SQLite database for better performance and data integrity
- **Password Encryption** - All stored passwords are encrypted using the Fernet algorithm for enhanced security
- **Master Password Protection** - Application access is protected by a master password with secure hash storage
- **Session Timeout/Auto-Exit** - The app automatically exits after 15 minutes of inactivity for enhanced security (improved with input-based checking)
- **🗜️ Data Compression** - Compress large datasets, backups, and exports to save space and optimize performance (GZIP, LZMA, ZLIB)
- **Bill Categories** - Assign a category (utilities, subscriptions, loans, insurance, etc.) to each bill for better organization
- **Payment Methods** - Track how bills are paid (auto-pay, manual, credit card, bank transfer, etc.) for payment pattern analysis

### Advanced Date Management
- **🔄 Flexible Billing Cycles** - Support for weekly, bi-weekly, monthly, quarterly, semi-annual, annual, and one-time bills
- **⏰ Custom Reminder Periods** - Set individual reminder periods (1-365 days) for each bill
- **📅 Smart Due Date Tracking** - Automatic detection based on custom reminder windows
- **🗓️ Calendar Integration** - View upcoming bills in calendar format
- **🚨 Overdue Tracking** - Highlight overdue bills with urgency indicators

### Bill Templates & Quick Actions
- **📋 Bill Templates** - Save and reuse bill configurations for quick bill creation
- **💾 Save as Template** - Convert existing bills into reusable templates
- **🚀 Quick Bill Creation** - Use templates to add bills with minimal input (just due date)
- **✏️ Template Management** - Edit, delete, and organize templates
- **📝 Manual Template Creation** - Create templates from scratch with all details

### Contact Information Management
- **📧 Customer Service Email** - Store company support email addresses
- **📞 Support Phone Numbers** - Separate support and billing phone numbers
- **🕒 Service Hours** - Track customer service availability
- **🆔 Account Information** - Store account numbers and reference IDs
- **💬 Live Chat Support** - URLs for online chat support
- **📱 Mobile App Information** - Details about mobile applications
- **🔍 Contact Search** - Search bills by contact information

### CSV Import/Export System
- **📥 Bulk Import** - Import multiple bills from CSV files with validation
- **📤 Data Export** - Export all bills to CSV format for backup and analysis
- **📋 Sample Templates** - Generate sample CSV files with correct format
- **✅ Comprehensive Validation** - URL, email, date, and billing cycle validation
- **🔄 Duplicate Detection** - Prevent importing duplicate bills
- **📊 Import Reports** - Detailed feedback on import success and errors

### Search & Organization
- **🔍 Smart Search** - Search bills by name, due date, website, contact information, or across all fields with pagination
- **🔄 Flexible Sorting** - Sort by due date, name, payment status, billing cycle (ascending/descending)
- **📄 Pagination** - Handle large numbers of bills efficiently with configurable page sizes
- **🎯 Smart Filtering** - Filter bills based on custom reminder periods or specific day ranges
- **💡 Auto-complete** - Smart suggestions while typing bill names and websites

### Bill Templates

**Template Features:**
- **Save Existing Bills** - Convert any bill into a reusable template
- **Manual Creation** - Create templates from scratch with all details
- **Quick Bill Creation** - Use templates to add bills with just a due date
- **Template Management** - Edit, delete, and organize templates
- **Duplicate Prevention** - Templates with same names are overwritten with confirmation

**Template Information:**
- **Name** - Template name (required)
- **Billing cycle** - Recurring pattern for bills created from template
- **Reminder period** - Default reminder days for new bills
- **Website & Login** - Pre-filled account information
- **Contact details** - All customer service information
- **No due dates** - Templates don't include due dates (set when creating bills)

**Using Templates:**
1. Choose "Bill templates" from main menu
2. Select "Use template to add bill"
3. Choose template from list
4. Enter only the due date
5. Bill is created with all template details automatically

### Contact Information Management

**Comprehensive Contact Details:**
- **Customer Service Email** - Primary contact email with validation
- **Support Phone** - General customer support number
- **Billing Phone** - Dedicated billing department number
- **Service Hours** - When customer service is available
- **Account Number** - Your unique account identifier
- **Reference ID** - Policy number or reference code
- **Live Chat URL** - Online chat support link with validation
- **Mobile App** - Mobile application details and platforms

**Contact Features:**
- **Search by Contact** - Find bills using any contact information
- **Validation** - Email and URL format validation
- **Display Integration** - Contact info shown in bill listings
- **Quick Access** - Easy access to support information
- **Comprehensive Storage** - All customer service details in one place

### CSV Import/Export System

**Import Features:**
- **Bulk Import** - Add multiple bills at once from CSV files
- **Format Validation** - Automatic validation of CSV structure
- **Data Validation** - URL, email, date, and billing cycle validation
- **Duplicate Detection** - Prevents importing duplicate bill names
- **Error Reporting** - Detailed feedback on import success and issues
- **Sample Templates** - Generate sample CSV files with correct format

**Export Features:**
- **Complete Export** - Export all bills with all fields to CSV
- **Timestamped Files** - Automatic filename generation with timestamps
- **Data Portability** - Easy backup and migration to other systems
- **Analysis Ready** - CSV format compatible with Excel, Google Sheets, etc.

**CSV Format Requirements:**
- **Required Columns**: name, due_date
- **Optional Columns**: billing_cycle, reminder_days, web_page, login_info, password, company_email, support_phone, billing_phone, customer_service_hours, account_number, reference_id, support_chat_url, mobile_app
- **Date Format**: YYYY-MM-DD
- **Headers**: Case-insensitive column names

**Import Process:**
1. Prepare CSV file with correct format
2. Choose "CSV Import/Export" from main menu
3. Select "Import bills from CSV"
4. Enter file path
5. Review validation results
6. Confirm import

**Export Process:**
1. Choose "CSV Import/Export" from main menu
2. Select "Export bills to CSV"
3. Enter filename (or use default)
4. Confirm export
5. File saved with all bill data

### Sorting & Organization
- **📅 Sort by due date** - Earliest or latest first with urgency indicators
- **🔤 Sort by name** - Alphabetical (A-Z or Z-A) 
- **✅ Sort by payment status** - Paid or unpaid first
- **🔄 Sort by billing cycle** - Group by cycle type (weekly, monthly, etc.)
- **⚡ Multi-level sorting** - Combine multiple sort criteria
- **📄 Reset to original order** - Restore file order

**Enhanced Features:**
- **Pagination** - Handle large sorted lists efficiently  
- **Save Order** - Permanently save current sort preferences
- **Visual Indicators** - Clear display of overdue and due-soon bills
- **Context Information** - Show days until due and billing cycle info

### Due Bills Monitoring

**Enhanced Due Bills System:**
- **Custom Reminder Periods** - Each bill uses its own reminder window
- **Specific Day Checking** - Traditional "bills due in X days" view
- **Smart Detection** - Bills appear based on individual reminder settings
- **Calendar View** - See upcoming bills in organized weekly format

**Status Indicators:**
- 🚨 **OVERDUE** - Past due date (red, urgent action required)
- 🔥 **DUE TODAY** - Bills due on current date (yellow, high priority)  
- ⚠️ **Due in 1-3 days** - Immediate attention needed (yellow)
- 📅 **Due within reminder period** - Plan ahead (cyan)
- ⏰ **Reminder info** - Shows custom reminder period for each bill

### Pagination System

**Automatic Pagination:**
- **Smart Threshold** - Automatically enabled when more than 10 items
- **Configurable Page Size** - Adjust number of items per page
- **Navigation Controls** - Easy browsing with numbered pages
- **Page Information** - Shows current page, total pages, and item count

**Navigation Options:**
- **Next/Previous** - Browse through pages sequentially
- **Jump to Page** - Go directly to specific page number
- **First/Last** - Quick access to beginning or end
- **Back to Menu** - Return to previous menu at any time

### Bill Status & Information Display

**Comprehensive Bill Information:**
- **Payment Status** - ✓ Paid (green) / ○ Unpaid (yellow) / ! OVERDUE (red)
- **Due Date** - With days until due and urgency coloring
- **Billing Cycle** - Color-coded cycle type (weekly, monthly, etc.)
- **Reminder Period** - ⏰ Custom reminder setting display
- **Website & Login** - Quick access to account information
- **Urgency Indicators** - Visual priority based on due date proximity

### Enhanced Input Validation

**Smart URL Correction:**
- Automatically adds missing protocols (http/https)
- Validates domain structure and format
- Corrects common input mistakes
- Example: `google.com` → `https://google.com`

**Email Format Validation:**
- Comprehensive email format checking
- Supports international domains and complex addresses
- Clear error messages for invalid formats
- Example: Accepts `user.name+tag@company.co.uk`

**Date Range Protection:**
- Prevents dates more than 1 year in the past
- Warns about dates more than 5 years in the future
- Validates actual date existence (no Feb 30th)
- Maintains data quality and prevents obvious errors

**Reminder Period Limits:**
- Enforces 1-365 day range for reminder periods
- Prevents unrealistic reminder settings
- Provides default values for convenience
- Ensures practical notification timing

**Interactive Error Handling:**
- User-friendly error messages with suggestions
- Option to cancel operations at any time
- Automatic retry prompts for invalid input
- Visual feedback with color-coded responses

### Data Compression System
- **🗜️ Data Compression Menu** - Option 13 in the main menu for all compression features
- **Database Compression** - Compress the SQLite database file with backup and analysis
- **Backup Compression** - Compress all files in the backup directory
- **Individual File Compression** - Compress any file or batch of files
- **Compression Analysis** - Find the best compression method for your data
- **Decompression** - Restore compressed files to their original format
- **Progress Tracking** - Visual progress indicators for large operations
- **Safe Operations** - Backups and integrity checks for all compression actions

See [docs/DATA_COMPRESSION_README.md](docs/DATA_COMPRESSION_README.md) for full details and usage examples.

### Demo & Test Scripts
- **Demo**: `python demo/demo_compression.py` - Demonstrates all compression features
- **Test**: `python test/test_compression.py` - Runs comprehensive tests for compression

### Bill Categories

- **Assign Categories**: When adding or editing a bill, select a category (utilities, subscriptions, loans, insurance, credit cards, rent/mortgage, entertainment, transportation, healthcare, education, business, other)
- **View by Category**: Use the "Bill Categories" menu to view bills grouped by category
- **Sort by Category**: Sort bills A-Z or Z-A by category from the sort menu or Bill Categories menu
- **Search by Category**: Find all bills in a specific category
- **Category Statistics**: See totals, paid/unpaid/overdue counts, and percentages for each category
- **Category Summary**: Quick overview of all categories and their descriptions
- **Auto-Migration**: Existing bills are automatically assigned a default category ("other") if missing

**Menu Integration:**
- Main menu option: "Bill Categories" (view, sort, search, stats)
- Category selection is part of bill creation and editing
- All bill views and exports now display category information

**Example Categories:**
- Utilities, Subscriptions, Loans, Insurance, Credit Cards, Rent/Mortgage, Entertainment, Transportation, Healthcare, Education, Business, Other

### Payment Methods

- **Assign Payment Methods**: When adding or editing a bill, select a payment method (auto-pay, manual, credit card, bank transfer, check, cash, PayPal, Venmo, Zelle, Apple Pay, Google Pay, other)
- **View by Payment Method**: Use the "Payment Methods" menu to view bills grouped by payment method
- **Sort by Payment Method**: Sort bills A-Z or Z-A by payment method from the sort menu or Payment Methods menu
- **Search by Payment Method**: Find all bills using a specific payment method
- **Payment Method Statistics**: See totals, paid/unpaid/overdue counts, and percentages for each payment method
- **Payment Method Summary**: Quick overview of all payment methods and their descriptions
- **Auto-Migration**: Existing bills are automatically assigned a default payment method ("manual") if missing

**Menu Integration:**
- Main menu option: "Payment Methods" (view, sort, search, stats)
- Payment method selection is part of bill creation and editing
- All bill views and exports now display payment method information

**Example Payment Methods:**
- Auto-Pay, Manual, Credit Card, Bank Transfer, Check, Cash, PayPal, Venmo, Zelle, Apple Pay, Google Pay, Other

## 📂 File Structure

```
Bills_tracker/
├── bills-tracker.py                    # Main application file with all features
├── bills.json                         # Bills data storage (auto-created)
├── bill_templates.json                # Bill templates storage (auto-created)
├── backups/                           # Automatic backup directory
│   ├── bills_backup_20250629_143022.json
│   ├── bills_backup_20250629_143045.json
│   └── ... (up to 5 most recent backups)
├── .encryption_key                    # Encryption key for password encryption (auto-generated)
├── .salt                              # Salt for key derivation (auto-generated)
├── .master_password                   # Master password hash and salt (auto-generated)
├── docs/                              # Documentation and implementation guides
│   ├── README.md                      # Documentation organization guide
│   ├── BILLING_CYCLES_IMPLEMENTATION.md   # Billing cycles feature documentation
│   ├── CUSTOM_REMINDERS_IMPLEMENTATION.md # Custom reminder periods documentation
│   ├── ENCRYPTION_README.md           # Password encryption and security guide
│   ├── PASSWORD_MANAGEMENT_README.md  # Password management and recovery guide
│   ├── organization_summary.txt       # Code organization overview
│   └── autocomplete_implementation_summary.txt # Auto-complete feature summary
├── demo/                              # Demonstration scripts
│   ├── README.md                      # Demo scripts documentation
│   ├── demo_flexible_billing.py       # Billing cycles demonstration script
│   ├── demo_custom_reminders.py      # Custom reminders demonstration script
│   ├── demo_compression.py            # Data compression demonstration script
│   └── demo_enhanced_validation.py   # Enhanced validation features demonstration
├── test/                              # Test scripts
│   ├── README.md                      # Test scripts documentation
│   ├── test_billing_cycles.py        # Billing cycles testing script
│   ├── test_edge_cases.py            # Date handling edge cases testing
│   ├── test_menu_options.py          # Menu options functionality testing
│   ├── test_validation.py            # Validation functions testing script
│   ├── test_autocomplete.py          # Auto-complete functionality testing
│   ├── test_encryption.py            # Password encryption testing
│   ├── test_password_management.py   # Password management functionality testing
│   └── test_compression.py           # Data compression test script
├── README.md                          # This comprehensive documentation
├── Future_Update.md                   # Planned enhancements and roadmap
└── .gitignore                        # Git ignore file
```

## 💾 Advanced Backup System

**Automatic Backups:**
- Created before every save operation with progress indicators
- Timestamped filename format: `bills_backup_YYYYMMDD_HHMMSS.json`
- Stored in `backups/` directory with automatic organization
- Automatic retention: keeps only 5 most recent backups
- Older backups are automatically deleted with cleanup notifications

**Backup Features:**
- ✅ Automatic creation on data changes with progress tracking
- ✅ Timestamped for easy identification and recovery
- ✅ Space management with automatic cleanup and notifications
- ✅ Error handling for backup failures with recovery options
- ✅ Progress bars for backup operations and cleanup
- ✅ Includes all new features (billing cycles, reminder periods)

**Backup Process:**
1. 🔍 Check directories and create backup folder if needed
2. 💾 Create timestamped backup with progress indicator
3. 🧹 Clean up old backups (keep 5 most recent)
4. ✅ Confirm successful backup creation
5. 💽 Save current data with validation

## 🛡️ Data Safety & Validation Features

### Input Validation
- **Date Format Validation** - Ensures proper YYYY-MM-DD format with comprehensive checking
- **Duplicate Prevention** - Stops duplicate bill names with case-insensitive detection
- **Billing Cycle Validation** - Validates cycle selection from supported options
- **Reminder Period Validation** - Ensures reminder days are within 1-365 range
- **URL Validation** - Automatic URL correction and format validation (e.g., 'google.com' → 'https://google.com')
- **Email Format Validation** - Proper email format checking with helpful error messages
- **Date Range Validation** - Prevents unrealistic dates (too far in past/future)
- **Reminder Period Validation** - Ensures reminder days are within reasonable range (1-365 days)
- **Cancel Operations** - Safe abort at any time during data entry

### Data Integrity
- **Automatic Migration** - Seamless upgrade of existing data with new features
- **Backward Compatibility** - Existing bills work without modification
- **Default Value Assignment** - Missing fields get sensible defaults (7-day reminders)
- **Error Recovery** - Graceful handling of corrupted files with backup restoration
- **Data Structure Validation** - Ensures all required fields are present

### Security Features
- **Master Password Protection** - Application access requires a master password with secure PBKDF2 hash storage
- **Password Encryption** - All passwords are encrypted using the Fernet algorithm from the `cryptography` library
- **Automatic Migration** - Existing plain text passwords are automatically encrypted on first load
- **Key Management** - Encryption keys are generated and stored in `.encryption_key` and `.salt` files (excluded from git)
- **Access Control** - 5-attempt limit for master password entry with automatic lockout
- **Session Timeout/Auto-Exit** - The app automatically exits after 15 minutes of inactivity for enhanced security
- **Password Management** - Change master password, reset functionality, and comprehensive recovery options
- **Secure Recovery** - Export data for recovery while maintaining security, backup management and restoration
- **Re-encryption** - Automatically re-encrypts all bill passwords when master password changes
- **Local Data Storage** - All data stays on your computer
- **No External Dependencies** - Minimal risk from third-party libraries
- **Backup Redundancy** - Multiple backup copies prevent data loss
- **Read-Only Backups** - Backup files are preserved from accidental modification
- **Input Sanitization** - Prevents malicious input from causing issues

See [ENCRYPTION_README.md](ENCRYPTION_README.md) for full details on encryption, key management, and recovery.

### Password Management System

**Comprehensive Password Management:**
- **Change Master Password** - Update master password with current password verification
- **Password Reset** - Complete password reset for forgotten passwords or security breaches
- **Recovery Options** - Step-by-step guidance for password recovery scenarios
- **Data Export** - Export bills to CSV with decrypted passwords for recovery
- **Backup Management** - View, restore, and manage backup files for data recovery

**Security Features:**
- **Current Password Verification** - Must enter current password to change it
- **Automatic Backup** - Creates backup before any password changes
- **Re-encryption** - All bill passwords automatically re-encrypted with new master password
- **Rollback Protection** - Can restore previous password if change fails
- **Comprehensive Backup** - Complete backup of all data before password reset

**Recovery Tools:**
- **Password Reset** - Remove current password and set new one
- **Data Export** - Export all bills to CSV (decrypted for recovery)
- **Backup Restoration** - Restore data from previous backups
- **Recovery Guidance** - Detailed instructions for various recovery scenarios

See [docs/PASSWORD_MANAGEMENT_README.md](docs/PASSWORD_MANAGEMENT_README.md) for comprehensive password management documentation.

## 🔧 Advanced Features Details

### Billing Cycle Management
- **7 Supported Cycles** - Weekly, bi-weekly, monthly, quarterly, semi-annual, annual, one-time
- **Smart Date Arithmetic** - Proper handling of month-end dates and leap years
- **Color-Coded Display** - Different colors for different cycle types
- **Automatic Advancement** - Due dates update correctly when bills are paid
- **Edge Case Handling** - January 31 + 1 month = February 28/29 (properly handled)

### Custom Reminder System
- **Individual Settings** - Each bill can have its own reminder period
- **Flexible Range** - 1 to 365 days supported
- **Smart Defaults** - New bills default to 7 days, existing bills migrated automatically
- **Custom vs. Fixed** - Choose between custom reminders or traditional fixed-day checking
- **Visual Indicators** - Clear display of reminder settings for each bill

### Pagination & Performance
- **Automatic Activation** - Kicks in when more than 10 items to display
- **Configurable Size** - Adjust items per page based on preference
- **Efficient Navigation** - Jump to specific pages or browse sequentially
- **Search Pagination** - Works with search results and filtered views
- **Memory Efficient** - Handles large numbers of bills without performance issues

### Enhanced Search & Sorting
- **Multi-Field Search** - Search across name, date, website, or all fields
- **Flexible Date Search** - Find by exact date, month/year, or year
- **Paginated Results** - Large search results handled efficiently
- **Multi-Level Sorting** - Combine multiple sort criteria
- **Persistent Preferences** - Save and restore sort order preferences

## 🐛 Troubleshooting

### Installation Issues

**"ModuleNotFoundError: No module named 'colorama'"**
```bash
pip install colorama tqdm
```

**"pip: command not found"**
```bash
# On Windows, try:
python -m pip install colorama tqdm

# On macOS/Linux, ensure pip is installed:
sudo apt-get install python3-pip  # Ubuntu/Debian
brew install python3              # macOS with Homebrew
```

### Display Issues

**Colors not displaying properly:**
- **Windows**: The app automatically initializes colorama for Windows compatibility
- **Terminal Issues**: Try using Windows Terminal, Command Prompt, or PowerShell
- **Legacy Systems**: Update your terminal or command prompt for best results

**Screen not clearing properly:**
- **Windows**: Uses `cls` command - ensure command prompt supports it
- **Linux/Mac**: Uses `clear` command - should work on all standard terminals
- **Workaround**: Manually scroll up if clear doesn't work

**Pagination not working:**
- Check that your terminal window is large enough
- Ensure terminal supports cursor positioning
- Try resizing terminal window and restarting application

### Data Issues

**"Invalid date format" errors:**
- Use YYYY-MM-DD format exactly (e.g., 2025-07-15)
- Ensure month and day have leading zeros: 2025-07-05, not 2025-7-5
- Verify the date exists: February 30th is invalid

**Billing cycle issues:**
- Choose from the numbered menu options (1-7)
- If cycles seem wrong, check the due date calculation in bill details
- One-time bills won't advance dates when paid (this is correct behavior)

**Reminder periods not working:**
- Ensure reminder days are between 1-365
- Check that bills show "⏰ X days before" in bill display
- Use "Custom reminder periods" option in due bills menu

### Performance Issues

**Application runs slowly:**
- Large number of bills (100+) may cause slower pagination
- Consider cleaning up old, unnecessary bills
- Backup files are automatically managed (only 5 kept)

**Backup creation errors:**
- Check write permissions in the application directory
- Ensure sufficient disk space for backup files
- Backup directory will be created automatically if missing

**Memory issues with large datasets:**
- Pagination helps manage large bill lists
- Consider archiving very old bills to separate files
- Application is optimized for typical household bill counts (10-50 bills)

### File & Data Issues

**Bills.json file corrupted:**
- Application will automatically create a new empty file
- Restore from recent backup in `backups/` directory
- Choose the most recent backup file and rename it to `bills.json`

**Migration issues:**
- If bills don't show reminder periods, restart the application
- Migration happens automatically on first load after update
- Check that bills display "⏰ 7 days before" for migrated bills

**Search not finding bills:**
- Search is case-insensitive but requires partial matches
- Try searching with shorter terms or single words
- Use "Search all fields" option for broader results

### Error Messages Guide

**Critical Errors:**
- **❌ "This field is required"** - Enter a value or type 'cancel' to abort
- **❌ "Invalid date format"** - Use YYYY-MM-DD format exactly
- **❌ "Bill already exists"** - Choose a different name (case-insensitive check)
- **❌ "Invalid billing cycle selection"** - Choose a number from 1-7

**Warnings:**
- **⚠️ "No bills found"** - Add bills first before other operations
- **⚠️ "No search results"** - Try different search terms or broader criteria
- **⚠️ "No bills due"** - No bills match current reminder criteria (normal)

**Information Messages:**
- **ℹ️ "Starting with empty bills list"** - No existing data file found (normal for first run)
- **ℹ️ "Bills migrated to include..."** - Automatic upgrade successful (one-time message)
- **ℹ️ "Using pagination for large dataset"** - Normal behavior for 10+ items

### Recovery Procedures

**Complete Data Loss:**
1. Check `backups/` folder for recent backup files
2. Copy most recent backup: `cp backups/bills_backup_YYYYMMDD_HHMMSS.json bills.json`
3. Restart the application to load recovered data
4. Verify all bills and settings are correct

**Partial Data Corruption:**
1. Application will attempt automatic recovery
2. Check if some bills loaded correctly
3. Compare with backup files if needed
4. Manually edit `bills.json` if you're comfortable with JSON format

**Feature Not Working:**
1. Restart the application completely
2. Check that you're using the latest version
3. Verify all required libraries are installed: `pip list | grep colorama`
4. Try running with a fresh `bills.json` file to test functionality

## 🚀 Future Enhancements

See [Future_Update.md](Future_Update.md) for comprehensive planned improvements.

### ✅ Phase 1 Completed Features
- [x] **Search functionality** - ✅ Multi-field search with pagination
- [x] **Sort options** - ✅ Multi-level sorting with persistence  
- [x] **Colored output** - ✅ Comprehensive color coding system
- [x] **Progress indicators** - ✅ Loading bars for operations
- [x] **Pagination** - ✅ Efficient handling of large datasets
- [x] **Flexible billing cycles** - ✅ 7 different cycle types supported
- [x] **Smart date updates** - ✅ Proper month/year handling
- [x] **Custom reminder periods** - ✅ Individual bill reminder settings
- [x] **Overdue tracking** - ✅ Color-coded urgency indicators
- [x] **Calendar integration** - ✅ Weekly calendar view of upcoming bills

### 🔄 Phase 2 In Development
- [ ] **Better validation** - Enhanced URL, email, and range validation
- [ ] **Auto-complete** - Smart suggestions while typing
- [ ] **Templates** - Save bill templates for quick adding
- [ ] **Bulk import** - Import bills from CSV files

### 🛡️ Phase 3 Security & Data (High Priority)
- [x] **Password encryption** - Encrypt stored passwords using Fernet
- [x] **Master password** - Require password to access application
- [ ] **Secure backups** - Encrypt backup files
- [ ] **Database migration** - Move from JSON to SQLite for better performance
- [ ] **Import/Export** - Support CSV, Excel formats

### 📊 Phase 4 Advanced Features (Medium Priority)
- [ ] **Bill categories** - Organize by type (utilities, subscriptions, etc.)
- [ ] **Bill amount tracking** - Track costs and spending patterns
- [ ] **Email notifications** - Automated bill reminders
- [ ] **Desktop notifications** - Pop-up reminders using plyer
- [ ] **Monthly reports** - Generate spending summaries
- [ ] **Visual charts** - Generate graphs using matplotlib

### 🖥️ Phase 5 Interface Enhancements (Future)
- [ ] **Rich CLI interface** - Beautiful tables and enhanced displays
- [ ] **GUI interface** - Desktop application with tkinter/customtkinter
- [ ] **Web interface** - Browser-based access with Flask/Django
- [ ] **Mobile app** - Cross-platform mobile application
- [ ] **Cloud sync** - Multi-device synchronization

### 🌐 Phase 6 Integration & Cloud (Long-term)
- [ ] **Google Calendar sync** - Add due dates to calendar
- [ ] **Cloud backup** - Google Drive, Dropbox integration
- [ ] **Bank integration** - Import transactions automatically
- [ ] **Payment platform integration** - PayPal, Stripe connections
- [ ] **Voice integration** - Voice commands for bill management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 coding standards
- Add color support for new features
- Include input validation for user inputs
- Update documentation for new features
- Test thoroughly before submitting

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 📞 Support & Community

### Getting Help

**Documentation:**
1. Read this comprehensive README for complete feature coverage
2. Check [Future_Update.md](Future_Update.md) for planned enhancements and roadmap
3. Review implementation documents for technical details:
   - [docs/BILLING_CYCLES_IMPLEMENTATION.md](docs/BILLING_CYCLES_IMPLEMENTATION.md)
   - [docs/CUSTOM_REMINDERS_IMPLEMENTATION.md](docs/CUSTOM_REMINDERS_IMPLEMENTATION.md)
   - [docs/ENCRYPTION_README.md](docs/ENCRYPTION_README.md)
   - [docs/DATA_COMPRESSION_README.md](docs/DATA_COMPRESSION_README.md)

**Troubleshooting:**
1. Check the troubleshooting section above for common issues
2. Try the demonstration scripts to verify functionality:
   - `python demo/demo_flexible_billing.py` - Billing cycles demo
   - `python demo/demo_custom_reminders.py` - Custom reminders demo
   - `python demo/demo_compression.py` - Data compression demo
3. Test with edge cases using: `python test/test_edge_cases.py`
4. Test encryption functionality: `python test/test_encryption.py`
5. **Test compression functionality:** `python test/test_compression.py`

**Community Support:**
1. Review existing issues on GitHub before creating new ones
2. Search closed issues for solutions to similar problems
3. Check the version history to ensure you're using the latest features

### Reporting Issues

**Before Reporting:**
- Verify you're using the latest version (3.0)
- Check that all dependencies are installed: `pip list | grep -E "colorama|tqdm"`
- Try reproducing the issue with a fresh bills.json file
- Review the troubleshooting section for known solutions

**When Creating an Issue:**
1. **Clear Title** - Briefly describe the problem
2. **System Information** - Include OS, Python version, terminal type
3. **Steps to Reproduce** - Detailed steps that cause the issue
4. **Expected vs. Actual** - What should happen vs. what actually happens
5. **Error Messages** - Include any error messages or tracebacks
6. **Screenshots** - If visual issues, include terminal screenshots

**Issue Categories:**
- 🐛 **Bug Report** - Something isn't working correctly
- 🚀 **Feature Request** - Suggest new functionality
- 📚 **Documentation** - Improvements to docs or help
- ❓ **Question** - General questions about usage
- 🔧 **Enhancement** - Improvements to existing features

### Contributing

**Ways to Contribute:**
1. **Report Issues** - Help identify bugs and improvement opportunities
2. **Suggest Features** - Propose new functionality or enhancements
3. **Improve Documentation** - Help make the docs clearer and more comprehensive
4. **Test Features** - Try out new functionality and provide feedback
5. **Code Contributions** - Submit pull requests for bug fixes or features

**Pull Request Process:**
1. Fork the repository on GitHub
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Follow the coding standards and conventions used in the project
4. Add tests for new functionality where applicable
5. Update documentation to reflect your changes
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request with detailed description

### Development Guidelines

**Code Quality:**
- Follow PEP 8 coding standards for Python
- Add comprehensive color support for any new features
- Include input validation for all user inputs
- Maintain backward compatibility with existing data
- Test thoroughly with various edge cases

**Documentation Standards:**
- Update README.md for any user-facing changes
- Add implementation documents for complex features
- Include code comments for complex logic
- Provide usage examples for new functionality
- Update troubleshooting section for known issues

**Testing Requirements:**
- Test all new features with various bill configurations
- Verify pagination works with large datasets
- Test edge cases for date handling and billing cycles
- Ensure migration works correctly for existing data
- Validate color output on different terminal types

## 📊 Statistics & Usage

### Current Capabilities
- **Supported Bills**: Unlimited (tested with 1000+ bills)
- **Billing Cycles**: 7 different types supported
- **Reminder Periods**: 1-365 days per bill
- **Search Fields**: 4 different search types
- **Sort Options**: 5 different sort criteria
- **Backup Retention**: 5 automatic backups maintained
- **Page Sizes**: Configurable (default 10 items per page)

### Performance Benchmarks
- **Small Dataset (1-10 bills)**: Instant response for all operations
- **Medium Dataset (11-50 bills)**: Pagination automatic, <1 second response
- **Large Dataset (51-100 bills)**: Efficient pagination, 1-2 second response
- **Very Large (100+ bills)**: May need optimization, consider archiving old bills

### Compatibility
- **Python Versions**: 3.6+ (tested on 3.8, 3.9, 3.10, 3.11)
- **Operating Systems**: Windows 10/11, macOS 10.14+, Linux (Ubuntu 18.04+)
- **Terminals**: Command Prompt, PowerShell, Windows Terminal, macOS Terminal, Linux terminals
- **Dependencies**: Minimal (colorama, tqdm) for maximum compatibility

## 🎯 Version History

### Version 3.3 (Current - July 2025)
- ✅ **Data Compression** - Compress database, backups, and files (GZIP, LZMA, ZLIB)
- ✅ **Compression Analysis** - Find best method for your data
- ✅ **Compression Menu** - Integrated as option 13 in the main menu
- ✅ **Demo & Test Scripts** - Comprehensive demonstration and testing for compression

### Version 3.2 (June 29, 2025)
- ✅ **Enhanced Input Validation** - URL auto-correction, email validation, date range checks, reminder period limits
- ✅ **Smart Error Handling** - User-friendly error messages with helpful suggestions and retry options
- ✅ **Data Quality Improvements** - Automatic input correction and validation for better data integrity

### Version 3.0 (June 29, 2025)
- ✅ **Custom Reminder Periods** - Individual reminder settings for each bill (1-365 days)
- ✅ **Flexible Billing Cycles** - 7 cycle types: weekly, bi-weekly, monthly, quarterly, semi-annual, annual, one-time
- ✅ **Smart Date Management** - Proper handling of month-end dates, leap years, and edge cases
- ✅ **Advanced Pagination** - Efficient handling of large datasets with configurable page sizes
- ✅ **Enhanced Due Bills System** - Custom reminders vs. specific day checking options
- ✅ **Calendar Integration** - Weekly calendar view of upcoming bills
- ✅ **Progress Indicators** - Visual feedback for backup operations and data processing
- ✅ **Automatic Migration** - Seamless upgrade of existing data with new features
- ✅ **Multi-level Sorting** - Combine multiple sort criteria with persistence
- ✅ **Enhanced Search** - Paginated search results with direct actions

### Version 2.0 (Previous)
- ✅ Added comprehensive search functionality across all fields
- ✅ Implemented flexible sorting options with visual indicators
- ✅ Added comprehensive colored output system
- ✅ Enhanced due date monitoring with urgency levels
- ✅ Improved input validation and error handling
- ✅ Added cancel operations support throughout application
- ✅ Enhanced backup system with progress tracking

### Version 1.0 (Initial)
- ✅ Basic bill management (add, view, edit, delete)
- ✅ Payment tracking with due date updates
- ✅ Automatic backup system with retention
- ✅ JSON data persistence
- ✅ Due bill notifications
- ✅ Console-based interface
- ✅ Payment method tracking

### v3.4 (July 2025)
- **Bill Categories**: Organize, view, sort, and search bills by category. New menu for category management and statistics. All bills now have a category field.

### v3.5 (July 2025)
- **Payment Methods**: Track, view, sort, and search bills by payment method. New menu for payment method management and statistics. All bills now have a payment method field. 12 payment methods supported including auto-pay, manual, credit card, bank transfer, digital wallets, and more.

## 🏆 Feature Comparison

| Feature | v1.0 | v2.0 | v3.0 | v3.2 | v3.3 |
|---------|------|------|------|------|------|
| Basic Bill Management | ✅ | ✅ | ✅ | ✅ | ✅ |
| Search Functionality | ❌ | ✅ | ✅ | ✅ | ✅ |
| Sorting Options | ❌ | ✅ | ✅ | ✅ | ✅ |
| Colored Output | ❌ | ✅ | ✅ | ✅ | ✅ |
| Billing Cycles | ❌ | ❌ | ✅ | ✅ | ✅ |
| Custom Reminders | ❌ | ❌ | ✅ | ✅ | ✅ |
| Pagination | ❌ | ❌ | ✅ | ✅ | ✅ |
| Progress Indicators | ❌ | ❌ | ✅ | ✅ | ✅ |
| Calendar View | ❌ | ❌ | ✅ | ✅ | ✅ |
| Multi-level Sorting | ❌ | ❌ | ✅ | ✅ | ✅ |
| Smart Date Handling | ❌ | ❌ | ✅ | ✅ | ✅ |
| Enhanced Validation | ❌ | ❌ | ❌ | ✅ | ✅ |
| Bill Templates | ❌ | ❌ | ❌ | ✅ | ✅ |
| Contact Information | ❌ | ❌ | ❌ | ✅ | ✅ |
| CSV Import/Export | ❌ | ❌ | ❌ | ✅ | ✅ |
| Help System | ❌ | ❌ | ❌ | ✅ | ✅ |
| Auto-complete | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Data Compression** | ❌ | ❌ | ❌ | ❌ | ✅ |

---

**Made with ❤️ for better bill management**

*Last updated: June 29, 2025 - Version 3.3*
*Next major release planned: September 2025*

---

## 🎉 Quick Start Guide

**New Users:**
1. Install: `pip install colorama tqdm`
2. Run: `python bills-tracker.py`
3. Add your first bill with option 1 (includes contact information)
4. Explore bill templates with option 9 for quick bill creation
5. Try CSV import/export with option 10 for bulk operations
6. **Try data compression with option 13 for storage savings**
7. Access help system with option 14 for detailed guidance
8. Check due bills with option 5 to see the enhanced menu system

**Existing Users Upgrading:**
1. Your data will be automatically migrated to include new features
2. All existing bills will get 7-day default reminder periods
3. Billing cycles will be set to "monthly" for existing bills
4. You can edit bills to add contact information and customize settings
5. Create templates from existing bills for quick future bill creation
6. Export your data to CSV for backup and analysis
7. Enjoy the new help system and auto-complete features!

**Power Users:**
- Try the demo scripts: `python demo/demo_flexible_billing.py`
- **Try the compression demo:** `python demo/demo_compression.py`
- Test edge cases: `python test/test_edge_cases.py`
- **Test compression:** `python test/test_compression.py`
- Create templates for recurring bills
- Use CSV import for bulk data migration
- Explore the comprehensive help system
- Contribute to future development via GitHub issues and PRs

---

*🏠 Bills Tracker v3.3 - The Complete Personal Finance Bill Management Solution 💳*

## 🔒 Security Features Overview

### Master Password Protection
The application now requires a master password for access. On first run, you'll set up a secure password that protects all your bill data. The password is securely hashed and never stored in plain text.

### Password Encryption
All passwords in bills and templates are encrypted using the Fernet algorithm for strong security. Encryption and decryption are automatic and transparent to users. Keys are managed securely and excluded from version control.

### Session Timeout/Auto-Exit
If the app is inactive for 15 minutes, it will automatically exit completely. This provides maximum security by ensuring no sensitive data remains accessible if you step away from your computer. You'll need to restart the app and enter the master password to continue.

### Security Features
- **Secure Authentication**: Master password with PBKDF2 hash and salt
- **Access Control**: 5-attempt limit with automatic lockout
- **Data Encryption**: All sensitive passwords encrypted at rest
- **Key Management**: Secure key derivation from master password
- **File Protection**: Security files excluded from version control
- **Session Timeout/Auto-Exit**: Automatic exit after 15 minutes of inactivity

For technical details, troubleshooting, and recovery, see [docs/ENCRYPTION_README.md](docs/ENCRYPTION_README.md).
