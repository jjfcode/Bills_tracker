# Bills Tracker Desktop (v3)

A modern, feature-rich desktop application for managing bills and recurring payments with an intuitive GUI built using CustomTkinter.

## 🚀 Features

### 📋 **Core Bill Management**
- **Add, Edit, Delete Bills** with comprehensive form validation
- **Smart Checkbox System** - Mark bills as paid with automatic next cycle generation
- **Apply Changes** - Review and confirm multiple changes before saving
- **Recurring Bill Cycles** - Automatic next due date calculation (weekly, bi-weekly, monthly, quarterly, semi-annually, annually)
- **Input Validation** - Email, phone, web page, and date format validation
- **Modal Dialogs** - Clean, modern interface for adding/editing bills

### 📅 **Advanced Date Selection** 🆕
- **Visual Calendar Picker** - Click 📅 button for intuitive date selection
- **Fallback Date Picker** - Simple dropdown picker if calendar unavailable
- **Direct Input** - Type dates manually in YYYY-MM-DD format
- **Date Validation** - Automatic validation of date format and validity

### 🏷️ **Category System**
- **10 Pre-defined Categories** with custom colors
- **Custom Category Management** - Add, edit, delete categories
- **Category Assignment** - Assign bills to categories via dropdown
- **Category-based Filtering** - Search and filter bills by category
- **Category Statistics** - View bill count per category
- **Color-coded Categories** - Visual organization with hex color support

### 🔍 **Advanced Search & Filtering** 🆕
- **Default Pending View** - Shows only unpaid bills by default for daily use
- **Status Filtering** - Filter by Pending, Paid, or All bills
- **Period Filtering** - Filter by time periods:
  - **This Month** - Current month bills
  - **Last Month** - Previous month bills  
  - **Previous Month** - Two months ago
  - **This Year** - Current year bills
  - **Last Year** - Previous year bills
- **Combined Filtering** - Use status, period, and search filters together
- **Real-time Search** - Instant filtering as you type
- **Multi-field Search** - Search by Name, Due Date, Category, Status, or Paid status
- **Smart Filtering** - Maintains sort order while filtering
- **Bill Counter** - Shows exactly how many bills are being displayed
- **Clear Filters** - Reset to default view or clear specific filters

### 📊 **Data Management**
- **Table Sorting** - Click any column header to sort (ascending/descending with arrow indicators)
- **Export to CSV** - Backup and share your bills data
- **Import from CSV** - Bulk import with validation and duplicate checking
- **Data Refresh** - Refresh data from database with pending changes protection

### 🎨 **User Experience**
- **Modern GUI** - Clean, responsive interface using CustomTkinter
- **User Feedback** - Success/error popups with proper error handling
- **Responsive Design** - Adapts to different window sizes
- **Keyboard Navigation** - Full keyboard support
- **Error Handling** - Robust error handling with user-friendly messages

### 🔄 **Smart Bill Processing**
- **Pending Changes System** - Make multiple changes before applying
- **Automatic Next Cycle** - When marking a bill as paid, automatically creates the next bill for the following cycle
- **Historical Tracking** - Keeps paid bills for reporting while creating new ones
- **Billing Cycle Support** - Handles all common billing cycles automatically

## 📁 Project Structure

```
Bills_tracker_v3/
├── src/
│   ├── gui/
│   │   └── main_window.py      # Main application window and dialogs
│   ├── core/
│   │   └── db.py              # Database operations and schema
│   └── utils/                 # Utilities and helpers
├── resources/
│   ├── icons/                 # Application icons
│   └── themes/                # Visual themes
├── main_desktop.py           # Application entry point
├── demo_date_selector.py     # Demo for date selection features
├── demo_advanced_filtering.py # Demo for advanced filtering features
├── requirements.txt          # Python dependencies
└── bills_tracker.db         # SQLite database
```

## 🛠️ Requirements

