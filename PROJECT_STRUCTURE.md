# Bills Tracker - Project Structure

This document explains the organization and structure of the Bills Tracker application, which now includes both command-line (v2) and desktop GUI (v3) versions.

## 🚀 **Two Versions Available**

### 📱 **Desktop GUI Version (v3)** - *Recommended*
Located in `Bills_tracker_v3/` directory
- Modern GUI built with CustomTkinter
- Category system with visual organization
- Smart checkbox system for bill payment tracking
- Advanced search & filtering capabilities
- Export/Import functionality
- Automatic next cycle generation

### 💻 **Command-Line Version (v2)** - *Legacy*
Located in `src/` directory
- Console-based interface
- Advanced features like data compression and encryption
- Bill templates and contact management
- CSV import/export with validation
- Comprehensive search and sorting

## Directory Structure

```
Bills_tracker/
├── Bills_tracker_v3/              # 🆕 Desktop GUI Version (v3)
│   ├── src/
│   │   ├── gui/
│   │   │   └── main_window.py     # Main GUI window and dialogs
│   │   ├── core/
│   │   │   └── db.py             # Database operations and schema
│   │   └── utils/                 # Utilities and helpers
│   ├── resources/
│   │   ├── icons/                 # Application icons
│   │   └── themes/                # Visual themes
│   ├── main_desktop.py           # Application entry point
│   ├── requirements.txt          # Python dependencies
│   ├── README.md                 # v3 documentation
│   └── bills_tracker.db         # SQLite database for v3
├── src/                          # Command-Line Version (v2)
│   ├── main.py                   # Main application (renamed from bills-tracker.py)
│   ├── data_compression.py       # Data compression functionality
│   ├── validation.py             # Input validation utilities
│   ├── integrity_checker.py      # Data integrity checking
│   ├── db.py                     # Database utilities
│   └── migrate_to_sqlite.py      # Database migration script
├── docs/                         # Documentation
│   ├── README.md                 # Documentation index
│   ├── DATA_COMPRESSION_README.md
│   ├── VALIDATION_README.md
│   ├── ENCRYPTION_README.md
│   ├── PASSWORD_MANAGEMENT_README.md
│   ├── SQLITE_MIGRATION_README.md
│   ├── BILLING_CYCLES_IMPLEMENTATION.md
│   ├── CUSTOM_REMINDERS_IMPLEMENTATION.md
│   ├── autocomplete_implementation_summary.txt
│   └── organization_summary.txt
├── demo/                         # Demo scripts
│   ├── README.md
│   ├── demo_compression.py
│   ├── demo_autocomplete.py
│   ├── demo_enhanced_validation.py
│   ├── demo_custom_reminders.py
│   └── demo_flexible_billing.py
├── test/                         # Test scripts
│   ├── README.md
│   ├── test_compression.py
│   ├── test_validation.py
│   ├── test_encryption.py
│   ├── test_integrity_checker.py
│   ├── test_password_management.py
│   ├── test_sqlite_integration.py
│   ├── test_autocomplete.py
│   ├── test_billing_cycles.py
│   ├── test_comprehensive_validation.py
│   ├── test_edge_cases.py
│   ├── test_menu_options.py
│   └── test_password_management_quick.py
├── backups/                      # Backup files (auto-generated)
├── run.py                        # Application launcher (v2)
├── requirements.txt              # Python dependencies (v2)
├── README.md                     # Main project documentation
├── PROJECT_STRUCTURE.md          # This file
├── Future_Update.md              # Feature roadmap
├── .gitignore                    # Git ignore rules
├── bills_tracker.db              # SQLite database (v2, auto-generated)
├── bills.json                    # Legacy JSON file (for migration)
├── .encryption_key               # Encryption key (auto-generated)
├── .salt                         # Salt for key derivation (auto-generated)
├── .master_password              # Master password hash (auto-generated)
└── BillsTracker.spec             # PyInstaller specification
```

## File Organization

