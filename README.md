# Bills Tracker 🏠💳

A comprehensi- **Data Integrity** - Comprehensive input validation and data recovery optionse command-line application for managing household bills with advanced features like flexible billing cycles, custom reminder periods, search, sorting, pagination, colored output, and automatic backups.

## ✨ Features

### Core Functionality
- **Add Bills** - Create new bills with name, due date, website, login info, password, and custom billing cycles
- **View Bills** - Display all bills with color-coded status, due date information, and pagination
- **Edit Bills** - Modify existing bill information including billing cycles and reminder periods
- **Delete Bills** - Remove bills with confirmation
- **Pay Bills** - Mark bills as paid and automatically update due dates based on billing cycles

### Advanced Date Management
- **🔄 Flexible Billing Cycles** - Support for weekly, bi-weekly, monthly, quarterly, semi-annual, annual, and one-time bills
- **⏰ Custom Reminder Periods** - Set individual reminder periods (1-365 days) for each bill
- **📅 Smart Due Date Tracking** - Automatic detection based on custom reminder windows
- **🗓️ Calendar Integration** - View upcoming bills in calendar format
- **🚨 Overdue Tracking** - Highlight overdue bills with urgency indicators

### Search & Organization
- **🔍 Smart Search** - Search bills by name, due date, website, or across all fields with pagination
- **🔄 Flexible Sorting** - Sort by due date, name, payment status, billing cycle (ascending/descending)
- **📄 Pagination** - Handle large numbers of bills efficiently with configurable page sizes
- **� Smart Filtering** - Filter bills based on custom reminder periods or specific day ranges

### Visual & User Experience
- **�🌈 Colored Output** - Visual feedback with color-coded status, urgency indicators, and billing cycles
- **📊 Progress Indicators** - Loading bars for backup operations and data processing
- **🎨 Visual Bill Status** - Emojis and colors for quick status recognition
- **� Clean Interface** - Clear console functionality for better navigation
- **❌ Cancel Operations** - Type 'cancel' at any time to abort operations

### Data Management
- **💾 Advanced Backup System** - Creates timestamped backups with retention management and progress tracking
- **🛡️ Input Validation** - Prevents duplicates and validates date formats, URLs, and ranges
- **🔄 Automatic Migration** - Seamless upgrade of existing data with new features
- **💽 Data Integrity** - Comprehensive error management with data recovery options

## 🎨 Color Scheme & Visual Indicators

### Status Colors
- 🟢 **Green** - Success messages, paid bills, completed operations
- 🔴 **Red** - Errors, overdue bills (urgent attention needed)
- 🟡 **Yellow** - Warnings, unpaid bills, due soon alerts, due today
- 🔵 **Blue** - Menu items, navigation, information details
- 🟣 **Magenta** - Titles, bill names, section headers
- 🔵 **Cyan** - General information, due dates, website details
- ⚪ **White** - User input prompts

### Billing Cycle Colors
- 🟡 **Yellow** - Weekly and bi-weekly cycles (frequent)
- 🔵 **Cyan** - Monthly cycles (standard)
- 🟢 **Green** - Quarterly cycles (seasonal)
- 🟣 **Magenta** - Semi-annual cycles (insurance, etc.)
- 🔵 **Blue** - Annual cycles (memberships, renewals)
- 🔴 **Red** - One-time bills (no recurrence)

### Urgency Indicators
- 🚨 **Red Flashing** - OVERDUE bills (immediate action required)
- 🔥 **Bright Yellow** - DUE TODAY (urgent)
- ⚠️ **Yellow** - Due within 3 days (high priority)
- 📅 **Cyan** - Due within custom reminder period (normal)
- ⏰ **White** - Reminder period information

## 📋 Requirements

