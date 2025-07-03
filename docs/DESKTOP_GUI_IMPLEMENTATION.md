# Desktop GUI Implementation (v3) - Bills Tracker

This document details the implementation of the desktop GUI version (v3) of Bills Tracker, built with CustomTkinter.

## 🚀 **Overview**

The desktop GUI version provides a modern, user-friendly interface for bill management with advanced features like category organization, smart checkbox system, and real-time search capabilities.

## 📁 **Project Structure**

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
├── requirements.txt          # Python dependencies
└── bills_tracker.db         # SQLite database
```

## 🏗️ **Architecture**

### **MVC Pattern Implementation**
- **Model**: `src/core/db.py` - Database operations and data management
- **View**: `src/gui/main_window.py` - GUI components and user interface
- **Controller**: Logic embedded in GUI components for user interactions

### **Key Components**

#### **Main Window (`main_window.py`)**
```python
class BillsTrackerApp:
    def __init__(self):
        # Initialize main window
        # Setup sidebar navigation
        # Create bills table
        # Initialize search and filter components
```

**Features:**
- **Sidebar Navigation** - Switch between Bills and Categories views
- **Bills Table** - Sortable, filterable table with checkboxes
- **Search & Filter** - Real-time search with multiple field options
- **Action Buttons** - Add, Edit, Delete, Export, Import functionality

#### **Database Layer (`db.py`)**
```python
class DatabaseManager:
    def __init__(self, db_path):
        # Initialize SQLite connection
        # Create tables if not exist
        # Setup foreign key constraints
```

**Tables:**
- **bills** - Main bills data with category references
- **categories** - Category definitions with colors and descriptions

## 🎯 **Key Features Implementation**

### **1. Category System**

#### **Database Schema**
```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    color TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE bills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    due_date TEXT NOT NULL,
    billing_cycle TEXT NOT NULL,
    reminder_days INTEGER DEFAULT 7,
    paid BOOLEAN DEFAULT 0,
    category_id INTEGER,
    web_page TEXT,
    login_info TEXT,
    password TEXT,
    company_email TEXT,
    support_phone TEXT,
    billing_phone TEXT,
    customer_service_hours TEXT,
    account_number TEXT,
    reference_id TEXT,
    support_chat_url TEXT,
    mobile_app TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories (id)
);
```

#### **Pre-defined Categories**
```python
DEFAULT_CATEGORIES = [
    ("Utilities", "#FF6B6B", "Electricity, water, gas, internet"),
    ("Subscriptions", "#4ECDC4", "Streaming, software, memberships"),
    ("Insurance", "#45B7D1", "Health, auto, home, life insurance"),
    ("Loans", "#96CEB4", "Mortgage, car loans, personal loans"),
    ("Credit Cards", "#FFEAA7", "Credit card payments"),
    ("Taxes", "#DDA0DD", "Property, income, sales taxes"),
    ("Healthcare", "#98D8C8", "Medical bills, prescriptions"),
    ("Entertainment", "#F7DC6F", "Movies, games, events"),
    ("Transportation", "#BB8FCE", "Fuel, public transit, maintenance"),
    ("Other", "#85C1E9", "Miscellaneous bills")
]
```

#### **Category Management Features**
- **Add Categories** - Create new categories with custom colors
- **Edit Categories** - Modify existing category details
- **Delete Categories** - Remove unused categories (with validation)
- **Category Statistics** - Show bill count per category
- **Color-coded Display** - Visual organization in bills table

### **2. Smart Checkbox System**

#### **Implementation Logic**
```python
def on_checkbox_click(self, bill_id, is_checked):
    # Store pending changes
    self.pending_changes[bill_id] = {
        'paid': is_checked,
        'original_paid': not is_checked
    }
    
    # Update checkbox display
    self.update_checkbox_display(bill_id, is_checked)
    
    # Update pending changes counter
    self.update_pending_counter()
```

#### **Apply Changes Process**
```python
def apply_changes(self):
    # Process all pending changes
    for bill_id, changes in self.pending_changes.items():
        # Update bill as paid
        self.db.update_bill_paid_status(bill_id, True)
        
        # Calculate next due date based on billing cycle
        next_due_date = self.calculate_next_due_date(bill_id)
        
        # Create new bill for next cycle
        self.create_next_cycle_bill(bill_id, next_due_date)
    
    # Clear pending changes
    self.pending_changes.clear()
    self.refresh_data()
