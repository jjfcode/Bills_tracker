# 1. Imports
import json
import os
import shutil
from datetime import datetime, timedelta

# 2. Configuration
BILLS_FILE = 'bills.json'
BACKUP_DIR = 'backups'
MAX_BACKUPS = 5
DATE_FORMAT = '%Y-%m-%d'

bills = []

# 3. Utility functions
def clear_console():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

# 4. File operations
def backup_bills():
    try:
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR)
        
        if not os.path.exists(BILLS_FILE):
            print("No bills.json found. No backup needed.")
            return
            
        # Create backup with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"bills_backup_{timestamp}.json"
        backup_path = os.path.join(BACKUP_DIR, backup_name)
        
        shutil.copy2(BILLS_FILE, backup_path)
        print(f"✓ Backup created: {backup_name}")
        
        # Clean up old backups
        cleanup_old_backups()
        
    except Exception as e:
        print(f"⚠ Backup error: {e}")

def cleanup_old_backups():
    """Remove old backups, keeping only the most recent ones."""
    try:
        backup_files = [f for f in os.listdir(BACKUP_DIR) 
                       if f.startswith('bills_backup_')]
        backup_files.sort(key=lambda x: os.path.getmtime(
            os.path.join(BACKUP_DIR, x)))
        
        while len(backup_files) > MAX_BACKUPS:
            oldest = backup_files.pop(0)
            os.remove(os.path.join(BACKUP_DIR, oldest))
            print(f"🗑 Removed old backup: {oldest}")
            
    except Exception as e:
        print(f"⚠ Cleanup error: {e}")

def load_bills():
    """Load bills from JSON file with error handling."""
    global bills
    try:
        with open(BILLS_FILE, 'r') as f:
            bills = json.load(f)
        print(f"✓ Loaded {len(bills)} bills")
    except FileNotFoundError:
        bills = []
        print("📝 Starting with empty bills list")
    except json.JSONDecodeError:
        bills = []
        print("⚠ Corrupted bills file. Starting fresh.")

def save_bills():
    """Save bills to JSON file with backup."""
    try:
        backup_bills()
        with open(BILLS_FILE, 'w') as f:
            json.dump(bills, f, indent=2)  # Use 2 spaces for cleaner format
        print("✓ Bills saved successfully")
    except Exception as e:
        print(f"⚠ Save error: {e}")

# 5. Input validation functions
def get_required_input(prompt):
    """Get required input with cancel option."""
    while True:
        value = input(f"{prompt}: ").strip()
        if value.lower() == 'cancel':
            return None
        if value:
            return value
        print("❌ This field is required. Please enter a value or type 'cancel' to cancel.\n")

def get_optional_input(prompt):
    """Get optional input with cancel option."""
    value = input(f"{prompt} (optional): ").strip()
    if value.lower() == 'cancel':
        return None
    return value or ""  # Return empty string if nothing entered

def get_valid_date(prompt):
    """Get a valid date input."""
    while True:
        date_str = get_required_input(prompt)
        if date_str is None:  # User cancelled
            return None
        try:
            datetime.strptime(date_str, DATE_FORMAT)
            return date_str
        except ValueError:
            print(f"❌ Invalid date format. Please use {DATE_FORMAT}")

def get_yes_no(prompt):
    """Get yes/no input."""
    while True:
        response = input(prompt).strip().lower()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        print("Please enter 'yes' or 'no'")

# 6. Core bill management functions
def add_bill():
    print("\n--- Add a New Bill ---")
    print("Type 'cancel' at any time to cancel.\n")

    # Ask for bill name and check for duplicates
    while True:
        name = get_required_input("Enter the name of the bill")
        if name is None:
            print("Bill addition cancelled.")
            return
        
        # Check for duplicates
        if any(bill['name'].lower() == name.lower() for bill in bills):
            print(f"❌ A bill with the name '{name}' already exists. Please enter a different name.\n")
        else:
            break

    # Get due date
    due_date = get_required_input("Enter the due date of the bill (YYYY-MM-DD)")
    if due_date is None:
        print("Bill addition cancelled.")
        return
    
    # Get optional fields
    web_page = get_optional_input("Enter the web page for the bill")
    if web_page is None:
        print("Bill addition cancelled.")
        return
    
    login_info = get_optional_input("Enter the login information for the bill")
    if login_info is None:
        print("Bill addition cancelled.")
        return

    password = get_optional_input("Enter the password for the bill")
    if password is None:
        print("Bill addition cancelled.")
        return

    # Create and save bill
    bill = {
        "name": name,
        "due_date": due_date,
        "web_page": web_page,
        "login_info": login_info,
        "password": password,
        "paid": False
    }
    bills.append(bill)
    save_bills()
    print(f"✅ Bill '{name}' added successfully!")
    input("Press Enter to continue...")

