# 1. Imports
import json
import os
import shutil
import time
import re
import urllib.parse
import calendar
from datetime import datetime, timedelta
from colorama import Fore, Back, Style, init
from tqdm import tqdm

# Initialize colorama for Windows compatibility
init(autoreset=True)

# 2. Configuration
BILLS_FILE = 'bills.json'
BACKUP_DIR = 'backups'
MAX_BACKUPS = 5
DATE_FORMAT = '%Y-%m-%d'

bills = []

# 3. Color utility functions
class Colors:
    """Color constants and helper functions."""
    
    # Status colors
    SUCCESS = Fore.GREEN
    ERROR = Fore.RED
    WARNING = Fore.YELLOW
    INFO = Fore.CYAN
    TITLE = Fore.MAGENTA
    
    # Bill status colors
    PAID = Fore.GREEN
    UNPAID = Fore.YELLOW
    OVERDUE = Fore.RED + Style.BRIGHT
    DUE_SOON = Fore.YELLOW + Style.BRIGHT
    
    # UI colors
    MENU = Fore.BLUE + Style.BRIGHT
    PROMPT = Fore.WHITE + Style.BRIGHT
    RESET = Style.RESET_ALL

def colored_print(text, color=Colors.RESET):
    """Print text with color."""
    print(f"{color}{text}{Colors.RESET}")

def colored_input(prompt, color=Colors.PROMPT):
    """Get input with colored prompt."""
    return input(f"{color}{prompt}{Colors.RESET}")

def success_msg(message):
    """Print success message."""
    colored_print(f"✅ {message}", Colors.SUCCESS)

def error_msg(message):
    """Print error message."""
    colored_print(f"❌ {message}", Colors.ERROR)

def warning_msg(message):
    """Print warning message."""
    colored_print(f"⚠️  {message}", Colors.WARNING)

def info_msg(message):
    """Print info message."""
    colored_print(f"ℹ️  {message}", Colors.INFO)

def title_msg(message):
    """Print title message."""
    colored_print(f"🏠 {message}", Colors.TITLE + Style.BRIGHT)

# 4. Utility functions
def clear_console():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

# 5. File operations
def load_bills():
    """Load bills from JSON file with colored feedback."""
    global bills
    try:
        with open(BILLS_FILE, 'r') as f:
            bills = json.load(f)
        
        # Migrate bills to include reminder_days if missing
        migrated = False
        for bill in bills:
            if 'reminder_days' not in bill:
                bill['reminder_days'] = 7  # Default to 7 days
                migrated = True
        
        if migrated:
            save_bills()
            info_msg("Bills migrated to include custom reminder periods")
        
        success_msg(f"Loaded {len(bills)} bills")
    except FileNotFoundError:
        bills = []
        info_msg("Starting with empty bills list")
    except json.JSONDecodeError:
        bills = []
        error_msg("Corrupted bills file. Starting fresh.")

def save_bills():
    """Save bills (with progress if many bills)."""
    try:
        # Always create backup first
        backup_bills_with_progress()
        
        # Save the bills
        with open(BILLS_FILE, 'w') as f:
            json.dump(bills, f, indent=2)
        success_msg("Bills saved successfully")
        
    except Exception as e:
        error_msg(f"Save error: {e}")

def backup_bills():
    """Main backup function with progress."""
    backup_bills_with_progress()