```

#### **Billing Cycle Calculations**
```python
def calculate_next_due_date(self, bill_id):
    bill = self.db.get_bill(bill_id)
    current_due = datetime.strptime(bill['due_date'], '%Y-%m-%d')
    
    if bill['billing_cycle'] == 'weekly':
        return current_due + timedelta(weeks=1)
    elif bill['billing_cycle'] == 'bi-weekly':
        return current_due + timedelta(weeks=2)
    elif bill['billing_cycle'] == 'monthly':
        return self.add_months(current_due, 1)
    # ... other cycles
```

### **3. Advanced Search & Filtering**

#### **Search Implementation**
```python
def filter_bills(self, search_text, search_field):
    if not search_text:
        return self.all_bills
    
    filtered_bills = []
    search_text = search_text.lower()
    
    for bill in self.all_bills:
        if search_field == "Name":
            if search_text in bill['name'].lower():
                filtered_bills.append(bill)
        elif search_field == "Category":
            category_name = self.get_category_name(bill['category_id'])
            if search_text in category_name.lower():
                filtered_bills.append(bill)
        # ... other fields
    
    return filtered_bills
```

#### **Real-time Filtering**
- **Instant Results** - Filter updates as user types
- **Multi-field Search** - Search by Name, Due Date, Category, Status, Paid
- **Case-insensitive** - Search works regardless of case
- **Clear Function** - Reset filters with one click

### **4. Export/Import Functionality**

#### **CSV Export**
```python
def export_to_csv(self, filename):
    bills = self.db.get_all_bills_with_categories()
    
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=bills[0].keys())
        writer.writeheader()
        writer.writerows(bills)
```

#### **CSV Import with Validation**
```python
def import_from_csv(self, filename):
    imported_bills = []
    errors = []
    
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            # Validate required fields
            if not self.validate_bill_data(row):
                errors.append(f"Invalid data in row: {row}")
                continue
            
            # Check for duplicates
            if self.db.bill_exists(row['name']):
                errors.append(f"Duplicate bill: {row['name']}")
                continue
            
            # Import bill
            bill_id = self.db.add_bill(row)
            imported_bills.append(bill_id)
    
    return imported_bills, errors
```

## 🎨 **User Interface Design**

### **Layout Structure**
```
┌─────────────────────────────────────────────────────────┐
│                    Bills Tracker v3                      │
├─────────────┬───────────────────────────────────────────┤
│   Sidebar   │              Main Content                 │
│             │                                           │
│ • Bills     │  ┌─────────────────────────────────────┐  │
│ • Categories│  │         Search & Filter              │  │
│             │  └─────────────────────────────────────┘  │
│             │                                           │
│             │  ┌─────────────────────────────────────┐  │
│             │  │         Bills Table                 │  │
│             │  │  [☐] Bill Name | Due Date | Cat...  │  │
│             │  │  [✓] Bill Name | Due Date | Cat...  │  │
│             │  └─────────────────────────────────────┘  │
│             │                                           │
│             │  ┌─────────────────────────────────────┐  │
│             │  │         Action Buttons              │  │
│             │  │ [Add] [Edit] [Delete] [Export] [Import] │
│             │  └─────────────────────────────────────┘  │
└─────────────┴───────────────────────────────────────────┘
```

### **Color Scheme**
- **Primary**: CustomTkinter default theme
- **Categories**: Hex color codes for visual organization
- **Status Indicators**: 
  - Green: Paid bills
  - Yellow: Unpaid bills
  - Red: Overdue bills

### **Responsive Design**
- **Flexible Layout** - Adapts to different window sizes
- **Scrollable Tables** - Handle large datasets
- **Proper Spacing** - Consistent margins and padding
- **Accessibility** - High contrast and readable fonts

## 🔧 **Technical Implementation Details**

### **Database Operations**
```python
class DatabaseManager:
    def get_all_bills_with_categories(self):
        """Get all bills with category information"""
        query = """
        SELECT b.*, c.name as category_name, c.color as category_color
        FROM bills b
        LEFT JOIN categories c ON b.category_id = c.id
        ORDER BY b.due_date
        """
        return self.execute_query(query)
    
    def update_bill_paid_status(self, bill_id, paid):
        """Update bill paid status"""
        query = "UPDATE bills SET paid = ? WHERE id = ?"
        self.execute_query(query, (paid, bill_id))
    
    def create_next_cycle_bill(self, original_bill_id, next_due_date):
        """Create new bill for next billing cycle"""
        original_bill = self.get_bill(original_bill_id)
        
        new_bill = {
            'name': original_bill['name'],
            'due_date': next_due_date.strftime('%Y-%m-%d'),
            'billing_cycle': original_bill['billing_cycle'],
            'reminder_days': original_bill['reminder_days'],
            'paid': False,  # New bill starts as unpaid
            'category_id': original_bill['category_id'],
            # ... copy other fields
        }
        
        return self.add_bill(new_bill)