def view_bills():
    print("\n--- All Bills ---")
    if not bills:
        print("No bills found.\n")
        return
    for idx, bll in enumerate(bills, start=1):
        print(f"{idx}. {bll['name']}")
        print(f"   Due Date: {bll['due_date']}")
        print(f"   Web Page: {bll['web_page']}")
        print(f"   Login Info: {bll['login_info']}")
        print(f"   Password: {bll['password']}\n")

def edit_bill():
    print("\n--- Edit a Bill ---")
    view_bills()
    if not bills:
        return
    try:
        choice = int(input("Enter the number of the bill to edit:"))
        if 1 <= choice <= len(bills):
            bill = bills[choice - 1]
            print(f"Editing '{bill['name']}'")
            new_name = input(f"Name [{bill['name']}]: ").strip()
            if new_name:
                bill['name'] = new_name

            new_due_date = input(f"Due Date [{bill['due_date']}]: ").strip()
            if new_due_date:
                try:
                    datetime.strptime(new_due_date, '%Y-%m-%d')
                    bill['due_date'] = new_due_date
                except ValueError:
                    print("Invalid date format. Keeping the original date.")
                
            new_web_page = input(f"Web Page [{bill['web_page']}]: ").strip()
            if new_web_page:
                bill['web_page'] = new_web_page

            new_login_info = input(f"Login Info [{bill['login_info']}]: ").strip()
            if new_login_info:
                bill['login_info'] = new_login_info

            new_password = input(f"Password [{bill['password']}]: ").strip()
            if new_password:
                bill['password'] = new_password

            paid_status = input(f"Paid (yes/no) [{ 'yes' if bill.get('paid', False) else 'no' }]: ").strip().lower()
            if paid_status in ['yes', 'y']:
                bill['paid'] = True
            elif paid_status in ['no', 'n']:
                bill['paid'] = False

            save_bills()
            print(f"Bill '{bill['name']}' updated successfully.")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def delete_bill():
    print("\n--- Delete a Bill ---")
    view_bills()
    if not bills:
        return
    try:
        choice = int(input("Enter the number of the bill to delete:"))
        if 1 <= choice <= len(bills):
            bill = bills[choice - 1]
            confirm = input(f"Are you sure you want to delete '{bill['name']}'? (yes/no): ").strip().lower()
            if confirm in ['yes', 'y']:
                bills.remove(bill)
                save_bills()
                print(f"Bill '{bill['name']}' has been deleted.")
            else:
                print("Deletion cancelled.")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input.")
        print("Invalid input. Please enter a number.")

def pay_bill():
    print("\n--- Pay a Bill ---")
    view_bills()
    if not bills:
        return
    try:
        choice = int(input("Enter the number of the bill you want to pay:"))
        if 1 <= choice <= len(bills):
            bill = bills[choice - 1]
            if bill.get("paid", False):
                print("This bill has already been paid.")
                return
            # Mark the bill as paid
            bill["paid"] = True
            # Update the due date to next month (simple logic)
            try:
                current_due_date = datetime.strptime(bill['due_date'], '%Y-%m-%d')
                next_month = current_due_date.replace(day=1) + timedelta(days=32)
                new_due_date = next_month.replace(day=1)
                bill['due_date'] = new_due_date.strftime('%Y-%m-%d')
                print(f"Bill '{bill['name']}' marked as paid. Next due date set to {bill['due_date']}.")
            except ValueError:
                print("Invalid date format, Cannot update due date.")
            save_bills()
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def verify_due_bills(days=7):
    print("\n--- Due Bills ---")
    today = datetime.now()
    due_now = False
    for bill in bills:
        try:
            date_due = datetime.strptime(bill['due_date'], '%Y-%m-%d')
            delta = date_due - today
            if 0 <= delta.days <= days:
                print(f"Bill '{bill['name']}' is due on {delta.days} days {bill['due_date']}")
                due_now = True
        except ValueError:
            print(f"Invalid date format for bill {bill['name']}: {bill['due_date']}")
    if not due_now:
        print("No bills are due in the specified timeframe.\n")
    else:
        print()

