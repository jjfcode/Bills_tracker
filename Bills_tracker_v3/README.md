# Bills Tracker Desktop (v3)

This is the desktop (GUI) version of Bills Tracker.

## Project Structure

- `src/gui/` - Graphical user interface (windows, dialogs, menus)
- `src/core/` - Business logic and data management
- `src/utils/` - Utilities and helpers
- `resources/icons/` - Application icons
- `resources/themes/` - Visual themes

## Features

- Add, edit, and delete bills with a modern GUI
- Dropdowns for billing cycle and reminder days
- Input validation for email, phone, and web page
- Modal dialogs for adding/editing bills
- User feedback popups for success and errors
- **Table sorting:** Click any column header to sort by that column. Click again to toggle ascending/descending. An arrow indicator shows the current sort order.
- **Search and filter:** Real-time filtering with a search bar. Select the search field (Name, Due Date, Category, Status) from a dropdown. Use the Clear button to reset the filter.
- **Export/Import:** Export all bills to CSV format for backup or sharing. Import bills from CSV with automatic validation and duplicate checking.

## Requirements
- Python 3.9+
- customtkinter or tkinter
- sqlite3
- cryptography

## How to Start
Coming soon...

---

*This README is specific to the desktop version (v3). For the console version, see the README in the project root.* 