def backup_bills_with_progress():
    """Create backup with progress indicator."""
    try:
        # Step 1: Check directories
        with ProgressBar.create_bar(100, "🔍 Checking directories", "blue") as pbar:
            if not os.path.exists(BACKUP_DIR):
                os.makedirs(BACKUP_DIR)
            pbar.update(50)
            
            if not os.path.exists(BILLS_FILE):
                info_msg("No bills.json found. No backup needed.")
                pbar.update(100)
                return
            pbar.update(100)
        
        # Step 2: Create backup
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"bills_backup_{timestamp}.json"
        backup_path = os.path.join(BACKUP_DIR, backup_name)
        
        with ProgressBar.create_bar(100, "💾 Creating backup", "green") as pbar:
            # Simulate file copy with progress
            file_size = os.path.getsize(BILLS_FILE)
            chunk_size = max(1024, file_size // 10)  # 10 chunks minimum
            
            with open(BILLS_FILE, 'rb') as src, open(backup_path, 'wb') as dst:
                copied = 0
                while True:
                    chunk = src.read(chunk_size)
                    if not chunk:
                        break
                    dst.write(chunk)
                    copied += len(chunk)
                    progress = min(95, (copied / file_size) * 100)
                    pbar.n = progress
                    pbar.refresh()
                    time.sleep(0.01)  # Small delay for visual effect
                pbar.update(100 - pbar.n)
        
        success_msg(f"Backup created: {backup_name}")
        
        # Step 3: Cleanup old backups
        cleanup_old_backups_with_progress()
        
    except Exception as e:
        error_msg(f"Backup error: {e}")

def cleanup_old_backups_with_progress():
    """Remove old backups with progress indicator."""
    try:
        with ProgressBar.create_bar(100, "🧹 Cleaning old backups", "yellow") as pbar:
            backup_files = [f for f in os.listdir(BACKUP_DIR) 
                           if f.startswith('bills_backup_')]
            pbar.update(30)
            
            backup_files.sort(key=lambda x: os.path.getmtime(
                os.path.join(BACKUP_DIR, x)))
            pbar.update(60)
            
            removed_count = 0
            while len(backup_files) > MAX_BACKUPS:
                oldest = backup_files.pop(0)
                os.remove(os.path.join(BACKUP_DIR, oldest))
                removed_count += 1
                info_msg(f"Removed old backup: {oldest}")
                time.sleep(0.1)  # Small delay for visual feedback
            
            pbar.update(100)
            
            if removed_count > 0:
                success_msg(f"Cleaned up {removed_count} old backup(s)")
            else:
                info_msg("No old backups to clean")
                
    except Exception as e:
        warning_msg(f"Cleanup error: {e}")

def save_bills_with_progress():
    """Save bills with progress indicator."""
    try:
        # Create backup first
        backup_bills_with_progress()
        
        # Save bills with progress
        with ProgressBar.create_bar(100, "💾 Saving bills", "green") as pbar:
            pbar.update(20)
            
            # Convert to JSON with progress simulation
            json_data = json.dumps(bills, indent=2)
            pbar.update(60)
            
            # Write to file
            with open(BILLS_FILE, 'w') as f:
                f.write(json_data)
            pbar.update(100)
            
        success_msg("Bills saved successfully")
        
    except Exception as e:
        error_msg(f"Save error: {e}")

# 6. Input validation functions
def get_required_input(prompt):
    """Get required input with cancel option and colors."""
    while True:
        value = colored_input(f"{prompt}: ", Colors.PROMPT).strip()
        if value.lower() == 'cancel':
            return None
        if value:
            return value
        error_msg("This field is required. Please enter a value or type 'cancel' to cancel.")

def get_optional_input(prompt):
    """Get optional input with cancel option and colors."""
    value = colored_input(f"{prompt} (optional): ", Colors.PROMPT).strip()
    if value.lower() == 'cancel':
        return None
    return value or ""

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

# 6.2 Enhanced validation functions
def validate_url(url):
    """Validate URL format and return cleaned URL."""
    if not url.strip():
        return ""  # Empty URLs are allowed
    
    # Clean the URL
    url = url.strip()
    
    # Add protocol if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        # Parse URL to validate structure
        parsed = urllib.parse.urlparse(url)
        
        # Check if domain is valid
        if not parsed.netloc:
            return None
        
        # Basic domain validation
        domain_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
        if not re.match(domain_pattern, parsed.netloc.split(':')[0]):
            return None
            
        return url
    except Exception:
        return None

def validate_email(email):
    """Validate email format."""
    if not email.strip():
        return ""  # Empty emails are allowed
    
    email = email.strip().lower()
    
    # Basic email regex pattern
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(email_pattern, email):
        return email
    return None

def validate_date_range(start_date, end_date):
    """Validate that start_date is before end_date."""
    try:
        start = datetime.strptime(start_date, DATE_FORMAT)
        end = datetime.strptime(end_date, DATE_FORMAT)
        return start <= end
    except ValueError:
        return False

def validate_reminder_days(days_str):
    """Validate reminder days input (1-365)."""
    try:
        days = int(days_str)
        return 1 <= days <= 365
    except ValueError:
        return False

def validate_future_date(date_str):
    """Validate that the date is not too far in the past (more than 1 year)."""
    try:
        date_obj = datetime.strptime(date_str, DATE_FORMAT)
        today = datetime.now()
        one_year_ago = today - timedelta(days=365)
        
        if date_obj < one_year_ago:
            return False, f"Date is more than 1 year in the past. Please enter a more recent date."
        
        # Warning for dates more than 5 years in the future
        five_years_future = today + timedelta(days=5*365)
        if date_obj > five_years_future:
            return False, f"Date is more than 5 years in the future. Please check the date."
            
        return True, None
    except ValueError:
        return False, "Invalid date format"

def get_valid_url(prompt):
    """Get a valid URL input with validation."""
    while True:
        url = input(f"{Colors.PROMPT}{prompt}{Colors.RESET}").strip()
        
        if url.lower() == 'cancel':
            return None
            
        if not url:  # Empty URL is allowed
            return ""
            
        validated_url = validate_url(url)
        if validated_url is not None:
            if validated_url != url:
                colored_print(f"✅ URL corrected to: {validated_url}", Colors.SUCCESS)
            return validated_url
        else:
            error_msg("Invalid URL format. Please enter a valid website URL (e.g., example.com)")

def get_valid_email(prompt):
    """Get a valid email input with validation."""
    while True:
        email = input(f"{Colors.PROMPT}{prompt}{Colors.RESET}").strip()
        
        if email.lower() == 'cancel':
            return None
            
        if not email:  # Empty email is allowed
            return ""
            
        validated_email = validate_email(email)
        if validated_email is not None:
            return validated_email
        else:
            error_msg("Invalid email format. Please enter a valid email address (e.g., user@example.com)")

def get_valid_reminder_days(prompt, default=7):
    """Get valid reminder days with validation."""
    while True:
        days_input = input(f"{Colors.PROMPT}{prompt} [default: {default}]: {Colors.RESET}").strip()
        
        if days_input.lower() == 'cancel':
            return None
            
        if not days_input:
            return default
            
        if validate_reminder_days(days_input):
            return int(days_input)
        else:
            error_msg("Please enter a number between 1 and 365 days")

def get_valid_date_with_range_check(prompt):
    """Get a valid date input with range validation."""
    while True:
        date_str = get_required_input(prompt)
        if date_str is None:  # User cancelled
            return None
            
        try:
            datetime.strptime(date_str, DATE_FORMAT)
            
            # Check date range
            is_valid, error_msg_text = validate_future_date(date_str)
            if not is_valid:
                error_msg(error_msg_text)
                continue
                
            return date_str
        except ValueError:
            error_msg(f"Invalid date format. Please use {DATE_FORMAT} (YYYY-MM-DD)")

# 6.1 Billing cycle constants and functions
class BillingCycle:
    """Billing cycle constants and utilities."""
    WEEKLY = "weekly"
    BI_WEEKLY = "bi-weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    SEMI_ANNUALLY = "semi-annually"
    ANNUALLY = "annually"
    ONE_TIME = "one-time"
    
    @staticmethod
    def get_all_cycles():
        return [
            BillingCycle.WEEKLY,
            BillingCycle.BI_WEEKLY,
            BillingCycle.MONTHLY,
            BillingCycle.QUARTERLY,
            BillingCycle.SEMI_ANNUALLY,
            BillingCycle.ANNUALLY,
            BillingCycle.ONE_TIME
        ]
    
    @staticmethod
    def get_cycle_description(cycle):
        descriptions = {
            BillingCycle.WEEKLY: "Every 7 days",
            BillingCycle.BI_WEEKLY: "Every 14 days",
            BillingCycle.MONTHLY: "Every month",
            BillingCycle.QUARTERLY: "Every 3 months",
            BillingCycle.SEMI_ANNUALLY: "Every 6 months",
            BillingCycle.ANNUALLY: "Every 12 months",
            BillingCycle.ONE_TIME: "One-time payment (no recurrence)"
        }
        return descriptions.get(cycle, "Unknown cycle")

def get_billing_cycle():
    """Get billing cycle from user input."""
    print("\n--- Select Billing Cycle ---")
    cycles = BillingCycle.get_all_cycles()
    
    for idx, cycle in enumerate(cycles, 1):
        description = BillingCycle.get_cycle_description(cycle)
        print(f"{idx}. {cycle.title()} - {description}")
    
    while True:
        try:
            choice = colored_input(f"\nChoose billing cycle (1-{len(cycles)}) or 'cancel': ", Colors.PROMPT).strip()
            
            if choice.lower() == 'cancel':
                return None
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(cycles):
                selected_cycle = cycles[choice_num - 1]
                success_msg(f"Selected: {selected_cycle.title()}")
                return selected_cycle
            else:
                error_msg(f"Please choose a number between 1 and {len(cycles)}")
        except ValueError:
            error_msg("Please enter a valid number or 'cancel'")

def calculate_next_due_date(current_due_date, billing_cycle):
    """Calculate the next due date based on billing cycle."""
    try:
        current_date = datetime.strptime(current_due_date, DATE_FORMAT)
    except ValueError:
        return current_due_date  # Return original if can't parse
    
    if billing_cycle == BillingCycle.WEEKLY:
        next_date = current_date + timedelta(days=7)
    elif billing_cycle == BillingCycle.BI_WEEKLY:
        next_date = current_date + timedelta(days=14)
    elif billing_cycle == BillingCycle.MONTHLY:
        # Handle month rollover properly
        next_date = add_months(current_date, 1)
    elif billing_cycle == BillingCycle.QUARTERLY:
        next_date = add_months(current_date, 3)
    elif billing_cycle == BillingCycle.SEMI_ANNUALLY:
        next_date = add_months(current_date, 6)
    elif billing_cycle == BillingCycle.ANNUALLY:
        next_date = add_months(current_date, 12)
    elif billing_cycle == BillingCycle.ONE_TIME:
        return current_due_date  # No change for one-time bills
    else:
        return current_due_date  # Unknown cycle, no change
    
    return next_date.strftime(DATE_FORMAT)

def add_months(date, months):
    """Add months to a date, handling month/year rollover properly."""
    month = date.month - 1 + months
    year = date.year + month // 12
    month = month % 12 + 1
    
    # Handle day overflow (e.g., Jan 31 + 1 month should be Feb 28/29)
    day = date.day
    max_day = calendar.monthrange(year, month)[1]
    if day > max_day:
        day = max_day
    
    return date.replace(year=year, month=month, day=day)

def get_billing_cycle_color(cycle):
    """Get color for billing cycle display."""
    color_map = {
        BillingCycle.WEEKLY: Colors.DUE_SOON,
        BillingCycle.BI_WEEKLY: Colors.WARNING,
        BillingCycle.MONTHLY: Colors.INFO,
        BillingCycle.QUARTERLY: Colors.SUCCESS,
        BillingCycle.SEMI_ANNUALLY: Colors.TITLE,
        BillingCycle.ANNUALLY: Colors.MENU,
        BillingCycle.ONE_TIME: Colors.ERROR
    }
    return color_map.get(cycle, Colors.RESET)

# 7. Core bill management functions
def add_bill():
    """Add a new bill with colored feedback."""
    title_msg("Add a New Bill")
    info_msg("Type 'cancel' at any time to cancel.")
    
    # Ask for bill name and check for duplicates
    while True:
        name = get_required_input("Enter the name of the bill")
        if name is None:
            warning_msg("Bill addition cancelled.")
            return
        
        # Check for duplicates
        if any(bill['name'].lower() == name.lower() for bill in bills):
            error_msg(f"A bill with the name '{name}' already exists. Please enter a different name.")
        else:
            break

    # Get due date with validation
    due_date = get_valid_date_with_range_check("Enter the due date of the bill (YYYY-MM-DD)")
    if due_date is None:
        warning_msg("Bill addition cancelled.")
        return
    
    # Get billing cycle
    billing_cycle = get_billing_cycle()
    if billing_cycle is None:
        warning_msg("Bill addition cancelled.")
        return
    
    # Get reminder period
    reminder_days = get_valid_reminder_days("Enter reminder days before due date (1-365)")
    if reminder_days is None:
        warning_msg("Bill addition cancelled.")
        return
    
    # Get optional fields with validation
    web_page = get_valid_url("Enter the web page for the bill (optional)")
    if web_page is None:
        warning_msg("Bill addition cancelled.")
        return
    
    login_info = get_optional_input("Enter the login information for the bill")
    if login_info is None:
        warning_msg("Bill addition cancelled.")
        return

    password = get_optional_input("Enter the password for the bill")
    if password is None:
        warning_msg("Bill addition cancelled.")
        return

    # Create and save bill
    bill = {
        "name": name,
        "due_date": due_date,
        "web_page": web_page,
        "login_info": login_info,
        "password": password,
        "paid": False,
        "billing_cycle": billing_cycle,
        "reminder_days": reminder_days
    }
    bills.append(bill)
    save_bills()
    success_msg(f"Bill '{name}' added successfully with {billing_cycle} billing cycle!")
    colored_input("Press Enter to continue...", Colors.INFO)

def display_menu():
    """Display the main menu with colors."""
    print("\n" + Colors.MENU + "="*40)
    title_msg("BILLS TRACKER")
    print(Colors.MENU + "="*40 + Colors.RESET)
    
    print(f"{Colors.MENU}1.{Colors.RESET} 📝 Add a bill")
    print(f"{Colors.MENU}2.{Colors.RESET} 📋 View all bills")
    print(f"{Colors.MENU}3.{Colors.RESET} 🔍 Search bills")
    print(f"{Colors.MENU}4.{Colors.RESET} 🔄 Sort bills")
    print(f"{Colors.MENU}5.{Colors.RESET} ⏰ Check due bills")
    print(f"{Colors.MENU}6.{Colors.RESET} 💰 Pay a bill")
    print(f"{Colors.MENU}7.{Colors.RESET} ✏️  Edit a bill")
    print(f"{Colors.MENU}8.{Colors.RESET} 🗑️  Delete a bill")
    print(f"{Colors.MENU}9.{Colors.RESET} 🚪 Exit")
    print(Colors.MENU + "="*40 + Colors.RESET)

def view_bills():
    """View all bills with color coding."""
    title_msg("All Bills")
    
    if not bills:
        warning_msg("No bills found.")
        return
    
    today = datetime.now()
    
    for idx, bill in enumerate(bills, 1):
        # Determine bill status and color
        if bill.get('paid', False):
            status = f"{Colors.PAID}✓ Paid{Colors.RESET}"
        else:
            status = f"{Colors.UNPAID}○ Unpaid{Colors.RESET}"
        
        # Calculate days until due
        try:
            due_date = datetime.strptime(bill['due_date'], DATE_FORMAT)
            days_diff = (due_date - today).days
            
            if days_diff < 0:
                date_info = f"{Colors.OVERDUE}(Overdue by {abs(days_diff)} days!){Colors.RESET}"
                status = f"{Colors.OVERDUE}! OVERDUE{Colors.RESET}"
            elif days_diff == 0:
                date_info = f"{Colors.DUE_SOON}(Due TODAY!){Colors.RESET}"
            elif days_diff <= 7:
                date_info = f"{Colors.DUE_SOON}(Due in {days_diff} days){Colors.RESET}"
            else:
                date_info = ""
        except ValueError:
            date_info = f"{Colors.ERROR}(Invalid date){Colors.RESET}"
        
        # Print bill info with colors
        print(f"{Colors.INFO}{idx:2}.{Colors.RESET} {Colors.TITLE}{bill['name']}{Colors.RESET} [{status}]")
        print(f"    Due: {Colors.INFO}{bill['due_date']}{Colors.RESET} {date_info}")
        
        # Show billing cycle
        cycle = bill.get('billing_cycle', 'monthly')
        cycle_color = get_billing_cycle_color(cycle)
        print(f"    Cycle: {cycle_color}{cycle.title()}{Colors.RESET}")
        
        # Show reminder period
        reminder_days = bill.get('reminder_days', 7)
        if reminder_days == 1:
            reminder_text = "1 day before"
        else:
            reminder_text = f"{reminder_days} days before"
        print(f"    Reminder: {Colors.WARNING}⏰ {reminder_text}{Colors.RESET}")
        
        if bill.get('web_page'):
            print(f"    Website: {Colors.INFO}{bill['web_page']}{Colors.RESET}")
        if bill.get('login_info'):
            print(f"    Login: {Colors.INFO}{bill['login_info']}{Colors.RESET}")
        print()

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
                # Validate date format and range
                try:
                    datetime.strptime(new_due_date, '%Y-%m-%d')
                    is_valid, error_msg_text = validate_future_date(new_due_date)
                    if is_valid:
                        bill['due_date'] = new_due_date
                    else:
                        error_msg(error_msg_text + " Keeping the original date.")
                except ValueError:
                    error_msg("Invalid date format. Keeping the original date.")
                
            # Website with validation
            print(f"Current website: {bill.get('web_page', 'Not provided')}")
            new_web_page = input(f"Web Page [{bill['web_page']}]: ").strip()
            if new_web_page:
                if new_web_page.lower() == 'clear':
                    bill['web_page'] = ""
                    success_msg("Website cleared.")
                else:
                    validated_url = validate_url(new_web_page)
                    if validated_url is not None:
                        bill['web_page'] = validated_url
                        if validated_url != new_web_page:
                            success_msg(f"Website corrected to: {validated_url}")
                    else:
                        error_msg("Invalid URL format. Keeping the original website.")

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

            # Billing cycle
            current_cycle = bill.get('billing_cycle', 'monthly')
            print(f"\nCurrent billing cycle: {current_cycle.title()}")
            change_cycle = input("Change billing cycle? (yes/no): ").strip().lower()
            if change_cycle in ['yes', 'y']:
                new_billing_cycle = get_billing_cycle()
                if new_billing_cycle is not None:
                    bill['billing_cycle'] = new_billing_cycle
                    success_msg(f"Billing cycle updated to {new_billing_cycle}")

            # Reminder period
            current_reminder = bill.get('reminder_days', 7)
            print(f"\nCurrent reminder period: {current_reminder} days before due date")
            change_reminder = input("Change reminder period? (yes/no): ").strip().lower()
            if change_reminder in ['yes', 'y']:
                new_reminder_days = get_valid_reminder_days("Enter new reminder days before due date (1-365)", bill.get('reminder_days', 7))
                if new_reminder_days is not None:
                    bill['reminder_days'] = new_reminder_days
                    success_msg(f"Reminder period updated to {new_reminder_days} days")

            save_bills()
            success_msg(f"Bill '{bill['name']}' updated successfully.")
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
    """Pay a bill with enhanced user experience."""
    print("\n--- Pay a Bill ---")
    view_bills()
    if not bills:
        return
    
    # Filter unpaid bills for better user experience
    unpaid_bills = [bill for bill in bills if not bill.get('paid', False)]
    if not unpaid_bills:
        warning_msg("All bills are already paid! 🎉")
        input("Press Enter to continue...")
        return
    
    try:
        choice = int(colored_input("Enter the number of the bill you want to pay: ", Colors.PROMPT))
        if 1 <= choice <= len(bills):
            bill = bills[choice - 1]
            if bill.get("paid", False):
                warning_msg(f"Bill '{bill['name']}' has already been paid.")
                input("Press Enter to continue...")
                return
            
            # Get billing cycle info
            billing_cycle = bill.get('billing_cycle', BillingCycle.MONTHLY)
            
            if billing_cycle == BillingCycle.ONE_TIME:
                # One-time bills just get marked as paid
                bill["paid"] = True
                success_msg(f"One-time bill '{bill['name']}' marked as paid and completed!")
            else:
                # For recurring bills, ask user preference
                print(f"\n'{bill['name']}' is a {billing_cycle} recurring bill.")
                print("Payment options:")
                print("1. 💰 Pay and advance to next billing cycle (recommended)")
                print("2. ✅ Mark as permanently paid (stops recurring)")
                
                payment_choice = colored_input("Choose option (1-2): ", Colors.PROMPT).strip()
                
                if payment_choice == '1':
                    # Standard recurring bill payment
                    old_due_date = bill['due_date']
                    new_due_date = calculate_next_due_date(bill['due_date'], billing_cycle)
                    bill['due_date'] = new_due_date
                    bill["paid"] = False  # Unpaid for next cycle
                    
                    success_msg(f"Bill '{bill['name']}' marked as paid!")
                    info_msg(f"Next due date ({billing_cycle}): {new_due_date}")
                elif payment_choice == '2':
                    # Mark as permanently paid
                    bill["paid"] = True
                    success_msg(f"Bill '{bill['name']}' marked as permanently paid!")
                    warning_msg("This bill will no longer appear in due bills until you manually edit it.")
                else:
                    error_msg("Invalid choice. Payment cancelled.")
                    input("Press Enter to continue...")
                    return
            
            save_bills()
            colored_input("\nPress Enter to continue...", Colors.INFO)
        else:
            error_msg("Invalid selection. Please choose a valid bill number.")
            input("Press Enter to continue...")
    except ValueError:
        error_msg("Invalid input. Please enter a valid number.")
        input("Press Enter to continue...")

def verify_due_bills(days=None):
    """Check for due bills with color highlighting. If days=None, use each bill's custom reminder period."""
    if days is None:
        title_msg("Bills Due Based on Custom Reminder Periods")
    else:
        title_msg(f"Bills Due Within {days} Days")
    
    today = datetime.now()
    due_bills = []
    
    for bill in bills:
        if bill.get('paid', False):
            continue  # Skip paid bills
            
        try:
            due_date = datetime.strptime(bill['due_date'], DATE_FORMAT)
            days_diff = (due_date - today).days
            
            # Use custom reminder period if days parameter is None
            if days is None:
                reminder_period = bill.get('reminder_days', 7)
                if days_diff <= reminder_period:
                    due_bills.append((bill, days_diff, reminder_period))
            else:
                # Use provided days parameter
                if days_diff <= days:
                    due_bills.append((bill, days_diff, days))
        except ValueError:
            continue
    
    if not due_bills:
        if days is None:
            success_msg("No bills are due based on your custom reminder periods! 🎉")
        else:
            success_msg("No bills are due soon! 🎉")
        return
    
    # Sort by days until due
    due_bills.sort(key=lambda x: x[1])
    
    for bill, days_diff, reminder_period in due_bills:
        if days_diff < 0:
            colored_print(f"🚨 {bill['name']} - OVERDUE by {abs(days_diff)} days!", Colors.OVERDUE)
        elif days_diff == 0:
            colored_print(f"🔥 {bill['name']} - DUE TODAY!", Colors.DUE_SOON)
        elif days_diff <= 3:
            colored_print(f"⚠️  {bill['name']} - Due in {days_diff} days", Colors.WARNING)
        else:
            colored_print(f"📅 {bill['name']} - Due in {days_diff} days", Colors.INFO)
        
        # Show reminder period for custom reminders
        if days is None:
            colored_print(f"   ⏰ Reminder set for {reminder_period} days before due date", Colors.INFO)
    print()

def verify_due_bills_paginated(days=None, items_per_page=10):
    """Check for due bills with pagination. If days=None, use each bill's custom reminder period."""
    if days is None:
        title_msg("Bills Due Based on Custom Reminder Periods")
    else:
        title_msg(f"Bills Due Within {days} Days")
    
    if not bills:
        warning_msg("No bills found.")
        return
    
    # Get due bills
    due_bills = get_due_bills(days)
    
    if not due_bills:
        if days is None:
            success_msg("No bills are due based on your custom reminder periods! 🎉")
        else:
            success_msg("No bills are due soon! 🎉")
        input("Press Enter to continue...")
        return
    
    # Sort by urgency (overdue first, then by days)
    due_bills.sort(key=lambda x: (x[1] >= 0, x[1]))  # Overdue first, then by days
    
    paginator = Paginator(due_bills, items_per_page)
    
    while True:
        clear_console()
        title_msg(f"Bills Due Within {days} Days")
        
        # Display current page of due bills
        current_due_bills = paginator.get_page()
        display_due_bills_page(current_due_bills, paginator)
        
        # Display pagination controls
        display_pagination_controls(paginator)
        
        # Additional options
        print("\nDue Bills Options:")
        print("1. 💰 Pay a bill from this list")
        print("2. 💳 Pay multiple bills")
        print("3. 📅 Change days filter")
        
        choice = colored_input("\nEnter your choice: ", Colors.PROMPT).strip().lower()
        
        if choice == 'n' and paginator.get_page_info()['has_next']:
            paginator.next_page()
        elif choice == 'p' and paginator.get_page_info()['has_prev']:
            paginator.prev_page()
        elif choice == 'g':
            goto_page(paginator)
        elif choice == 's':
            new_size = change_page_size()
            if new_size:
                paginator = Paginator(due_bills, new_size)
        elif choice == '1':
            pay_bill_from_due_list_paginated(current_due_bills, paginator)
        elif choice == '2':
            bulk_pay_bills_from_due_list(due_bills)
        elif choice == '3':
            new_days = change_days_filter()
            if new_days:
                return verify_due_bills_paginated(new_days, items_per_page)
        elif choice == 'b':
            break
        else:
            error_msg("Invalid option.")
            input("Press Enter to continue...")

def get_due_bills(days=None):
    """Get bills due within specified days. If days=None, use each bill's custom reminder period."""
    today = datetime.now()
    due_bills = []
    
    for bill in bills:
        if bill.get('paid', False):
            continue  # Skip paid bills
            
        try:
            due_date = datetime.strptime(bill['due_date'], DATE_FORMAT)
            days_diff = (due_date - today).days
            
            # Use custom reminder period if days parameter is None
            if days is None:
                reminder_period = bill.get('reminder_days', 7)
                if days_diff <= reminder_period:
                    due_bills.append((bill, days_diff))
            else:
                # Use provided days parameter
                if days_diff <= days:
                    due_bills.append((bill, days_diff))
        except ValueError:
            continue  # Skip invalid dates
    
    return due_bills

def display_due_bills_page(current_due_bills, paginator):
    """Display a page of due bills with urgency indicators."""
    page_info = paginator.get_page_info()
    
    success_msg(f"Found {page_info['total_items']} bills due soon:")
    print()
    
    for idx, (bill, days_diff) in enumerate(current_due_bills, 1):
        actual_number = (paginator.current_page - 1) * paginator.items_per_page + idx
        
        # Determine bill status and color
        if bill.get('paid', False):
            status = f"{Colors.PAID}✓ Paid{Colors.RESET}"
        else:
            status = f"{Colors.UNPAID}○ Unpaid{Colors.RESET}"
        
        # Override status for overdue bills
        if days_diff < 0:
            status = f"{Colors.OVERDUE}! OVERDUE{Colors.RESET}"
        
        # Determine urgency and color
        if days_diff < 0:
            urgency = f"{Colors.OVERDUE}🚨 OVERDUE by {abs(days_diff)} days!{Colors.RESET}"
        elif days_diff == 0:
            urgency = f"{Colors.DUE_SOON}🔥 DUE TODAY!{Colors.RESET}"
        elif days_diff <= 3:
            urgency = f"{Colors.WARNING}⚠️  Due in {days_diff} days{Colors.RESET}"
        else:
            urgency = f"{Colors.INFO}📅 Due in {days_diff} days{Colors.RESET}"
        
        print(f"{Colors.INFO}{actual_number:3}.{Colors.RESET} {Colors.TITLE}{bill['name']}{Colors.RESET} [{status}]")
        print(f"     {urgency}")
        print(f"     Due Date: {Colors.INFO}{bill['due_date']}{Colors.RESET}")
        if bill.get('web_page'):
            print(f"     Website: {Colors.INFO}{bill['web_page'][:40]}{'...' if len(bill.get('web_page', '')) > 40 else ''}{Colors.RESET}")
        if bill.get('login_info'):
            print(f"     Login: {Colors.INFO}{bill['login_info'][:30]}{'...' if len(bill.get('login_info', '')) > 30 else ''}{Colors.RESET}")
        print()

def change_days_filter():
    """Change the number of days for due bill filter."""
    try:
        days = int(colored_input("Enter number of days to check (1-365): ", Colors.PROMPT))
        if 1 <= days <= 365:
            success_msg(f"Filter changed to {days} days")
            return days
        else:
            error_msg("Days must be between 1 and 365")
    except ValueError:
        error_msg("Please enter a valid number")
    
    input("Press Enter to continue...")
    return None

# 8. Search functions
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

def search_all_fields_with_progress(search_term):
    """Search across all bill fields with progress."""
    if not bills:
        warning_msg("No bills found.")
        return []
    
    results = []
    search_term_lower = search_term.lower()
    
    with ProgressBar.create_bar(len(bills), "🔍 Searching bills", "blue") as pbar:
        for bill in bills:
            # Search in all text fields
            searchable_text = ' '.join([
                bill.get('name', ''),
                bill.get('due_date', ''),
                bill.get('web_page', ''),
                bill.get('login_info', '')
            ]).lower()
            
            if search_term_lower in searchable_text:
                results.append(bill)
            
            pbar.update(1)
            time.sleep(0.02)  # Small delay for visual effect
    
    return results

def search_all_fields():
    """Search across all bill fields with progress indicator."""
    if not bills:
        warning_msg("No bills found.")
        return
    
    search_term = input("Enter search term (searches all fields): ").strip()
    if not search_term:
        error_msg("Search term cannot be empty.")
        return
    
    results = search_all_fields_with_progress(search_term)
    display_search_results(results, f"Bills containing '{search_term}' in any field")

def display_search_results(results, title):
    """Display search results with automatic pagination."""
    if len(results) > 10:
        display_search_results_paginated(results, title)
    else:
        display_search_results_simple(results, title)

def display_search_results_simple(results, title):
    """Display search results without pagination (for small result sets)."""
    colored_print(f"\n--- {title} ---", Colors.TITLE)
    
    if not results:
        error_msg("No bills found matching your search.")
        input("\nPress Enter to continue...")
        return
    
    success_msg(f"Found {len(results)} bill(s):")
    print()
    
    today = datetime.now()
    
    for idx, bill in enumerate(results, 1):
        # Determine bill status and color (same logic as view_bills)
        if bill.get('paid', False):
            status = f"{Colors.PAID}✓ Paid{Colors.RESET}"
        else:
            status = f"{Colors.UNPAID}○ Unpaid{Colors.RESET}"
        
        # Calculate days until due
        try:
            due_date = datetime.strptime(bill['due_date'], DATE_FORMAT)
            days_diff = (due_date - today).days
            
            if days_diff < 0:
                date_info = f"{Colors.OVERDUE}(Overdue by {abs(days_diff)} days!){Colors.RESET}"
                status = f"{Colors.OVERDUE}! OVERDUE{Colors.RESET}"
            elif days_diff == 0:
                date_info = f"{Colors.DUE_SOON}(Due TODAY!){Colors.RESET}"
            elif days_diff <= 7:
                date_info = f"{Colors.DUE_SOON}(Due in {days_diff} days){Colors.RESET}"
            else:
                date_info = ""
        except ValueError:
            date_info = f"{Colors.ERROR}(Invalid date){Colors.RESET}"
        
        # Display bill with colors (same format as view_bills)
        print(f"{Colors.INFO}{idx:2}.{Colors.RESET} {Colors.TITLE}{bill['name']}{Colors.RESET} [{status}]")
        print(f"    Due: {Colors.INFO}{bill['due_date']}{Colors.RESET} {date_info}")
        
        if bill.get('web_page'):
            print(f"    Website: {Colors.INFO}{bill['web_page']}{Colors.RESET}")
        if bill.get('login_info'):
            print(f"    Login: {Colors.INFO}{bill['login_info']}{Colors.RESET}")
        print()
    
    # Keep the existing options for simple display
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
        error_msg("Invalid option.")
        input("Press Enter to continue...")

def display_search_results_paginated(results, title, items_per_page=10):
    """Display search results with pagination."""
    if not results:
        print(f"\n--- {title} ---")
        error_msg("No bills found matching your search.")
        input("\nPress Enter to continue...")
        return
    
    paginator = Paginator(results, items_per_page)
    
    while True:
        clear_console()
        colored_print(f"--- {title} ---", Colors.TITLE)
        
        # Display current page of results
        current_results = paginator.get_page()
        display_search_results_page(current_results, paginator)
        
        # Display pagination controls
        display_pagination_controls(paginator)
        
        # Additional options for search results
        print("\nSearch Result Options:")
        print("1. 👁️  View details of a bill")
        print("2. 💰 Pay a bill from results")
        print("3. ✏️  Edit a bill from results")
        
        # Get user input
        choice = colored_input("\nEnter your choice: ", Colors.PROMPT).strip().lower()
        
        if choice == 'n' and paginator.get_page_info()['has_next']:
            paginator.next_page()
        elif choice == 'p' and paginator.get_page_info()['has_prev']:
            paginator.prev_page()
        elif choice == 'g':
            goto_page(paginator)
        elif choice == 's':
            new_size = change_page_size()
            if new_size:
                paginator = Paginator(results, new_size)
        elif choice == '1':
            view_bill_details_from_search_paginated(current_results, paginator)
        elif choice == '2':
            pay_bill_from_search_paginated(current_results, paginator)
        elif choice == '3':
            edit_bill_from_search_paginated(current_results, paginator)
        elif choice == 'b':
            break
        else:
            error_msg("Invalid option.")
            input("Press Enter to continue...")

def display_search_results_page(current_results, paginator):
    """Display a page of search results with proper color coding."""
    page_info = paginator.get_page_info()
    
    success_msg(f"Found {page_info['total_items']} bill(s) total:")
    print()
    
    today = datetime.now()
    
    for idx, bill in enumerate(current_results, 1):
        # Calculate actual bill number across all pages
        actual_number = (paginator.current_page - 1) * paginator.items_per_page + idx
        
        # Determine bill status and color (same logic as view_bills)
        if bill.get('paid', False):
            status = f"{Colors.PAID}✓ Paid{Colors.RESET}"
        else:
            status = f"{Colors.UNPAID}○ Unpaid{Colors.RESET}"
        
        # Calculate days until due
        try:
            due_date = datetime.strptime(bill['due_date'], DATE_FORMAT)
            days_diff = (due_date - today).days
            
            if days_diff < 0:
                date_info = f"{Colors.OVERDUE}(Overdue by {abs(days_diff)} days!){Colors.RESET}"
                status = f"{Colors.OVERDUE}! OVERDUE{Colors.RESET}"
            elif days_diff == 0:
                date_info = f"{Colors.DUE_SOON}(Due TODAY!){Colors.RESET}"
            elif days_diff <= 7:
                date_info = f"{Colors.DUE_SOON}(Due in {days_diff} days){Colors.RESET}"
            else:
                date_info = ""
        except ValueError:
            date_info = f"{Colors.ERROR}(Invalid date){Colors.RESET}"
        
        # Display bill with colors (same format as view_bills)
        print(f"{Colors.INFO}{actual_number:3}.{Colors.RESET} {Colors.TITLE}{bill['name']}{Colors.RESET} [{status}]")
        print(f"     Due: {Colors.INFO}{bill['due_date']}{Colors.RESET} {date_info}")
        
        if bill.get('web_page'):
            print(f"     Website: {Colors.INFO}{bill['web_page'][:50]}{'...' if len(bill.get('web_page', '')) > 50 else ''}{Colors.RESET}")
        if bill.get('login_info'):
            print(f"     Login: {Colors.INFO}{bill['login_info'][:30]}{'...' if len(bill.get('login_info', '')) > 30 else ''}{Colors.RESET}")
        print()

# Add these after your color utility functions

class ProgressBar:
    """Progress bar utility functions."""
    
    @staticmethod
    def create_bar(total, description="Processing", color="green"):
        """Create a progress bar with custom styling."""
        bar_format = "{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]"
        
        # Color mapping for tqdm
        color_map = {
            "green": "\033[92m",
            "blue": "\033[94m", 
            "yellow": "\033[93m",
            "red": "\033[91m",
            "cyan": "\033[96m"
        }
        
        return tqdm(
            total=total,
            desc=f"{color_map.get(color, '')}{description}\033[0m",
            bar_format=bar_format,
            ncols=70,
            ascii=True,
            colour=color
        )
    
    @staticmethod
    def simulate_work(pbar, steps, work_function=None):
        """Simulate work with progress updates."""
        step_size = 100 / steps
        for i in range(steps):
            if work_function:
                work_function()
            else:
                time.sleep(0.1)  # Simulate work
            pbar.update(step_size)

def show_progress(func, description="Processing", steps=10, color="green"):
    """Decorator to show progress bar for functions."""
    def wrapper(*args, **kwargs):
        with ProgressBar.create_bar(100, description, color) as pbar:
            # Simulate progress during function execution
            result = func(*args, **kwargs)
            pbar.update(100)
            return result
    return wrapper

# 9. Pagination utility classes and functions
class Paginator:
    """Pagination utility for handling large datasets."""
    
    def __init__(self, items, items_per_page=10):
        self.items = items
        self.items_per_page = items_per_page
        self.total_items = len(items)
        self.total_pages = max(1, (self.total_items + items_per_page - 1) // items_per_page)
        self.current_page = 1
    
    def get_page(self, page_number=None):
        """Get items for a specific page."""
        if page_number is not None:
            self.current_page = max(1, min(page_number, self.total_pages))
        
        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = start_idx + self.items_per_page
        return self.items[start_idx:end_idx]
    
    def next_page(self):
        """Go to next page."""
        if self.current_page < self.total_pages:
            self.current_page += 1
            return True
        return False
    
    def prev_page(self):
        """Go to previous page."""
        if self.current_page > 1:
            self.current_page -= 1
            return True
        return False
    
    def get_page_info(self):
        """Get pagination information."""
        start_item = (self.current_page - 1) * self.items_per_page + 1
        end_item = min(self.current_page * self.items_per_page, self.total_items)
        
        return {
            'current_page': self.current_page,
            'total_pages': self.total_pages,
            'total_items': self.total_items,
            'start_item': start_item,
            'end_item': end_item,
            'has_next': self.current_page < self.total_pages,
            'has_prev': self.current_page > 1
        }

def display_pagination_controls(paginator):
    """Display pagination controls and information."""
    info = paginator.get_page_info()
    
    # Display page information
    colored_print(
        f"📄 Page {info['current_page']} of {info['total_pages']} "
        f"(showing {info['start_item']}-{info['end_item']} of {info['total_items']} bills)",
        Colors.INFO
    )
    
    # Display navigation options
    print("\n" + "="*50)
    nav_options = []
    
    if info['has_prev']:
        nav_options.append("⬅️  [P] Previous page")
    if info['has_next']:
        nav_options.append("➡️  [N] Next page")
    
    nav_options.extend([
        "🔢 [G] Go to page",
        "📊 [S] Change page size",
        "🚪 [B] Back to main menu"
    ])
    
    for option in nav_options:
        print(option)
    print("="*50)

def due_bills_menu():
    """Display due bills menu options."""
    title_msg("Due Bills Options")
    print(f"{Colors.MENU}1.{Colors.RESET} ⏰ Check bills with custom reminder periods")
    print(f"{Colors.MENU}2.{Colors.RESET} 📅 Check bills due within specific days")
    print(f"{Colors.MENU}3.{Colors.RESET} 🔙 Back to main menu")
    print()
    
    while True:
        choice = colored_input("Choose an option (1-3): ", Colors.PROMPT).strip()
        
        if choice == '1':
            clear_console()
            # Use custom reminder periods
            if len(bills) > 10:
                verify_due_bills_paginated(days=None)
            else:
                verify_due_bills(days=None)
                colored_input("\n📖 Press Enter to continue...", Colors.INFO)
            break
        elif choice == '2':
            clear_console()
            # Ask for specific number of days
            try:
                custom_days = int(colored_input("Enter number of days to check (1-365): ", Colors.PROMPT))
                if 1 <= custom_days <= 365:
                    if len(bills) > 10:
                        verify_due_bills_paginated(days=custom_days)
                    else:
                        verify_due_bills(days=custom_days)
                        colored_input("\n📖 Press Enter to continue...", Colors.INFO)
                else:
                    error_msg("Please enter a number between 1 and 365")
                    continue
            except ValueError:
                error_msg("Please enter a valid number")
                continue
            break
        elif choice == '3':
            break
        else:
            error_msg("Please choose option 1, 2, or 3")

# 11. Pagination functions (moved here to be available before main)
def view_bills_paginated(items_per_page=10):
    """View all bills with pagination."""
    if not bills:
        warning_msg("No bills found.")
        input("Press Enter to continue...")
        return
    
    paginator = Paginator(bills, items_per_page)
    
    while True:
        clear_console()
        title_msg("All Bills")
        
        # Display current page of bills
        current_bills = paginator.get_page()
        display_bills_page(current_bills, paginator)
        
        # Display pagination controls
        display_pagination_controls(paginator)
        
        # Get user input
        choice = colored_input("\nEnter your choice: ", Colors.PROMPT).strip().lower()
        
        if choice == 'n' and paginator.get_page_info()['has_next']:
            paginator.next_page()
        elif choice == 'p' and paginator.get_page_info()['has_prev']:
            paginator.prev_page()
        elif choice == 'g':
            goto_page(paginator)
        elif choice == 's':
            new_size = change_page_size()
            if new_size:
                paginator = Paginator(bills, new_size)
        elif choice == 'b':
            break
        else:
            error_msg("Invalid option. Use P/N to navigate, G to go to page, S to change size, B to go back.")
            input("Press Enter to continue...")

def display_bills_page(current_bills, paginator):
    """Display a page of bills with enhanced formatting."""
    today = datetime.now()
    page_info = paginator.get_page_info()
    
    for idx, bill in enumerate(current_bills, page_info['start_item']):
        # Determine bill status and color
        if bill.get('paid', False):
            status = f"{Colors.PAID}✓ Paid{Colors.RESET}"
        else:
            status = f"{Colors.UNPAID}○ Unpaid{Colors.RESET}"
        
        # Calculate days until due
        try:
            due_date = datetime.strptime(bill['due_date'], DATE_FORMAT)
            days_diff = (due_date - today).days
            
            if days_diff < 0:
                date_info = f"{Colors.OVERDUE}(Overdue by {abs(days_diff)} days!){Colors.RESET}"
                status = f"{Colors.OVERDUE}! OVERDUE{Colors.RESET}"
            elif days_diff == 0:
                date_info = f"{Colors.DUE_SOON}(Due TODAY!){Colors.RESET}"
            elif days_diff <= 7:
                date_info = f"{Colors.DUE_SOON}(Due in {days_diff} days){Colors.RESET}"
            else:
                date_info = ""
        except ValueError:
            date_info = f"{Colors.ERROR}(Invalid date){Colors.RESET}"
        
        # Print bill info with colors and numbers
        print(f"{Colors.INFO}{idx:3}.{Colors.RESET} {Colors.TITLE}{bill['name']}{Colors.RESET} [{status}]")
        print(f"     Due: {Colors.INFO}{bill['due_date']}{Colors.RESET} {date_info}")
        
        if bill.get('web_page'):
            print(f"     Website: {Colors.INFO}{bill['web_page'][:50]}{'...' if len(bill.get('web_page', '')) > 50 else ''}{Colors.RESET}")
        if bill.get('login_info'):
            print(f"     Login: {Colors.INFO}{bill['login_info'][:30]}{'...' if len(bill.get('login_info', '')) > 30 else ''}{Colors.RESET}")
        print()

def goto_page(paginator):
    """Go to a specific page."""
    info = paginator.get_page_info()
    try:
        page = int(colored_input(f"Enter page number (1-{info['total_pages']}): ", Colors.PROMPT))
        if 1 <= page <= info['total_pages']:
            paginator.get_page(page)
            success_msg(f"Jumped to page {page}")
        else:
            error_msg(f"Page must be between 1 and {info['total_pages']}")
    except ValueError:
        error_msg("Please enter a valid number")
    
    input("Press Enter to continue...")

def change_page_size():
    """Change the number of items per page."""
    try:
        size = int(colored_input("Enter items per page (5-50): ", Colors.PROMPT))
        if 5 <= size <= 50:
            success_msg(f"Page size changed to {size}")
            return size
        else:
            error_msg("Page size must be between 5 and 50")
    except ValueError:
        error_msg("Please enter a valid number")
    
    input("Press Enter to continue...")
    return None

def display_bill_details(bill):
    """Display detailed information for a single bill."""
    print(f"\n--- Bill Details: {bill['name']} ---")
    print(f"Name: {Colors.TITLE}{bill['name']}{Colors.RESET}")
    print(f"Due Date: {Colors.INFO}{bill['due_date']}{Colors.RESET}")
    
    status_color = Colors.PAID if bill.get('paid', False) else Colors.UNPAID
    status_text = "✓ Paid" if bill.get('paid', False) else "○ Unpaid"
    print(f"Status: {status_color}{status_text}{Colors.RESET}")
    
    print(f"Website: {Colors.INFO}{bill.get('web_page', 'Not provided')}{Colors.RESET}")
    print(f"Login Info: {Colors.INFO}{bill.get('login_info', 'Not provided')}{Colors.RESET}")
    
    # Show password as asterisks
    password = bill.get('password', '')
    password_display = '*' * len(password) if password else 'Not provided'
    print(f"Password: {Colors.INFO}{password_display}{Colors.RESET}")

# 12. Main application
def main():
    """Main application loop with pagination support."""
    clear_console()
    title_msg("Welcome to Bills Tracker! 🏠💳")
    
    # Load existing bills
    load_bills()

    while True:
        display_menu()
        choice = colored_input("Choose an option (1-9): ", Colors.PROMPT).strip()
        
        if choice == '1':
            clear_console()
            add_bill()
        elif choice == '2':
            clear_console()
            # Use pagination if more than 10 bills
            if len(bills) > 10:
                view_bills_paginated()
            else:
                view_bills()
                colored_input("\n📖 Press Enter to continue...", Colors.INFO)
        elif choice == '3':
            clear_console()
            search_bills()
        elif choice == '4':
            clear_console()
            sort_bills()
        elif choice == '5':
            clear_console()
            due_bills_menu()
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
            success_msg("Thank you for using Bills Tracker! 👋")
            break
        else:
            error_msg("Invalid option. Please choose 1-9.")
            colored_input("Press Enter to continue...", Colors.WARNING)

# 10. Missing pagination helper functions
def view_bill_details_from_search(results):
    """View detailed information of a bill from search results."""
    try:
        choice = int(input(f"Enter bill number (1-{len(results)}): "))
        if 1 <= choice <= len(results):
            bill = results[choice - 1]
            display_bill_details(bill)
        else:
            error_msg("Invalid bill number.")
    except ValueError:
        error_msg("Please enter a valid number.")
    
    input("\nPress Enter to continue...")

def pay_bill_from_search(results):
    """Pay a bill from search results."""
    try:
        choice = int(input(f"Enter bill number to pay (1-{len(results)}): "))
        if 1 <= choice <= len(results):
            bill = results[choice - 1]
            if bill.get('paid', False):
                error_msg(f"Bill '{bill['name']}' is already paid.")
            else:
                # Find the bill in the main bills list and pay it
                for main_bill in bills:
                    if main_bill['name'] == bill['name'] and main_bill['due_date'] == bill['due_date']:
                        main_bill['paid'] = True
                        save_bills()
                        success_msg(f"Bill '{bill['name']}' marked as paid!")
                        break
        else:
            error_msg("Invalid bill number.")
    except ValueError:
        error_msg("Please enter a valid number.")
    
    input("Press Enter to continue...")

def view_bill_details_from_search_paginated(current_results, paginator):
    """View bill details from paginated search results."""
    if not current_results:
        return
    
    try:
        choice = int(colored_input(f"Enter bill number (1-{len(current_results)}): ", Colors.PROMPT))
        if 1 <= choice <= len(current_results):
            bill = current_results[choice - 1]
            display_bill_details(bill)
        else:
            error_msg("Invalid bill number.")
    except ValueError:
        error_msg("Please enter a valid number.")
    
    input("\nPress Enter to continue...")

def pay_bill_from_search_paginated(current_results, paginator):
    """Pay a bill from paginated search results."""
    if not current_results:
        return
    
    try:
        choice = int(colored_input(f"Enter bill number to pay (1-{len(current_results)}): ", Colors.PROMPT))
        if 1 <= choice <= len(current_results):
            bill = current_results[choice - 1]
            if bill.get('paid', False):
                error_msg(f"Bill '{bill['name']}' is already paid.")
            else:
                # Find the bill in the main bills list and pay it
                for main_bill in bills:
                    if main_bill['name'] == bill['name'] and main_bill['due_date'] == bill['due_date']:
                        main_bill['paid'] = True
                        save_bills()
                        success_msg(f"Bill '{bill['name']}' marked as paid!")
                        break
        else:
            error_msg("Invalid bill number.")
    except ValueError:
        error_msg("Please enter a valid number.")
    
    input("Press Enter to continue...")

def edit_bill_from_search_paginated(current_results, paginator):
    """Edit a bill from paginated search results."""
    if not current_results:
        return
    
    try:
        choice = int(colored_input(f"Enter bill number to edit (1-{len(current_results)}): ", Colors.PROMPT))
        if 1 <= choice <= len(current_results):
            bill = current_results[choice - 1]
            # Find the bill in the main bills list and edit it
            for main_bill in bills:
                if main_bill['name'] == bill['name'] and main_bill['due_date'] == bill['due_date']:
                    edit_bill_details(main_bill)
                    break
        else:
            error_msg("Invalid bill number.")
    except ValueError:
        error_msg("Please enter a valid number.")

def edit_bill_details(bill):
    """Edit details of a specific bill."""
    print(f"\n--- Editing '{bill['name']}' ---")
    
    new_name = colored_input(f"Name [{bill['name']}]: ", Colors.PROMPT).strip()
    if new_name:
        bill['name'] = new_name

    new_due_date = colored_input(f"Due Date [{bill['due_date']}]: ", Colors.PROMPT).strip()
    if new_due_date:
        try:
            datetime.strptime(new_due_date, DATE_FORMAT)
            is_valid, error_msg_text = validate_future_date(new_due_date)
            if is_valid:
                bill['due_date'] = new_due_date
            else:
                error_msg(error_msg_text + " Keeping the original date.")
        except ValueError:
            error_msg("Invalid date format. Keeping the original date.")
            
    # Website with validation
    colored_print(f"Current website: {bill.get('web_page', 'Not provided')}", Colors.INFO)
    new_web_page = colored_input(f"Web Page [{bill.get('web_page', '')}]: ", Colors.PROMPT).strip()
    if new_web_page:
        if new_web_page.lower() == 'clear':
            bill['web_page'] = ""
            success_msg("Website cleared.")
        else:
            validated_url = validate_url(new_web_page)
            if validated_url is not None:
                bill['web_page'] = validated_url
                if validated_url != new_web_page:
                    success_msg(f"Website corrected to: {validated_url}")
            else:
                error_msg("Invalid URL format. Keeping the original website.")

    new_login_info = colored_input(f"Login Info [{bill.get('login_info', '')}]: ", Colors.PROMPT).strip()
    if new_login_info:
        bill['login_info'] = new_login_info

    new_password = colored_input(f"Password [{bill.get('password', '')}]: ", Colors.PROMPT).strip()
    if new_password:
        bill['password'] = new_password

    paid_status = colored_input(f"Paid (yes/no) [{'yes' if bill.get('paid', False) else 'no'}]: ", Colors.PROMPT).strip().lower()
    if paid_status in ['yes', 'y']:
        bill['paid'] = True
    elif paid_status in ['no', 'n']:
        bill['paid'] = False

    # Billing cycle
    current_cycle = bill.get('billing_cycle', 'monthly')
    print(f"\nCurrent billing cycle: {current_cycle.title()}")
    change_cycle = colored_input("Change billing cycle? (yes/no): ", Colors.PROMPT).strip().lower()
    if change_cycle in ['yes', 'y']:
        new_billing_cycle = get_billing_cycle()
        if new_billing_cycle is not None:
            bill['billing_cycle'] = new_billing_cycle
            success_msg(f"Billing cycle updated to {new_billing_cycle}")

    # Reminder period
    current_reminder = bill.get('reminder_days', 7)
    print(f"\nCurrent reminder period: {current_reminder} days before due date")
    change_reminder = colored_input("Change reminder period? (yes/no): ", Colors.PROMPT).strip().lower()
    if change_reminder in ['yes', 'y']:
        new_reminder_days = get_valid_reminder_days("Enter new reminder days before due date (1-365)", bill.get('reminder_days', 7))
        if new_reminder_days is not None:
            bill['reminder_days'] = new_reminder_days
            success_msg(f"Reminder period updated to {new_reminder_days} days")

    save_bills()
    success_msg(f"Bill '{bill['name']}' updated successfully.")
    input("Press Enter to continue...")

def pay_bill_from_due_list_paginated(current_due_bills, paginator):
    """Pay a specific bill from the paginated due bills list."""
    if not current_due_bills:
        return
    
    try:
        choice = int(colored_input(f"Enter bill number to pay (1-{len(current_due_bills)}): ", Colors.PROMPT))
        if 1 <= choice <= len(current_due_bills):
            bill, days_diff = current_due_bills[choice - 1]
            
            # Find and pay the bill
            for main_bill in bills:
                if main_bill['name'] == bill['name'] and main_bill['due_date'] == bill['due_date']:
                    main_bill['paid'] = True
                    save_bills()
                    success_msg(f"Bill '{bill['name']}' marked as paid!")
                    break
        else:
            error_msg("Invalid bill number.")
    except ValueError:
        error_msg("Please enter a valid number.")
    
    input("Press Enter to continue...")

def bulk_pay_bills_from_due_list(due_bills):
    """Pay multiple bills from the due bills list."""
    if not due_bills:
        warning_msg("No bills to pay.")
        return
    
    choice = colored_input(f"\nPay all {len(due_bills)} due bills? (yes/no): ", Colors.PROMPT).strip().lower()
    
    if choice in ['yes', 'y']:
        paid_count = 0
        for bill, _ in due_bills:
            # Find and pay the bill
            for main_bill in bills:
                if main_bill['name'] == bill['name'] and main_bill['due_date'] == bill['due_date']:
                    if not main_bill.get('paid', False):
                        main_bill['paid'] = True
                        paid_count += 1
                    break
        
        save_bills()
        success_msg(f"Paid {paid_count} bills successfully!")
    else:
        info_msg("Bulk payment cancelled.")
    
    input("Press Enter to continue...")

# 11. Sort functions (missing from your code)
def sort_bills():
    """Sort bills by different criteria."""
    if not bills:
        error_msg("No bills found to sort.")
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
        error_msg("Invalid option. Please choose 1-8.")
        input("Press Enter to continue...")
        sort_bills()

def sort_by_due_date_asc():
    """Sort bills by due date (earliest first)."""
    global bills
    try:
        bills.sort(key=lambda bill: datetime.strptime(bill['due_date'], DATE_FORMAT))
        success_msg("Bills sorted by due date (earliest first)")
        display_sorted_bills("Bills Sorted by Due Date (Earliest First)")
    except ValueError:
        error_msg("Invalid date format found")
        input("Press Enter to continue...")

def sort_by_due_date_desc():
    """Sort bills by due date (latest first)."""
    global bills
    try:
        bills.sort(key=lambda bill: datetime.strptime(bill['due_date'], DATE_FORMAT), reverse=True)
        success_msg("Bills sorted by due date (latest first)")
        display_sorted_bills("Bills Sorted by Due Date (Latest First)")
    except ValueError:
        error_msg("Invalid date format found")
        input("Press Enter to continue...")

def sort_by_name_asc():
    """Sort bills by name (A-Z)."""
    global bills
    bills.sort(key=lambda bill: bill['name'].lower())
    success_msg("Bills sorted by name (A-Z)")
    display_sorted_bills("Bills Sorted by Name (A-Z)")

def sort_by_name_desc():
    """Sort bills by name (Z-A)."""
    global bills
    bills.sort(key=lambda bill: bill['name'].lower(), reverse=True)
    success_msg("Bills sorted by name (Z-A)")
    display_sorted_bills("Bills Sorted by Name (Z-A)")

def sort_by_status_unpaid_first():
    """Sort bills by payment status (unpaid first)."""
    global bills
    bills.sort(key=lambda bill: bill.get('paid', False))
    success_msg("Bills sorted by status (unpaid first)")
    display_sorted_bills("Bills Sorted by Status (Unpaid First)")

def sort_by_status_paid_first():
    """Sort bills by payment status (paid first)."""
    global bills
    bills.sort(key=lambda bill: bill.get('paid', False), reverse=True)
    success_msg("Bills sorted by status (paid first)")
    display_sorted_bills("Bills Sorted by Status (Paid First)")

def reset_bill_order():
    """Reset bills to original order (reload from file)."""
    global bills
    load_bills()
    success_msg("Bills reset to original order")
    display_sorted_bills("Bills in Original Order")

def display_sorted_bills(title):
    """Display sorted bills with formatting."""
    print(f"\n--- {title} ---")
    
    if not bills:
        error_msg("No bills to display.")
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
        success_msg("Sort order saved!")
        input("Press Enter to continue...")
    elif choice == '2':
        sort_bills()
    elif choice == '3':
        return
    else:
        error_msg("Invalid option.")
        input("Press Enter to continue...")

def migrate_bills_to_billing_cycles():
    """Add billing cycle to existing bills that don't have it."""
    migrated_count = 0
    for bill in bills:
        if 'billing_cycle' not in bill:
            bill['billing_cycle'] = BillingCycle.MONTHLY  # Default to monthly
            migrated_count += 1
    
    if migrated_count > 0:
        save_bills()
        info_msg(f"Migrated {migrated_count} bills to include billing cycles (defaulted to monthly)")

def show_billing_cycle_summary():
    """Show a summary of bills by billing cycle."""
    if not bills:
        warning_msg("No bills found.")
        return
    
    title_msg("Bills by Billing Cycle")
    
    # Group bills by cycle
    cycle_groups = {}
    for bill in bills:
        cycle = bill.get('billing_cycle', BillingCycle.MONTHLY)
        if cycle not in cycle_groups:
            cycle_groups[cycle] = []
        cycle_groups[cycle].append(bill)
    
    # Display each group
    for cycle in BillingCycle.get_all_cycles():
        if cycle in cycle_groups:
            cycle_color = get_billing_cycle_color(cycle)
            bills_in_cycle = cycle_groups[cycle]
            
            print(f"\n{cycle_color}📅 {cycle.title()} ({len(bills_in_cycle)} bills){Colors.RESET}")
            print(f"   {BillingCycle.get_cycle_description(cycle)}")
            
            for bill in bills_in_cycle:
                status = "✓ Paid" if bill.get('paid', False) else "○ Unpaid"
                print(f"   • {bill['name']} - Due: {bill['due_date']} [{status}]")
    
    input("\nPress Enter to continue...")

def calculate_upcoming_bills(days=30):
    """Calculate all upcoming bill occurrences within the specified days."""
    upcoming = []
    today = datetime.now()
    end_date = today + timedelta(days=days)
    
    for bill in bills:
        if bill.get('billing_cycle') == BillingCycle.ONE_TIME and bill.get('paid', False):
            continue  # Skip completed one-time bills
        
        try:
            current_due = datetime.strptime(bill['due_date'], DATE_FORMAT)
            cycle = bill.get('billing_cycle', BillingCycle.MONTHLY)
            
            # Generate occurrences for this billing cycle
            occurrence_date = current_due
            occurrences = 0
            max_occurrences = 20  # Prevent infinite loops
            
            while occurrence_date <= end_date and occurrences < max_occurrences:
                if occurrence_date >= today:
                    days_until = (occurrence_date - today).days
                    upcoming.append({
                        'bill': bill,
                        'due_date': occurrence_date,
                        'days_until': days_until,
                        'cycle': cycle
                    })
                
                # Calculate next occurrence
                if cycle == BillingCycle.ONE_TIME:
                    break  # One-time bills don't repeat
                
                next_due_str = calculate_next_due_date(
                    occurrence_date.strftime(DATE_FORMAT), 
                    cycle
                )
                occurrence_date = datetime.strptime(next_due_str, DATE_FORMAT)
                occurrences += 1
                
        except ValueError:
            continue  # Skip bills with invalid dates
    
    return sorted(upcoming, key=lambda x: x['days_until'])

def show_upcoming_bills_calendar():
    """Show upcoming bills in a calendar-like view."""
    title_msg("Upcoming Bills Calendar (Next 30 Days)")
    
    upcoming = calculate_upcoming_bills(30)
    
    if not upcoming:
        info_msg("No upcoming bills in the next 30 days!")
        input("Press Enter to continue...")
        return
    
    # Group by weeks
    current_week = []
    current_week_start = None
    
    for occurrence in upcoming:
        due_date = occurrence['due_date']
        
        # Start new week if needed
        week_start = due_date - timedelta(days=due_date.weekday())
        if current_week_start != week_start:
            if current_week:
                display_week(current_week_start, current_week)
            current_week = []
            current_week_start = week_start
        
        current_week.append(occurrence)
    
    # Display last week
    if current_week:
        display_week(current_week_start, current_week)
    
    input("\nPress Enter to continue...")

def display_week(week_start, occurrences):
    """Display a week of bill occurrences."""
    week_end = week_start + timedelta(days=6)
    print(f"\n📅 Week of {week_start.strftime('%B %d')} - {week_end.strftime('%B %d, %Y')}")
    print("=" * 60)
    
    # Group occurrences by day
    days_dict = {}
    for occurrence in occurrences:
        day_key = occurrence['due_date'].strftime('%Y-%m-%d')
        if day_key not in days_dict:
            days_dict[day_key] = []
        days_dict[day_key].append(occurrence)
    
    # Display each day of the week
    for i in range(7):
        day = week_start + timedelta(days=i)
        day_key = day.strftime('%Y-%m-%d')
        day_name = day.strftime('%A')
        day_date = day.strftime('%m/%d')
        
        if day_key in days_dict:
            day_occurrences = days_dict[day_key]
            print(f"\n{Colors.INFO}{day_name} {day_date}:{Colors.RESET}")
            
            for occurrence in day_occurrences:
                bill = occurrence['bill']
                cycle = occurrence['cycle']
                cycle_color = get_billing_cycle_color(cycle)
                
                days_until = occurrence['days_until']
                if days_until == 0:
                    urgency = f"{Colors.DUE_SOON}DUE TODAY!{Colors.RESET}"
                elif days_until <= 3:
                    urgency = f"{Colors.WARNING}Due in {days_until} days{Colors.RESET}"
                else:
                    urgency = f"{Colors.INFO}Due in {days_until} days{Colors.RESET}"
                
                print(f"  • {bill['name']} ({cycle_color}{cycle}{Colors.RESET}) - {urgency}")


# Add to menu system
def billing_cycle_menu():
    """Show billing cycle management menu."""
    while True:
        clear_console()
        title_msg("Billing Cycle Management")
        
        print(f"{Colors.MENU}1.{Colors.RESET} 📊 Show bills by billing cycle")
        print(f"{Colors.MENU}2.{Colors.RESET} 📅 Show upcoming bills calendar")
        print(f"{Colors.MENU}3.{Colors.RESET} 🔄 Migrate existing bills to billing cycles")
        print(f"{Colors.MENU}4.{Colors.RESET} 🚪 Back to main menu")
        
        choice = colored_input("\nChoose option (1-4): ", Colors.PROMPT).strip()
        
        if choice == '1':
            clear_console()
            show_billing_cycle_summary()
        elif choice == '2':
            clear_console()
            show_upcoming_bills_calendar()
        elif choice == '3':
            clear_console()
            migrate_bills_to_billing_cycles()
            input("Press Enter to continue...")
        elif choice == '4':
            break
        else:
            error_msg("Invalid option. Please choose 1-4.")
            input("Press Enter to continue...")

# Entry point
if __name__ == "__main__":
    main()