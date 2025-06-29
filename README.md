# Bills Tracker 🏠💳

A comprehensive command-line application for managing household bills with advanced features like search, sorting, colored output, and automatic backups.

## ✨ Features

### Core Functionality
- **Add Bills** - Create new bills with name, due date, website, login info, and password
- **View Bills** - Display all bills with color-coded status and due date information
- **Edit Bills** - Modify existing bill information
- **Delete Bills** - Remove bills with confirmation
- **Pay Bills** - Mark bills as paid and automatically update due dates

### Advanced Features
- **🔍 Smart Search** - Search bills by name, due date, website, or across all fields
- **🔄 Flexible Sorting** - Sort by due date, name, payment status (ascending/descending)
- **🌈 Colored Output** - Visual feedback with color-coded status and urgency indicators
- **⏰ Due Date Tracking** - Automatic detection of overdue and upcoming bills
- **💾 Automatic Backups** - Creates timestamped backups with retention management
- **🛡️ Input Validation** - Prevents duplicates and validates date formats
- **❌ Cancel Operations** - Type 'cancel' at any time to abort operations

### User Experience
- **Clean Interface** - Clear console functionality for better navigation
- **Visual Indicators** - Emojis and colors for quick status recognition
- **Smart Feedback** - Contextual messages for all operations
- **Error Handling** - Comprehensive error management with helpful messages

## 🎨 Color Scheme

- 🟢 **Green** - Success messages, paid bills
- 🔴 **Red** - Errors, overdue bills
- 🟡 **Yellow** - Warnings, unpaid bills, due soon alerts
- 🔵 **Blue** - Menu items and navigation
- 🟣 **Magenta** - Titles and bill names
- 🔵 **Cyan** - Information and details
- ⚪ **White** - User input prompts

## 📋 Requirements