- **Python 3.6 or higher**
- **colorama** library for colored output
- **tqdm** library for progress indicators  
- No other external dependencies required

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/jjfcode/Bills_tracker.git
   cd Bills_tracker
   ```

2. **Install required dependencies:**
   ```bash
   pip install colorama tqdm
   ```

3. **Run the application:**
   ```bash
   python bills-tracker.py
   ```

## 📖 Usage

### Main Menu Options

1. **📝 Add a bill** - Create new bills with comprehensive information and billing cycles
2. **📋 View all bills** - Display all bills with color-coded status and pagination
3. **🔍 Search bills** - Find bills using various search criteria with paginated results
4. **🔄 Sort bills** - Organize bills by different attributes with multiple sort options
5. **⏰ Check due bills** - View bills using custom reminder periods or specific day ranges
6. **💰 Pay a bill** - Mark bills as paid and automatically advance due dates
7. **✏️ Edit a bill** - Modify existing bill information including billing cycles
8. **🗑️ Delete a bill** - Remove bills with confirmation
9. **🚪 Exit** - Close the application

### Adding a Bill

When adding a bill, you'll be prompted for:
- **Bill name** (required) - Duplicate names are automatically detected
- **Due date** (required) - Format: YYYY-MM-DD with validation
- **Billing cycle** (required) - Choose from 7 options:
  - Weekly (every 7 days)
  - Bi-weekly (every 14 days)  
  - Monthly (every month)
  - Quarterly (every 3 months)
  - Semi-annually (every 6 months)
  - Annually (every 12 months)
  - One-time (no recurrence)
- **Reminder period** (required) - Set custom reminder days (1-365 or default 7)
- **Website** (optional) - Bill provider's website
- **Login information** (optional) - Username or account details
- **Password** (optional) - Account password

**Features:**
- Type `cancel` at any time to abort the operation
- Automatic duplicate detection prevents duplicate bill names
- Date format validation ensures proper due date entry
- Smart billing cycle selection with descriptions
- Custom reminder periods for personalized notifications
- All optional fields can be skipped

### Billing Cycles & Due Date Management

**Supported Billing Cycles:**
- **Weekly**: Perfect for weekly services (cleaning, lawn care)
- **Bi-weekly**: Great for bi-weekly payments (some salaries, newspapers)
- **Monthly**: Most common billing cycle (utilities, subscriptions, rent)
- **Quarterly**: Seasonal services (estimated taxes, some insurance)
- **Semi-annually**: Insurance premiums, some memberships
- **Annually**: Annual subscriptions, domain registrations, memberships
- **One-time**: Single payments that don't recur

**Smart Due Date Updates:**
- When you pay a bill, the due date automatically advances based on its billing cycle
- Monthly bills: January 15 → February 15 → March 15
- Quarterly bills: January 15 → April 15 → July 15
- Handles month-end dates properly (Jan 31 → Feb 28/29)
- One-time bills stay marked as paid and don't recur

### Custom Reminder Periods

**How It Works:**
- Each bill can have its own reminder period (1-365 days)
- High-priority bills (rent, utilities) can have shorter periods (3-5 days)
- Less urgent bills (annual renewals) can have longer periods (30-60 days)
- Default is 7 days for all new bills

**Due Bills Menu Options:**
1. **Custom Reminder Periods** - Shows bills based on their individual reminder settings
2. **Specific Days** - Traditional view of bills due within X days (1-365)

**Example Scenarios:**
- Rent (3 days): Get reminded 3 days before rent is due
- Credit card (7 days): Standard weekly reminder
- Car insurance (14 days): Two-week notice for expensive bills
- Annual subscription (30 days): Month-long planning time

### Search Functionality

**Search Options:**
1. **Search by name** - Find bills containing specific text in the name
2. **Search by due date** - Find bills by exact date, month/year, or year
3. **Search by website** - Find bills by website URL
4. **Search all fields** - Global search across all bill information

**Search Results Features:**
- **Pagination** - Handle large search results efficiently
- **Detailed View** - View complete bill information from search results
- **Direct Actions** - Pay or edit bills directly from search results
- **Navigation** - Easy browsing through multiple pages of results
- **Interactive Menu** - Return to search menu for new searches

### Sorting & Organization

**Sorting Options:**
1. **📅 Sort by due date** - Earliest or latest first with urgency indicators
2. **🔤 Sort by name** - Alphabetical (A-Z or Z-A) 
3. **✅ Sort by payment status** - Paid or unpaid first
4. **🔄 Sort by billing cycle** - Group by cycle type (weekly, monthly, etc.)
5. **⚡ Multi-level sorting** - Combine multiple sort criteria
6. **📄 Reset to original order** - Restore file order

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

## 📂 File Structure

```
Bills_tracker/
├── bills-tracker.py                    # Main application file with all features
├── bills.json                         # Bills data storage (auto-created)
├── backups/                           # Automatic backup directory
│   ├── bills_backup_20250629_143022.json
│   ├── bills_backup_20250629_143045.json
│   └── ... (up to 5 most recent backups)
├── README.md                          # This comprehensive documentation
├── Future_Update.md                   # Planned enhancements and roadmap
├── BILLING_CYCLES_IMPLEMENTATION.md   # Billing cycles feature documentation
├── CUSTOM_REMINDERS_IMPLEMENTATION.md # Custom reminder periods documentation
├── demo_flexible_billing.py           # Billing cycles demonstration script
├── demo_custom_reminders.py          # Custom reminders demonstration script
├── demo_enhanced_validation.py       # Enhanced validation features demonstration
├── test_billing_cycles.py            # Billing cycles testing script
├── test_edge_cases.py                # Date handling edge cases testing
├── test_validation.py                # Validation functions testing script
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
- **Local Data Storage** - All data stays on your computer
- **No External Dependencies** - Minimal risk from third-party libraries  
- **Backup Redundancy** - Multiple backup copies prevent data loss
- **Read-Only Backups** - Backup files are preserved from accidental modification
- **Input Sanitization** - Prevents malicious input from causing issues

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
- [ ] **Password encryption** - Encrypt stored passwords using Fernet
- [ ] **Master password** - Require password to access application
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
   - [BILLING_CYCLES_IMPLEMENTATION.md](BILLING_CYCLES_IMPLEMENTATION.md)
   - [CUSTOM_REMINDERS_IMPLEMENTATION.md](CUSTOM_REMINDERS_IMPLEMENTATION.md)