```

### **Event Handling**
```python
def setup_event_handlers(self):
    """Setup all event handlers"""
    # Search field changes
    self.search_var.trace('w', self.on_search_change)
    
    # Table selection
    self.bills_table.bind('<<TreeviewSelect>>', self.on_bill_select)
    
    # Checkbox clicks
    self.bills_table.bind('<Button-1>', self.on_table_click)
    
    # Button clicks
    self.add_button.configure(command=self.show_add_dialog)
    self.edit_button.configure(command=self.show_edit_dialog)
    self.delete_button.configure(command=self.delete_selected_bill)
    self.export_button.configure(command=self.export_to_csv)
    self.import_button.configure(command=self.import_from_csv)
    self.apply_changes_button.configure(command=self.apply_changes)
```

### **Dialog Management**
```python
class BillDialog:
    def __init__(self, parent, title, bill_data=None):
        self.dialog = customtkinter.CTkToplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("500x600")
        self.dialog.resizable(False, False)
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog on parent
        self.center_dialog(parent)
        
        # Setup form fields
        self.setup_form(bill_data)
```

## 🧪 **Testing Strategy**

### **Manual Testing Checklist**
- [ ] **Category Management**
  - Add new categories
  - Edit existing categories
  - Delete unused categories
  - Verify category colors display correctly

- [ ] **Bill Operations**
  - Add new bills with categories
  - Edit existing bills
  - Delete bills
  - Verify all fields save correctly

- [ ] **Checkbox System**
  - Click checkboxes to mark bills as paid
  - Verify pending changes counter updates
  - Apply changes and verify new bills created
  - Check next due date calculations

- [ ] **Search & Filtering**
  - Search by different fields
  - Verify real-time filtering
  - Test clear filter functionality
  - Verify sorting works with filters

- [ ] **Export/Import**
  - Export bills to CSV
  - Import bills from CSV
  - Verify validation and duplicate checking
  - Test error handling

### **Database Testing**
```python
def test_database_operations():
    """Test all database operations"""
    db = DatabaseManager(":memory:")  # Use in-memory database for testing
    
    # Test category operations
    category_id = db.add_category("Test Category", "#FF0000", "Test description")
    assert db.get_category(category_id) is not None
    
    # Test bill operations
    bill_data = {
        'name': 'Test Bill',
        'due_date': '2024-01-01',
        'billing_cycle': 'monthly',
        'category_id': category_id
    }
    bill_id = db.add_bill(bill_data)
    assert db.get_bill(bill_id) is not None
    
    # Test foreign key constraints
    db.delete_category(category_id)
    # Should fail due to foreign key constraint
```

## 🚀 **Performance Considerations**

### **Optimization Strategies**
1. **Lazy Loading** - Load data only when needed
2. **Efficient Queries** - Use JOINs and proper indexing
3. **Memory Management** - Clear unused references
4. **UI Responsiveness** - Use threading for long operations

### **Database Indexing**
```sql
-- Index for faster searches
CREATE INDEX idx_bills_name ON bills(name);
CREATE INDEX idx_bills_due_date ON bills(due_date);
CREATE INDEX idx_bills_category ON bills(category_id);
CREATE INDEX idx_bills_paid ON bills(paid);
```

## 🔮 **Future Enhancements**

### **Planned Features**
1. **Reminder System** - Desktop notifications and email alerts
2. **Reports & Analytics** - Spending reports and bill history
3. **Backup & Sync** - Cloud backup and multi-device sync
4. **Theme System** - Dark/light mode and custom themes
5. **Keyboard Shortcuts** - Full keyboard navigation

### **Technical Improvements**
1. **Unit Tests** - Comprehensive test coverage
2. **Error Handling** - More robust error recovery
3. **Performance** - Optimize for large datasets
4. **Accessibility** - Screen reader support and keyboard navigation

---

**Bills Tracker v3** - Modern bill management with a beautiful, intuitive interface! 💰📊 