### Desktop GUI Version (v3) - `Bills_tracker_v3/`
- **main_desktop.py**: Application entry point for GUI version
- **src/gui/main_window.py**: Main application window and all dialogs
- **src/core/db.py**: Database operations with category support
- **src/utils/**: Utility functions for GUI
- **resources/**: Icons and themes for the GUI
- **requirements.txt**: Dependencies for GUI version

### Command-Line Version (v2) - `src/`
- **main.py**: Main application with all core functionality
- **data_compression.py**: Data compression utilities for large datasets
- **validation.py**: Input validation and data sanitization
- **integrity_checker.py**: Data integrity verification and repair
- **db.py**: Database connection and utility functions
- **migrate_to_sqlite.py**: Migration script from JSON to SQLite

### Documentation (`docs/`)
Comprehensive documentation for each major feature:
- Implementation guides
- Usage instructions
- Technical details
- Migration guides

### Demo Scripts (`demo/`)
Interactive demonstrations of key features:
- Data compression examples
- Autocomplete functionality
- Validation features
- Billing cycles
- Custom reminders

### Test Scripts (`test/`)
Comprehensive test suite:
- Unit tests for each module
- Integration tests
- Edge case testing
- Performance testing

### Auto-Generated Files
These files are created automatically and should not be manually edited:
- `bills_tracker.db`: SQLite database (both versions have their own)
- `bills.json`: Legacy JSON data (for migration)
- `.encryption_key`: Encryption key for password protection (v2 only)
- `.salt`: Salt for key derivation (v2 only)
- `.master_password`: Master password hash (v2 only)
- `backups/`: Directory containing backup files

## Running the Applications

### Desktop GUI Version (v3) - *Recommended*
```bash
cd Bills_tracker_v3
python main_desktop.py
```

### Command-Line Version (v2) - *Legacy*
```bash
# Option 1: Using the launcher script
python run.py

# Option 2: Running directly from src
cd src
python main.py
```

## Key Differences Between Versions

### Version 3 (Desktop GUI)
- **Modern GUI**: Built with CustomTkinter for a modern look
- **Category System**: Visual organization with color-coded categories
- **Smart Checkbox**: Mark bills as paid with automatic next cycle generation
- **Advanced UI**: Search, filtering, sorting with visual feedback
- **Simplified Setup**: No encryption or master password required
- **Database**: SQLite with category support

### Version 2 (Command-Line)
- **Console Interface**: Text-based interface with colored output
- **Advanced Security**: Master password protection and encryption
- **Data Compression**: Built-in compression for large datasets
- **Bill Templates**: Save and reuse bill configurations
- **Comprehensive Features**: All advanced features from original version
- **Database**: SQLite with encryption support

## Development Workflow

### For Version 3 (GUI)
1. **Main Development**: Edit files in `Bills_tracker_v3/src/`
2. **GUI Components**: Work in `Bills_tracker_v3/src/gui/`
3. **Database**: Modify `Bills_tracker_v3/src/core/db.py`
4. **Testing**: Test GUI functionality manually

### For Version 2 (Command-Line)
1. **Main Development**: Edit files in `src/`
2. **Testing**: Run tests from `test/` directory
3. **Documentation**: Update files in `docs/` as needed
4. **Demos**: Create new demos in `demo/` for new features

## Git Ignore Rules

The `.gitignore` file is configured to exclude:
- Database files (`bills_tracker.db`, `bills.json`)
- Backup files (`backups/`)
- Encryption keys (`.encryption_key`, `.salt`, `.master_password`)
- Python cache files (`__pycache__/`, `*.pyc`)
- Build artifacts (`build/`, `dist/`)
- IDE files (`.vscode/`, `.idea/`)
- OS files (`.DS_Store`, `Thumbs.db`)
- Temporary files (`*.tmp`, `*.log`)

## Migration Notes

- **Version 3**: New desktop GUI version with modern interface
- **Version 2**: Legacy command-line version with all original features
- Both versions use SQLite databases but with different schemas
- Version 3 focuses on ease of use, Version 2 on advanced features
- Users can choose which version best fits their needs

## Security Considerations

### Version 2 (Command-Line)
- Encryption keys and passwords are stored in hidden files (starting with `.`)
- These files are excluded from version control
- Database files contain sensitive data and are also excluded
- Backup files may contain sensitive data and are excluded

### Version 3 (Desktop GUI)
- No encryption by default (simplified for ease of use)
- Database files are excluded from version control
- Users should manually backup the database file

## Backup Strategy

- Automatic backups are stored in `backups/` directory (v2)
- Backup files are excluded from version control
- Users should manually backup the entire project directory for safekeeping
- Database files should be backed up separately
- Version 3 users should backup `Bills_tracker_v3/bills_tracker.db`

## Choosing Between Versions

### Choose Version 3 (Desktop GUI) if you:
- Prefer a modern, visual interface
- Want easy category organization
- Need quick bill management
- Don't require advanced security features
- Want automatic next cycle generation

### Choose Version 2 (Command-Line) if you:
- Prefer keyboard-based navigation
- Need advanced security features
- Want data compression capabilities
- Use bill templates extensively
- Need comprehensive contact management
- Work with large datasets 