# 7. Search functions
def search_bills():
    """Search bills by name, due date, or website."""
    print("\n--- Search Bills ---")
    print("Search options:")
    print("1. Search by name")
    print("2. Search by due date")
    print("3. Search by website")
    print("4. Search all fields")
    print("5. Back to main menu")
    
    choice = input("\nChoose search option (1-5): ").strip()
    
    if choice == '1':
        search_by_name()
    elif choice == '2':
        search_by_due_date()
    elif choice == '3':
        search_by_website()
    elif choice == '4':
        search_all_fields()
    elif choice == '5':
        return
    else:
        print("❌ Invalid option. Please choose 1-5.")
        input("Press Enter to continue...")
        search_bills()

def search_by_name():
    """Search bills by name (partial match)."""
    if not bills:
        print("No bills found.")
        return
    
    search_term = input("Enter bill name to search: ").strip().lower()
    if not search_term:
        print("Search term cannot be empty.")
        return
    
    results = [bill for bill in bills 
              if search_term in bill['name'].lower()]
    
    display_search_results(results, f"Bills containing '{search_term}' in name")

def search_by_due_date():
    """Search bills by due date or date range."""
    if not bills:
        print("No bills found.")
        return
    
    print("\nSearch options:")
    print("1. Exact date (YYYY-MM-DD)")
    print("2. Month and year (YYYY-MM)")
    print("3. Year only (YYYY)")
    
    option = input("Choose option (1-3): ").strip()
    
    if option == '1':
        search_term = input("Enter exact date (YYYY-MM-DD): ").strip()
        results = [bill for bill in bills if bill['due_date'] == search_term]
        display_search_results(results, f"Bills due on {search_term}")
        
    elif option == '2':
        search_term = input("Enter month and year (YYYY-MM): ").strip()
        results = [bill for bill in bills if bill['due_date'].startswith(search_term)]
        display_search_results(results, f"Bills due in {search_term}")
        
    elif option == '3':
        search_term = input("Enter year (YYYY): ").strip()
        results = [bill for bill in bills if bill['due_date'].startswith(search_term)]
        display_search_results(results, f"Bills due in {search_term}")
    else:
        print("❌ Invalid option.")

def search_by_website():
    """Search bills by website (partial match)."""
    if not bills:
        print("No bills found.")
        return
    
    search_term = input("Enter website to search: ").strip().lower()
    if not search_term:
        print("Search term cannot be empty.")
        return
    
    results = [bill for bill in bills 
              if search_term in bill.get('web_page', '').lower()]
    
    display_search_results(results, f"Bills with website containing '{search_term}'")

def search_all_fields():
    """Search across all bill fields."""
    if not bills:
        print("No bills found.")
        return
    
    search_term = input("Enter search term (searches all fields): ").strip().lower()
    if not search_term:
        print("Search term cannot be empty.")
        return
    
    results = []
    for bill in bills:
        # Search in all text fields
        searchable_text = ' '.join([
            bill.get('name', ''),
            bill.get('due_date', ''),
            bill.get('web_page', ''),
            bill.get('login_info', '')
        ]).lower()
        
        if search_term in searchable_text:
            results.append(bill)
    
    display_search_results(results, f"Bills containing '{search_term}' in any field")

def display_search_results(results, title):
    """Display search results in a formatted way."""
    print(f"\n--- {title} ---")
    
    if not results:
        print("❌ No bills found matching your search.")
        input("\nPress Enter to continue...")
        return
    
    print(f"✅ Found {len(results)} bill(s):\n")
    
    for idx, bill in enumerate(results, 1):
        status = "✓ Paid" if bill.get('paid', False) else "○ Unpaid"
        print(f"{idx:2}. {bill['name']} [{status}]")
        print(f"    Due: {bill['due_date']}")
        if bill.get('web_page'):
            print(f"    Website: {bill['web_page']}")
        if bill.get('login_info'):
            print(f"    Login: {bill['login_info']}")
        print()
    
    # Option to perform actions on search results
    print("Options:")
    print("1. View details of a specific bill")
    print("2. Pay a bill from results")
    print("3. Back to search menu")
    
    choice = input("Choose option (1-3): ").strip()
    
    if choice == '1':
        view_bill_details_from_search(results)
    elif choice == '2':
        pay_bill_from_search(results)
    elif choice == '3':
        return
    else:
        print("❌ Invalid option.")
        input("Press Enter to continue...")