- **Python 3.6 or higher**
- **colorama** library for colored output
- No other external dependencies required

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/jjfcode/Bills_tracker.git
   cd Bills_tracker
   ```

2. **Install required dependencies:**
   ```bash
   pip install colorama
   ```

3. **Run the application:**
   ```bash
   python bills-tracker.py
   ```

## 📖 Usage

### Main Menu Options

1. **📝 Add a bill** - Create new bills with comprehensive information
2. **📋 View all bills** - Display all bills with color-coded status
3. **🔍 Search bills** - Find bills using various search criteria
4. **🔄 Sort bills** - Organize bills by different attributes
5. **⏰ Check due bills** - View bills due within 7 days
6. **💰 Pay a bill** - Mark bills as paid and update due dates
7. **✏️ Edit a bill** - Modify existing bill information
8. **🗑️ Delete a bill** - Remove bills with confirmation
9. **🚪 Exit** - Close the application

### Adding a Bill

When adding a bill, you'll be prompted for:
- **Bill name** (required) - Duplicate names are automatically detected
- **Due date** (required) - Format: YYYY-MM-DD with validation
- **Website** (optional) - Bill provider's website
- **Login information** (optional) - Username or account details
- **Password** (optional) - Account password

**Features:**
- Type `cancel` at any time to abort the operation
- Automatic duplicate detection prevents duplicate bill names
- Date format validation ensures proper due date entry
- All fields except name and due date are optional

### Search Functionality

**Search Options:**
1. **Search by name** - Find bills containing specific text in the name
2. **Search by due date** - Find bills by exact date, month/year, or year
3. **Search by website** - Find bills by website URL
4. **Search all fields** - Global search across all bill information

**Search Results Actions:**
- View detailed information for any bill
- Pay bills directly from search results
- Return to search menu for new searches

### Sorting Options

**Basic Sorting:**
1. **📅 Sort by due date** - Earliest or latest first
2. **🔤 Sort by name** - Alphabetical (A-Z or Z-A)
3. **✅ Sort by payment status** - Paid or unpaid first
4. **🔄 Reset to original order** - Restore file order

**Additional Features:**
- Save current sort order permanently
- Visual indicators show overdue and due-soon bills
- Context information displays days until due

### Due Bills Monitoring

The "Check due bills" feature shows:
- 🚨 **Overdue bills** - Past due date (red, urgent)
- 🔥 **Due today** - Bills due on current date (yellow, high priority)
- ⚠️ **Due soon (1-3 days)** - Immediate attention needed (yellow)
- 📅 **Due within week (4-7 days)** - Plan ahead (cyan)

### Bill Status Indicators

- **✓ Paid** - Bill has been paid (green)
- **○ Unpaid** - Bill is pending payment (yellow)
- **! OVERDUE** - Bill is past due (red, flashing)
- **Due TODAY!** - Bill is due on current date (yellow, bright)

## 📂 File Structure

```
Bills_tracker/
├── bills-tracker.py          # Main application file
├── bills.json               # Bills data storage (auto-created)
├── backups/                 # Automatic backup directory
│   ├── bills_backup_20250629_143022.json
│   ├── bills_backup_20250629_143045.json
│   └── ... (up to 5 most recent backups)
├── README.md               # This file
├── Future_Update.md        # Planned enhancements
└── .gitignore             # Git ignore file
```

## 💾 Backup System

**Automatic Backups:**
- Created before every save operation
- Timestamped filename format: `bills_backup_YYYYMMDD_HHMMSS.json`
- Stored in `backups/` directory
- Automatic retention: keeps only 5 most recent backups
- Older backups are automatically deleted

**Backup Features:**
- ✅ Automatic creation on data changes
- ✅ Timestamped for easy identification
- ✅ Space management with automatic cleanup
- ✅ Error handling for backup failures

## 🛡️ Data Safety Features

- **Input Validation** - Prevents invalid data entry
- **Duplicate Prevention** - Stops duplicate bill names
- **Date Validation** - Ensures proper date formats
- **Automatic Backups** - Protects against data loss
- **Error Recovery** - Graceful handling of corrupted files
- **Cancel Operations** - Safe abort at any time

## 🐛 Troubleshooting

### Common Issues

**"ModuleNotFoundError: No module named 'colorama'"**
```bash
pip install colorama
```

**Colors not displaying properly on Windows:**
- The app automatically initializes colorama for Windows compatibility
- If issues persist, try updating your terminal or command prompt

**"Invalid date format" errors:**
- Use YYYY-MM-DD format (e.g., 2025-07-15)
- Ensure month and day have leading zeros if needed

**Screen not clearing properly:**
- On Windows: Uses `cls` command
- On Linux/Mac: Uses `clear` command
- Ensure your terminal supports these commands

**Backup creation errors:**
- Check write permissions in the application directory
- Ensure sufficient disk space for backup files

**Bills.json file corrupted:**
- Application will automatically create a new empty file
- Restore from recent backup in `backups/` directory if needed

### Error Messages

- **❌ "This field is required"** - Enter a value or type 'cancel'
- **❌ "Invalid date format"** - Use YYYY-MM-DD format
- **❌ "Bill already exists"** - Choose a different name
- **⚠️ "No bills found"** - Add bills first before other operations
- **ℹ️ "Starting with empty bills list"** - No existing data file found

## 🚀 Future Enhancements

See [Future_Update.md](Future_Update.md) for planned improvements including:

### Phase 1 (In Progress)
- [x] **Search functionality** - ✅ Implemented
- [x] **Sort options** - ✅ Implemented  
- [x] **Colored output** - ✅ Implemented
- [ ] **Progress indicators** - Loading bars for operations
- [ ] **Pagination** - Handle large numbers of bills

### Phase 2 (Planned)
- [ ] **Password encryption** - Secure sensitive data
- [ ] **GUI interface** - Desktop application with tkinter
- [ ] **Email notifications** - Automated bill reminders
- [ ] **Bill categories** - Organize by type (utilities, subscriptions, etc.)
- [ ] **Recurring bills** - Handle complex billing cycles

### Phase 3 (Future)
- [ ] **Web interface** - Browser-based access
- [ ] **Mobile app** - Cross-platform mobile application
- [ ] **Cloud sync** - Multi-device synchronization
- [ ] **Reporting** - Analytics and spending reports

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

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Review existing issues on GitHub
3. Create a new issue with detailed description
4. Include error messages and system information

## 🎯 Version History

### Version 2.0 (Current)
- ✅ Added search functionality across all fields
- ✅ Implemented flexible sorting options
- ✅ Added comprehensive colored output
- ✅ Enhanced due date monitoring
- ✅ Improved input validation and error handling
- ✅ Added cancel operations support

### Version 1.0 (Initial)
- ✅ Basic bill management (add, view, edit, delete)
- ✅ Payment tracking with due date updates
- ✅ Automatic backup system
- ✅ JSON data persistence
- ✅ Due bill notifications

---

**Made with ❤️ for better bill management**

*Last updated: June 29, 2025*
