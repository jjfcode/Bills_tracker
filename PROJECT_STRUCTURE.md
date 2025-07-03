# Bills Tracker - Project Structure

This document explains the organization and structure of the Bills Tracker application.

## Directory Structure

```
Bills_tracker/
├── src/                          # Main source code
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
├── run.py                        # Application launcher
├── requirements.txt              # Python dependencies
├── README.md                     # Main project documentation
├── Future_Update.md              # Feature roadmap
├── .gitignore                    # Git ignore rules
├── bills_tracker.db              # SQLite database (auto-generated)
├── bills.json                    # Legacy JSON file (for migration)
├── .encryption_key               # Encryption key (auto-generated)
├── .salt                         # Salt for key derivation (auto-generated)
├── .master_password              # Master password hash (auto-generated)
└── BillsTracker.spec             # PyInstaller specification
```

## File Organization

### Source Code (`src/`)
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
- `bills_tracker.db`: SQLite database
- `bills.json`: Legacy JSON data (for migration)
- `.encryption_key`: Encryption key for password protection
- `.salt`: Salt for key derivation
- `.master_password`: Master password hash
- `backups/`: Directory containing backup files

## Running the Application

### Option 1: Using the launcher script
```bash
python run.py
```

### Option 2: Running directly from src
```bash
cd src
python main.py
```

## Development Workflow

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

- The main application was moved from `bills-tracker.py` to `src/main.py`
- All utility modules are now in the `src/` directory
- A launcher script (`run.py`) was added for easy execution
- Import statements were updated to use relative imports

## Security Considerations

- Encryption keys and passwords are stored in hidden files (starting with `.`)
- These files are excluded from version control
- Database files contain sensitive data and are also excluded
- Backup files may contain sensitive data and are excluded

## Backup Strategy

- Automatic backups are stored in `backups/` directory
- Backup files are excluded from version control
- Users should manually backup the entire project directory for safekeeping
- Database and encryption files should be backed up separately 