# Bills Tracker

A simple command-line Python application to help you track and manage your bills, due dates, and payment history.

## Features

- **Add Bills**: Store bill information including name, due date, web page, login credentials, and password
- **View All Bills**: Display a complete list of all your bills with their details
- **Check Due Bills**: Identify bills that are due within a specified timeframe (default: 7 days)
- **Pay Bills**: Mark bills as paid and automatically update the next due date
- **Persistent Storage**: All bill data is saved to a JSON file for persistence between sessions

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only built-in Python libraries)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/jjfcode/Bills_tracker.git
   cd Bills_tracker
   ```
2. Ensure you have Python installed on your system
3. No additional installation steps required

## Usage

Run the program from the command line:

```bash
python bills-tracker.py
```

### Menu Options

When you run the program, you'll see a menu with the following options:

1. **Add a bill** - Add a new bill to your tracker
2. **View all bills** - Display all stored bills
3. **Verify due bills** - Check which bills are due soon
4. **Pay a bill** - Mark a bill as paid and update its next due date
5. **Exit** - Close the program

### Adding a Bill

When adding a bill, you'll be prompted to enter:
- Bill name
- Due date (format: YYYY-MM-DD)
- Web page URL
- Login information
- Password

### Paying a Bill

When you pay a bill:
- The bill is marked as paid
- The due date is automatically updated to the first day of the next month
- The data is saved to the JSON file

### Checking Due Bills

The program will show you bills that are due within the next 7 days by default. Bills are considered due if their due date falls within the specified timeframe from today.

## File Structure

```
Bills_tracker/
├── bills-tracker.py    # Main application file
├── bills.json         # Data storage file (created automatically)
└── README.md          # This documentation file
```

## Data Storage

Bills are stored in a JSON file (`bills.json`) with the following structure:

```json
[
    {
        "name": "Electric Bill",
        "due_date": "2025-07-15",
        "web_page": "https://electric-company.com",
        "login_info": "user@email.com",
        "password": "your_password",
        "paid": false
    }
]
```

## Security Note

⚠️ **Important**: This application stores passwords in plain text in the JSON file. For production use, consider implementing proper encryption for sensitive data like passwords.

## Future Enhancements

Potential improvements for this application could include:
- Password encryption
- Bill categories and filtering
- Recurring bill management
- Email notifications for due bills
- GUI interface
- Export functionality
- Bill amount tracking

## Contributing

Feel free to fork this project and submit pull requests for any improvements.

Repository: https://github.com/jjfcode/Bills_tracker

## License

This project is open source and available under the [MIT License](LICENSE).

## Troubleshooting

### Common Issues

1. **"Invalid date format" error**: Ensure dates are entered in YYYY-MM-DD format
2. **File permissions**: Make sure the application has write permissions in the directory
3. **JSON file corruption**: If the bills.json file becomes corrupted, delete it and restart the application

### Error Messages

- **"No bills found"**: No bills have been added yet
- **"Invalid selection"**: You entered a number outside the valid range when selecting a bill
- **"This bill has already been paid"**: The selected bill is already marked as paid

## Contact

If you encounter any issues or have suggestions for improvements, please create an issue in the repository: https://github.com/jjfcode/Bills_tracker/issues