def view_bill_details_from_search(results):
    """View detailed information of a bill from search results."""
    try:
        choice = int(input(f"Enter bill number (1-{len(results)}): "))
        if 1 <= choice <= len(results):
            bill = results[choice - 1]
            print(f"\n--- Bill Details: {bill['name']} ---")
            print(f"Name: {bill['name']}")
            print(f"Due Date: {bill['due_date']}")
            print(f"Status: {'✓ Paid' if bill.get('paid', False) else '○ Unpaid'}")
            print(f"Website: {bill.get('web_page', 'Not provided')}")
            print(f"Login Info: {bill.get('login_info', 'Not provided')}")
            print(f"Password: {'*' * len(bill.get('password', '')) if bill.get('password') else 'Not provided'}")
        else:
            print("❌ Invalid bill number.")
    except ValueError:
        print("❌ Please enter a valid number.")
    
    input("\nPress Enter to continue...")

def pay_bill_from_search(results):
    """Pay a bill from search results."""
    try:
        choice = int(input(f"Enter bill number to pay (1-{len(results)}): "))
        if 1 <= choice <= len(results):
            bill = results[choice - 1]
            if bill.get('paid', False):
                print(f"❌ Bill '{bill['name']}' is already paid.")
            else:
                # Find the bill in the main bills list and pay it
                for main_bill in bills:
                    if main_bill['name'] == bill['name'] and main_bill['due_date'] == bill['due_date']:
                        main_bill['paid'] = True
                        save_bills()
                        print(f"✅ Bill '{bill['name']}' marked as paid!")
                        break
        else:
            print("❌ Invalid bill number.")
    except ValueError:
        print("❌ Please enter a valid number.")
    
    input("\nPress Enter to continue...")

# 8. Sort functions (PUT ALL SORT FUNCTIONS HERE)
def sort_bills():
    """Sort bills by different criteria."""
    if not bills:
        print("❌ No bills found to sort.")
        input("Press Enter to continue...")
        return
    
    print("\n--- Sort Bills ---")
    print("Sort options:")
    print("1. 📅 Sort by due date (earliest first)")
    print("2. 📅 Sort by due date (latest first)")
    print("3. 🔤 Sort by name (A-Z)")
    print("4. 🔤 Sort by name (Z-A)")
    print("5. ✅ Sort by payment status (unpaid first)")
    print("6. ✅ Sort by payment status (paid first)")
    print("7. 🔄 Reset to original order")
    print("8. 🚪 Back to main menu")
    
    choice = input("\nChoose sort option (1-8): ").strip()
    
    if choice == '1':
        sort_by_due_date_asc()
    elif choice == '2':
        sort_by_due_date_desc()
    elif choice == '3':
        sort_by_name_asc()
    elif choice == '4':
        sort_by_name_desc()
    elif choice == '5':
        sort_by_status_unpaid_first()
    elif choice == '6':
        sort_by_status_paid_first()
    elif choice == '7':
        reset_bill_order()
    elif choice == '8':
        return
    else:
        print("❌ Invalid option. Please choose 1-8.")
        input("Press Enter to continue...")
        sort_bills()

def sort_by_due_date_asc():
    """Sort bills by due date (earliest first)."""
    global bills
    try:
        bills.sort(key=lambda bill: datetime.strptime(bill['due_date'], DATE_FORMAT))
        print("✅ Bills sorted by due date (earliest first)")
        display_sorted_bills("Bills Sorted by Due Date (Earliest First)")
    except ValueError as e:
        print(f"❌ Error sorting by date: Invalid date format found")
        input("Press Enter to continue...")

def sort_by_due_date_desc():
    """Sort bills by due date (latest first)."""
    global bills
    try:
        bills.sort(key=lambda bill: datetime.strptime(bill['due_date'], DATE_FORMAT), reverse=True)
        print("✅ Bills sorted by due date (latest first)")
        display_sorted_bills("Bills Sorted by Due Date (Latest First)")
    except ValueError as e:
        print(f"❌ Error sorting by date: Invalid date format found")
        input("Press Enter to continue...")

def sort_by_name_asc():
    """Sort bills by name (A-Z)."""
    global bills
    bills.sort(key=lambda bill: bill['name'].lower())
    print("✅ Bills sorted by name (A-Z)")
    display_sorted_bills("Bills Sorted by Name (A-Z)")