- **Python 3.9+**
- **CustomTkinter** - Modern GUI framework
- **tkcalendar** - Calendar widget for date selection
- **SQLite3** - Database engine (included with Python)
- **Additional dependencies** (see requirements.txt)

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Bills_tracker_v3
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main_desktop.py
   ```

4. **Try the demos:**
   ```bash
   python demo_date_selector.py      # Date selection features
   python demo_advanced_filtering.py # Advanced filtering features
   ```

## 📖 How to Use

### **Adding Bills**
1. Click "Add Bill" button
2. Fill in the required fields (Name, Due Date)
3. **Select Due Date** using the new date selector:
   - Click 📅 for visual calendar
   - Use quick buttons for common dates
   - Type directly in the date field
4. Select a category from the dropdown
5. Choose billing cycle and reminder days
6. Add optional information (web page, contact details)
7. Click "Add" to save

### **Date Selection Features**
- **📅 Calendar Picker**: Click the calendar button for visual date selection
- **Direct Input**: Type dates directly in YYYY-MM-DD format
- **Fallback Picker**: Simple dropdown picker if calendar widget unavailable
- **Validation**: Automatic validation of date format and validity

### **Managing Categories**
1. Click "Categories" in the sidebar
2. View all categories with bill counts
3. Use "Add Category" to create new ones
4. Select a category and use "Edit" or "Delete"
5. Categories in use cannot be deleted

### **Marking Bills as Paid**
1. Click the checkbox (☐) next to a bill
2. The bill will be marked as paid (✓) and date updated
3. Click "Apply Changes" to confirm
4. A new bill for the next cycle will be created automatically

### **Searching and Filtering**
1. **Default View**: App opens showing only PENDING bills (most useful for daily use)
2. **Status Filter**: Choose Pending, Paid, or All bills
3. **Period Filter**: Filter by time periods (This Month, Last Month, etc.)
4. **Search**: Use the search bar with different fields (Name, Due Date, Category, etc.)
5. **Combined Filters**: Use status, period, and search filters together
6. **Clear Options**: 
   - "Clear Search" - Clears only the search field
   - "Clear All" - Resets to default view (Pending bills only)
7. **Bill Counter**: Shows exactly how many bills are being displayed
8. Click column headers to sort

### **Exporting/Importing Data**
1. Click "Export CSV" to download all bills
2. Click "Import CSV" to upload bills from file
3. Duplicate checking prevents importing existing bills

## 🗄️ Database Schema

### **Bills Table**
- `id` - Primary key
- `name` - Bill name
- `due_date` - Due date (YYYY-MM-DD)
- `billing_cycle` - Recurring cycle
- `reminder_days` - Days before due for reminders
- `paid` - Boolean paid status
- `category_id` - Foreign key to categories
- Plus additional fields for contact info, web pages, etc.

### **Categories Table**
- `id` - Primary key
- `name` - Category name (unique)
- `color` - Hex color code
- `description` - Category description
- `created_at` - Timestamp

## 🎯 Key Features Explained

### **Smart Checkbox System**
Unlike traditional bill trackers, this system:
- Allows multiple changes before saving
- Automatically calculates next due dates based on billing cycles
- Creates new bills for future cycles while preserving payment history
- Provides visual feedback with pending changes counter

### **Advanced Date Selection**
The new date selector provides multiple ways to choose dates:
- **Visual Calendar**: Intuitive point-and-click date selection
- **Direct Input**: Type dates manually with validation
- **Fallback Support**: Works even if calendar widget unavailable
- **Clean Interface**: Simple and focused design

### **Category Management**
- **Pre-defined Categories**: 10 common categories with appropriate colors
- **Custom Categories**: Create unlimited custom categories
- **Visual Organization**: Color-coded categories for easy identification
- **Statistics**: See how many bills are in each category

### **Data Integrity**
- **Foreign Key Constraints**: Prevents orphaned data
- **Input Validation**: Ensures data quality
- **Duplicate Prevention**: Prevents importing duplicate bills
- **Error Recovery**: Graceful handling of database errors

## 🔧 Technical Details

### **Architecture**
- **MVC Pattern**: Separation of concerns between GUI, business logic, and data
- **SQLite Database**: Lightweight, file-based database
- **CustomTkinter**: Modern, themeable GUI framework
- **tkcalendar**: Professional calendar widget
- **Modular Design**: Easy to extend and maintain

### **Performance**
- **Efficient Queries**: Optimized database queries with JOINs
- **Lazy Loading**: Data loaded only when needed
- **Memory Management**: Proper cleanup of resources
- **Responsive UI**: Non-blocking operations for better UX

## 🐛 Troubleshooting

### **Common Issues**
1. **Database Errors**: Ensure you have write permissions in the application directory
2. **Import Errors**: Check CSV format matches expected structure
3. **GUI Issues**: Verify CustomTkinter is properly installed
4. **Calendar Issues**: Install tkcalendar with `pip install tkcalendar`

### **Error Messages**
- All errors are displayed in user-friendly popups
- Console output provides detailed error information for debugging

## 🔄 Version History

### **v3.1** (Current)
- ✅ **Advanced Filtering System** - Default pending view, status/period filters, bill counter
- ✅ **Advanced Date Selection** - Visual calendar picker and direct input
- ✅ Complete GUI rewrite with CustomTkinter
- ✅ Category system with management interface
- ✅ Smart checkbox system with pending changes
- ✅ Export/Import functionality
- ✅ Automatic next cycle generation
- ✅ Modern, responsive design

### **v3.0** (Previous)
- Basic date entry with manual typing
- All other features from v3.1

### **v2.0** (Legacy)
- Console-based interface
- Basic bill management
- Simple file storage

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Bills Tracker v3** - Modern bill management with intuitive date selection! 💰📊📅 