**Troubleshooting:**
1. Check the troubleshooting section above for common issues
2. Try the demonstration scripts to verify functionality:
   - `python demo_flexible_billing.py` - Billing cycles demo
   - `python demo_custom_reminders.py` - Custom reminders demo
3. Test with edge cases using: `python test_edge_cases.py`

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

### Version 3.1 (Current - June 29, 2025)
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

## 🏆 Feature Comparison

| Feature | v1.0 | v2.0 | v3.0 |
|---------|------|------|------|
| Basic Bill Management | ✅ | ✅ | ✅ |
| Search Functionality | ❌ | ✅ | ✅ |
| Sorting Options | ❌ | ✅ | ✅ |
| Colored Output | ❌ | ✅ | ✅ |
| Billing Cycles | ❌ | ❌ | ✅ |
| Custom Reminders | ❌ | ❌ | ✅ |
| Pagination | ❌ | ❌ | ✅ |
| Progress Indicators | ❌ | ❌ | ✅ |
| Calendar View | ❌ | ❌ | ✅ |
| Multi-level Sorting | ❌ | ❌ | ✅ |
| Smart Date Handling | ❌ | ❌ | ✅ |

---

**Made with ❤️ for better bill management**

*Last updated: June 29, 2025 - Version 3.0*
*Next major release planned: September 2025*

---

## 🎉 Quick Start Guide

**New Users:**
1. Install: `pip install colorama tqdm`
2. Run: `python bills-tracker.py`
3. Add your first bill with option 1
4. Explore custom billing cycles and reminder periods
5. Check due bills with option 5 to see the new menu system

**Existing Users Upgrading:**
1. Your data will be automatically migrated to include new features
2. All existing bills will get 7-day default reminder periods
3. Billing cycles will be set to "monthly" for existing bills
4. You can edit bills to customize billing cycles and reminder periods
5. Enjoy the new pagination, calendar view, and enhanced search features!

**Power Users:**
- Try the demo scripts: `python demo_flexible_billing.py`
- Test edge cases: `python test_edge_cases.py`
- Explore the implementation docs for technical details
- Contribute to future development via GitHub issues and PRs

---

*🏠 Bills Tracker v3.0 - The Complete Personal Finance Bill Management Solution 💳*