def sort_by_name_desc():
    """Sort bills by name (Z-A)."""
    global bills
    bills.sort(key=lambda bill: bill['name'].lower(), reverse=True)
    print("✅ Bills sorted by name (Z-A)")
    display_sorted_bills("Bills Sorted by Name (Z-A)")

def sort_by_status_unpaid_first():
    """Sort bills by payment status (unpaid first)."""
    global bills
    bills.sort(key=lambda bill: bill.get('paid', False))
    print("✅ Bills sorted by status (unpaid first)")
    display_sorted_bills("Bills Sorted by Status (Unpaid First)")

def sort_by_status_paid_first():
    """Sort bills by payment status (paid first)."""
    global bills
    bills.sort(key=lambda bill: bill.get('paid', False), reverse=True)
    print("✅ Bills sorted by status (paid first)")
    display_sorted_bills("Bills Sorted by Status (Paid First)")

def reset_bill_order():
    """Reset bills to original order (reload from file)."""
    global bills
    load_bills()
    print("✅ Bills reset to original order")
    display_sorted_bills("Bills in Original Order")

def display_sorted_bills(title):
    """Display sorted bills with formatting."""
    print(f"\n--- {title} ---")
    
    if not bills:
        print("❌ No bills to display.")
        input("Press Enter to continue...")
        return
    
    for idx, bill in enumerate(bills, 1):
        status = "✓ Paid" if bill.get('paid', False) else "○ Unpaid"
        
        # Add due date info for better context
        try:
            due_date = datetime.strptime(bill['due_date'], DATE_FORMAT)
            today = datetime.now()
            days_diff = (due_date - today).days
            
            if days_diff < 0:
                date_info = f"(Overdue by {abs(days_diff)} days)"
            elif days_diff == 0:
                date_info = "(Due today!)"
            elif days_diff <= 7:
                date_info = f"(Due in {days_diff} days)"
            else:
                date_info = ""
        except ValueError:
            date_info = ""
        
        print(f"{idx:2}. {bill['name']} [{status}]")
        print(f"    Due: {bill['due_date']} {date_info}")
        if bill.get('web_page'):
            print(f"    Website: {bill['web_page']}")
        print()
    
    # Options after viewing sorted bills
    print("Options:")
    print("1. 💾 Save this sort order permanently")
    print("2. 🔄 Sort again with different criteria")
    print("3. 🚪 Back to main menu")
    
    choice = input("Choose option (1-3): ").strip()
    
    if choice == '1':
        save_bills()
        print("✅ Sort order saved!")
        input("Press Enter to continue...")
    elif choice == '2':
        sort_bills()
    elif choice == '3':
        return
    else:
        print("❌ Invalid option.")
        input("Press Enter to continue...")

# 9. Main application
def display_menu():
    """Display the main menu."""
    print("\n" + "="*40)
    print("           BILLS TRACKER")
    print("="*40)
    print("1. 📝 Add a bill")
    print("2. 📋 View all bills")
    print("3. 🔍 Search bills")
    print("4. 🔄 Sort bills")  # New option
    print("5. ⏰ Check due bills")
    print("6. 💰 Pay a bill")
    print("7. ✏️  Edit a bill")
    print("8. 🗑️  Delete a bill")
    print("9. 🚪 Exit")
    print("="*40)

def main():
    """Main application loop."""
    clear_console()
    print("Welcome to Bills Tracker! 🏠💳")
    
    # Load existing bills
    load_bills()

    while True:
        display_menu()
        choice = input("Choose an option (1-9): ").strip()
        
        if choice == '1':
            clear_console()
            add_bill()
        elif choice == '2':
            clear_console()
            view_bills()
            input("\n📖 Press Enter to continue...")
        elif choice == '3':
            clear_console()
            search_bills()
        elif choice == '4':  # New sort option
            clear_console()
            sort_bills()
        elif choice == '5':
            clear_console()
            verify_due_bills()
            input("\n📖 Press Enter to continue...")
        elif choice == '6':
            clear_console()
            pay_bill()
        elif choice == '7':
            clear_console()
            edit_bill()
        elif choice == '8':
            clear_console()
            delete_bill()
        elif choice == '9':
            print("\n👋 Thank you for using Bills Tracker!")
            break
        else:
            print("❌ Invalid option. Please choose 1-9.")
            input("Press Enter to continue...")

# 10. Entry point
if __name__ == "__main__":
    main()