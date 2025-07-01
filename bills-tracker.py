# 1. Imports
import json
import os
import shutil
import time
import re
import urllib.parse
import calendar
import difflib
import csv
import base64
from datetime import datetime, timedelta
from colorama import Fore, Back, Style, init
from tqdm import tqdm
import getpass
import hashlib

# Cryptography imports for password encryption
try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False
    print("Warning: cryptography library not available. Passwords will be stored in plain text.")
    print("Install with: pip install cryptography")

# Initialize colorama for Windows compatibility
init(autoreset=True)

# 2. Configuration
BILLS_FILE = 'bills.json'
BACKUP_DIR = 'backups'
MAX_BACKUPS = 5
DATE_FORMAT = '%Y-%m-%d'
TEMPLATES_FILE = 'bill_templates.json'

# Encryption configuration
ENCRYPTION_KEY_FILE = '.encryption_key'
SALT_FILE = '.salt'
MASTER_PASSWORD_FILE = '.master_password'

# Session timeout configuration
SESSION_TIMEOUT_MINUTES = 0.5  # Auto-exit after 15 minutes of inactivity
SESSION_CONFIG_FILE = '.session_config'

bills = []
templates = []

# Global session variables
session_start_time = None
last_activity_time = None
session_locked = False

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
    """Get input with colored prompt and session timeout check."""
    # Check timeout before accepting input
    if check_session_timeout():
        # Session timeout will exit the app
        pass
    # Get input and update activity
    user_input = input(f"{color}{prompt}{Colors.RESET}")
    update_activity()
    return user_input

# 4.2 Encryption utility functions
class PasswordEncryption:
    """Password encryption and decryption utilities using Fernet."""
    
    def __init__(self):
        self.fernet = None
        self.key = None
        self.salt = None
    
    def generate_salt(self):
        """Generate a random salt for key derivation."""
        if not CRYPTOGRAPHY_AVAILABLE:
            return None
        return os.urandom(16)
    
    def derive_key_from_password(self, password, salt):
        """Derive encryption key from password and salt."""
        if not CRYPTOGRAPHY_AVAILABLE:
            return None
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def initialize_encryption(self, master_password=None):
        """Initialize encryption with master password or generate new key."""
        if not CRYPTOGRAPHY_AVAILABLE:
            return False
        
        try:
            # Check if key file exists
            if os.path.exists(ENCRYPTION_KEY_FILE) and os.path.exists(SALT_FILE):
                # Load existing key
                with open(SALT_FILE, 'rb') as f:
                    self.salt = f.read()
                
                if master_password:
                    # Derive key from provided password
                    self.key = self.derive_key_from_password(master_password, self.salt)
                else:
                    # Load stored key
                    with open(ENCRYPTION_KEY_FILE, 'rb') as f:
                        self.key = f.read()
            else:
                # Generate new key
                if master_password:
                    # Use provided password
                    self.salt = self.generate_salt()
                    self.key = self.derive_key_from_password(master_password, self.salt)
                else:
                    # Generate random key
                    self.key = Fernet.generate_key()
                    self.salt = self.generate_salt()
                
                # Save key and salt
                with open(ENCRYPTION_KEY_FILE, 'wb') as f:
                    f.write(self.key)
                with open(SALT_FILE, 'wb') as f:
                    f.write(self.salt)
            
            self.fernet = Fernet(self.key)
            return True
            
        except Exception as e:
            error_msg(f"Failed to initialize encryption: {e}")
            return False
    
    def encrypt_password(self, password):
        """Encrypt a password."""
        if not CRYPTOGRAPHY_AVAILABLE or not self.fernet or not password:
            return password
        
        try:
            encrypted = self.fernet.encrypt(password.encode())
            return base64.urlsafe_b64encode(encrypted).decode()
        except Exception as e:
            error_msg(f"Failed to encrypt password: {e}")
            return password
    
    def decrypt_password(self, encrypted_password):
        """Decrypt a password."""
        if not CRYPTOGRAPHY_AVAILABLE or not self.fernet or not encrypted_password:
            return encrypted_password
        
        try:
            # Check if password is already encrypted
            if encrypted_password.startswith('gAAAAA'):
                # This is a Fernet token, decrypt it
                encrypted_bytes = base64.urlsafe_b64decode(encrypted_password.encode())
                decrypted = self.fernet.decrypt(encrypted_bytes)
                return decrypted.decode()
            else:
                # This might be a plain text password, return as is
                return encrypted_password
        except Exception as e:
            # If decryption fails, assume it's plain text
            return encrypted_password
    
    def migrate_passwords(self, bills_data):
        """Migrate plain text passwords to encrypted format."""
        if not CRYPTOGRAPHY_AVAILABLE or not self.fernet:
            return bills_data
        
        migrated = False
        for bill in bills_data:
            if 'password' in bill and bill['password']:
                # Check if password is already encrypted
                if not bill['password'].startswith('gAAAAA'):
                    # Encrypt plain text password
                    bill['password'] = self.encrypt_password(bill['password'])
                    migrated = True
        
        if migrated:
            success_msg("Passwords migrated to encrypted format")
        
        return bills_data

# Global encryption instance
password_encryption = PasswordEncryption()

def check_session_timeout():
    """Check if session has timed out."""
    if last_activity_time is None:
        return False
    
    if (datetime.now() - last_activity_time) > timedelta(minutes=SESSION_TIMEOUT_MINUTES):
        print(f"\n🔒 Session expired due to {SESSION_TIMEOUT_MINUTES} minutes of inactivity.")
        print("🔄 Exiting application for security...")
        success_msg("Thank you for using Bills Tracker! 👋")
        os._exit(0)  # Force exit immediately
        return True
    return False

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

# 4.1 Auto-complete functions
class AutoComplete:
    """Auto-complete functionality for bill names and other fields."""
    
    @staticmethod
    def get_bill_names():
        """Get all bill names for auto-completion."""
        return [bill['name'] for bill in bills]
    
    @staticmethod
    def get_websites():
        """Get all unique websites for auto-completion."""
        websites = set()
        for bill in bills:
            if bill.get('web_page'):
                websites.add(bill['web_page'])
        return list(websites)
    
    @staticmethod
    def suggest_names(partial_input, max_suggestions=5):
        """Suggest bill names based on partial input."""
        if not partial_input or not bills:
            return []
        
        bill_names = AutoComplete.get_bill_names()
        partial_lower = partial_input.lower()
        
        # Find exact matches first
        exact_matches = [name for name in bill_names if name.lower().startswith(partial_lower)]
        
        # Find fuzzy matches if we need more suggestions
        if len(exact_matches) < max_suggestions:
            fuzzy_matches = difflib.get_close_matches(
                partial_input, 
                bill_names, 
                n=max_suggestions - len(exact_matches),
                cutoff=0.3
            )
            # Remove duplicates
            fuzzy_matches = [name for name in fuzzy_matches if name not in exact_matches]
            exact_matches.extend(fuzzy_matches)
        
        return exact_matches[:max_suggestions]
    
    @staticmethod
    def suggest_websites(partial_input, max_suggestions=3):
        """Suggest websites based on partial input."""
        if not partial_input or not bills:
            return []
        
        websites = AutoComplete.get_websites()
        partial_lower = partial_input.lower()
        
        # Find matches
        matches = [site for site in websites if partial_lower in site.lower()]
        return matches[:max_suggestions]

def get_input_with_autocomplete(prompt, autocomplete_type="bills", allow_empty=False):
    """Get input with auto-complete suggestions."""
    if autocomplete_type not in ["bills", "websites"]:
        autocomplete_type = "bills"
    
    print(f"{Colors.PROMPT}{prompt}{Colors.RESET}")
    if autocomplete_type == "bills" and bills:
        print(f"{Colors.INFO}💡 Type to see suggestions (available bills: {len(bills)}){Colors.RESET}")
    elif autocomplete_type == "websites":
        websites = AutoComplete.get_websites()
        if websites:
            print(f"{Colors.INFO}💡 Type to see website suggestions (available: {len(websites)}){Colors.RESET}")
    
    user_input = ""
    suggestions_shown = False
    
    while True:
        if not suggestions_shown:
            current_input = input(f"{Colors.PROMPT}> {Colors.RESET}").strip()
        else:
            current_input = input(f"{Colors.PROMPT}> {user_input}{Colors.RESET}").strip()
        
        # Handle special commands
        if current_input.lower() == 'cancel':
            return None
        elif current_input.lower() == 'help':
            show_autocomplete_help(autocomplete_type)
            continue
        elif current_input.lower().startswith('?'):
            # Show all available options
            show_all_options(autocomplete_type)
            continue
        elif current_input == "":
            if allow_empty:
                return ""
            if user_input:
                return user_input
            continue
        
        # Update user input
        if not suggestions_shown:
            user_input = current_input
        else:
            user_input += current_input
        
        # Get suggestions
        if autocomplete_type == "bills":
            suggestions = AutoComplete.suggest_names(user_input)
        else:
            suggestions = AutoComplete.suggest_websites(user_input)
        
        if suggestions and len(user_input) > 0:
            print(f"\n{Colors.SUCCESS}💡 Suggestions:{Colors.RESET}")
            for i, suggestion in enumerate(suggestions, 1):
                # Highlight the matching part
                if user_input.lower() in suggestion.lower():
                    highlighted = suggestion.replace(
                        user_input, 
                        f"{Colors.WARNING}{user_input}{Colors.RESET}{Colors.INFO}"
                    )
                    print(f"{Colors.INFO}  {i}. {highlighted}{Colors.RESET}")
                else:
                    print(f"{Colors.INFO}  {i}. {suggestion}{Colors.RESET}")
            
            print(f"{Colors.INFO}  0. Continue typing...{Colors.RESET}")
            print(f"{Colors.INFO}  ?. Show all options{Colors.RESET}")
            print(f"{Colors.WARNING}  Enter number to select, or continue typing{Colors.RESET}")
            
            choice = input(f"{Colors.PROMPT}Choice (or continue typing): {Colors.RESET}").strip()
            
            if choice.isdigit():
                choice_num = int(choice)
                if 1 <= choice_num <= len(suggestions):
                    return suggestions[choice_num - 1]
                elif choice_num == 0:
                    suggestions_shown = True
                    continue
            elif choice.lower() == 'cancel':
                return None
            elif choice.lower().startswith('?'):
                show_all_options(autocomplete_type)
                continue
            else:
                # User wants to continue typing
                user_input += choice
                suggestions_shown = True
                continue
        else:
            # No suggestions, accept input or ask to continue
            if user_input:
                confirm = input(f"{Colors.WARNING}No suggestions found. Use '{user_input}'? (y/n/continue): {Colors.RESET}").strip().lower()
                if confirm in ['y', 'yes']:
                    return user_input
                elif confirm in ['n', 'no']:
                    user_input = ""
                    suggestions_shown = False
                    continue
                else:
                    suggestions_shown = True
                    continue
            else:
                continue

def show_autocomplete_help(autocomplete_type):
    """Show help for auto-complete feature."""
    print(f"\n{Colors.TITLE}📚 Auto-Complete Help{Colors.RESET}")
    print(f"{Colors.INFO}Available commands:{Colors.RESET}")
    print(f"  • Type partial name to see suggestions")
    print(f"  • Enter number to select a suggestion")
    print(f"  • Type '?' to see all available options")
    print(f"  • Type 'cancel' to cancel input")
    print(f"  • Type 'help' to see this help")
    print(f"  • Press Enter with empty input to continue\n")

def show_all_options(autocomplete_type):
    """Show all available options for auto-complete."""
    if autocomplete_type == "bills":
        if not bills:
            warning_msg("No bills available yet.")
            return
        
        print(f"\n{Colors.TITLE}📋 All Available Bills:{Colors.RESET}")
        for i, bill in enumerate(bills, 1):
            status = "✓ Paid" if bill.get('paid', False) else "○ Unpaid"
            print(f"{Colors.INFO}  {i:2}. {bill['name']} [{status}] - Due: {bill['due_date']}{Colors.RESET}")
    
    elif autocomplete_type == "websites":
        websites = AutoComplete.get_websites()
        if not websites:
            warning_msg("No websites available yet.")
            return
        
        print(f"\n{Colors.TITLE}🌐 All Available Websites:{Colors.RESET}")
        for i, website in enumerate(websites, 1):
            print(f"{Colors.INFO}  {i:2}. {website}{Colors.RESET}")
    
    print()

# 5. File operations
def load_bills():
    """Load bills from JSON file with colored feedback."""
    global bills
    try:
        with open(BILLS_FILE, 'r') as f:
            bills = json.load(f)
        
        # Initialize encryption if available
        if CRYPTOGRAPHY_AVAILABLE:
            password_encryption.initialize_encryption()
            # Migrate passwords to encrypted format if needed
            bills = password_encryption.migrate_passwords(bills)
        
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
        
        # Encrypt passwords before saving
        bills_to_save = bills.copy()
        if CRYPTOGRAPHY_AVAILABLE and password_encryption.fernet:
            for bill in bills_to_save:
                if 'password' in bill and bill['password']:
                    # Only encrypt if not already encrypted
                    if not bill['password'].startswith('gAAAAA'):
                        bill['password'] = password_encryption.encrypt_password(bill['password'])
        
        # Save the bills
        with open(BILLS_FILE, 'w') as f:
            json.dump(bills_to_save, f, indent=2)
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
    """Add a new bill with colored feedback and auto-complete assistance."""
    title_msg("Add a New Bill")
    info_msg("Type 'cancel' at any time to cancel.")
    
    # Show existing bills for reference if any exist
    if bills:
        print(f"\n{Colors.INFO}📋 Existing bills for reference:{Colors.RESET}")
        for i, bill in enumerate(bills[:5], 1):  # Show first 5 bills
            status = "✓ Paid" if bill.get('paid', False) else "○ Unpaid"
            print(f"{Colors.INFO}  • {bill['name']} [{status}]{Colors.RESET}")
        if len(bills) > 5:
            print(f"{Colors.INFO}  ... and {len(bills) - 5} more bills{Colors.RESET}")
        print()
    
    # Ask for bill name and check for duplicates
    while True:
        name = get_required_input("Enter the name of the new bill")
        if name is None:
            warning_msg("Bill addition cancelled.")
            return
        
        # Check for duplicates
        if any(bill['name'].lower() == name.lower() for bill in bills):
            error_msg(f"A bill with the name '{name}' already exists. Please enter a different name.")
            # Show similar names for reference
            similar_names = AutoComplete.suggest_names(name, max_suggestions=3)
            if similar_names:
                print(f"{Colors.WARNING}💡 Similar existing bills:{Colors.RESET}")
                for similar in similar_names:
                    print(f"{Colors.WARNING}  • {similar}{Colors.RESET}")
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

    # Get contact information
    print(f"\n{Colors.TITLE}📞 Contact Information (Optional){Colors.RESET}")
    print(f"{Colors.INFO}Add customer service contact details for this bill:{Colors.RESET}")
    
    company_email = get_valid_email("Enter company customer service email")
    if company_email is None:
        warning_msg("Bill addition cancelled.")
        return
    
    support_phone = get_optional_input("Enter customer support phone number")
    if support_phone is None:
        warning_msg("Bill addition cancelled.")
        return
    
    billing_phone = get_optional_input("Enter billing department phone number")
    if billing_phone is None:
        warning_msg("Bill addition cancelled.")
        return
    
    customer_service_hours = get_optional_input("Enter customer service hours (e.g., Mon-Fri 9AM-5PM)")
    if customer_service_hours is None:
        warning_msg("Bill addition cancelled.")
        return
    
    account_number = get_optional_input("Enter account/customer number")
    if account_number is None:
        warning_msg("Bill addition cancelled.")
        return
    
    reference_id = get_optional_input("Enter reference/policy number")
    if reference_id is None:
        warning_msg("Bill addition cancelled.")
        return
    
    support_chat_url = get_valid_url("Enter live chat support URL (optional)")
    if support_chat_url is None:
        warning_msg("Bill addition cancelled.")
        return
    
    mobile_app = get_optional_input("Enter mobile app information (e.g., 'Netflix App - iOS/Android')")
    if mobile_app is None:
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
        "reminder_days": reminder_days,
        # Contact information
        "company_email": company_email,
        "support_phone": support_phone,
        "billing_phone": billing_phone,
        "customer_service_hours": customer_service_hours,
        "account_number": account_number,
        "reference_id": reference_id,
        "support_chat_url": support_chat_url,
        "mobile_app": mobile_app
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
    print(f"{Colors.MENU}9.{Colors.RESET} 📋 Bill templates")
    print(f"{Colors.MENU}10.{Colors.RESET} 📥 CSV Import/Export")
    print(f"{Colors.MENU}11.{Colors.RESET} 📖 Help")
    print(f"{Colors.MENU}12.{Colors.RESET} 🚪 Exit")
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
        
        # Show contact information if available
        contact_info = []
        if bill.get('company_email'):
            contact_info.append(f"📧 {bill['company_email']}")
        if bill.get('support_phone'):
            contact_info.append(f"📞 Support: {bill['support_phone']}")
        if bill.get('billing_phone'):
            contact_info.append(f"💰 Billing: {bill['billing_phone']}")
        if bill.get('account_number'):
            contact_info.append(f"🆔 Account: {bill['account_number']}")
        
        if contact_info:
            print(f"    {Colors.INFO}📞 Contact: {', '.join(contact_info[:2])}{'...' if len(contact_info) > 2 else ''}{Colors.RESET}")
        
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

            # Show decrypted password for editing
            current_password = bill.get('password', '')
            if current_password and CRYPTOGRAPHY_AVAILABLE and password_encryption.fernet:
                current_password = password_encryption.decrypt_password(current_password)
            
            new_password = input(f"Password [{current_password}]: ").strip()
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

            # Contact Information
            print(f"\n{Colors.TITLE}📞 Contact Information{Colors.RESET}")
            
            new_company_email = colored_input(f"Company Email [{bill.get('company_email', '')}]: ", Colors.PROMPT).strip()
            if new_company_email:
                if new_company_email.lower() == 'clear':
                    bill['company_email'] = ""
                    success_msg("Company email cleared.")
                else:
                    validated_email = validate_email(new_company_email)
                    if validated_email is not None:
                        bill['company_email'] = validated_email
                    else:
                        error_msg("Invalid email format. Keeping the original email.")

            new_support_phone = colored_input(f"Support Phone [{bill.get('support_phone', '')}]: ", Colors.PROMPT).strip()
            if new_support_phone:
                bill['support_phone'] = new_support_phone

            new_billing_phone = colored_input(f"Billing Phone [{bill.get('billing_phone', '')}]: ", Colors.PROMPT).strip()
            if new_billing_phone:
                bill['billing_phone'] = new_billing_phone

            new_service_hours = colored_input(f"Service Hours [{bill.get('customer_service_hours', '')}]: ", Colors.PROMPT).strip()
            if new_service_hours:
                bill['customer_service_hours'] = new_service_hours

            new_account_number = colored_input(f"Account Number [{bill.get('account_number', '')}]: ", Colors.PROMPT).strip()
            if new_account_number:
                bill['account_number'] = new_account_number

            new_reference_id = colored_input(f"Reference ID [{bill.get('reference_id', '')}]: ", Colors.PROMPT).strip()
            if new_reference_id:
                bill['reference_id'] = new_reference_id

            new_support_chat_url = colored_input(f"Support Chat URL [{bill.get('support_chat_url', '')}]: ", Colors.PROMPT).strip()
            if new_support_chat_url:
                if new_support_chat_url.lower() == 'clear':
                    bill['support_chat_url'] = ""
                    success_msg("Support chat URL cleared.")
                else:
                    validated_url = validate_url(new_support_chat_url)
                    if validated_url is not None:
                        bill['support_chat_url'] = validated_url
                    else:
                        error_msg("Invalid URL format. Keeping the original URL.")

            new_mobile_app = colored_input(f"Mobile App [{bill.get('mobile_app', '')}]: ", Colors.PROMPT).strip()
            if new_mobile_app:
                bill['mobile_app'] = new_mobile_app

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
    print("4. Search by contact information")
    print("5. Search all fields")
    print("6. Back to main menu")
    
    choice = input("\nChoose search option (1-6): ").strip()
    
    if choice == '1':
        search_by_name()
    elif choice == '2':
        search_by_due_date()
    elif choice == '3':
        search_by_website()
    elif choice == '4':
        search_by_contact_info()
    elif choice == '5':
        search_all_fields()
    elif choice == '6':
        return
    else:
        print("❌ Invalid option. Please choose 1-6.")
        input("Press Enter to continue...")
        search_bills()

def search_by_name():
    """Search bills by name with auto-complete suggestions."""
    if not bills:
        warning_msg("No bills found.")
        return
    
    colored_print("\n🔍 Search Bills by Name", Colors.TITLE)
    
    search_term = get_input_with_autocomplete(
        "Enter bill name to search (with auto-complete)", 
        autocomplete_type="bills", 
        allow_empty=False
    )
    
    if search_term is None:
        warning_msg("Search cancelled.")
        return
    
    if not search_term:
        error_msg("Search term cannot be empty.")
        return
    
    # Perform search (case-insensitive partial match)
    search_term_lower = search_term.lower()
    results = [bill for bill in bills 
              if search_term_lower in bill['name'].lower()]
    
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
    """Search bills by website with auto-complete suggestions."""
    if not bills:
        warning_msg("No bills found.")
        return
    
    websites = AutoComplete.get_websites()
    if not websites:
        warning_msg("No websites found in bills.")
        return
    
    colored_print("\n🌐 Search Bills by Website", Colors.TITLE)
    
    search_term = get_input_with_autocomplete(
        "Enter website to search (with auto-complete)", 
        autocomplete_type="websites", 
        allow_empty=False
    )
    
    if search_term is None:
        warning_msg("Search cancelled.")
        return
    
    if not search_term:
        error_msg("Search term cannot be empty.")
        return
    
    # Perform search (case-insensitive partial match)
    search_term_lower = search_term.lower()
    results = [bill for bill in bills 
              if search_term_lower in bill.get('web_page', '').lower()]
    
    display_search_results(results, f"Bills with website containing '{search_term}'")

def search_by_contact_info():
    """Search bills by contact information."""
    if not bills:
        warning_msg("No bills found.")
        return
    
    print("\nSearch by Contact Information:")
    print("1. Search by company email")
    print("2. Search by phone number")
    print("3. Search by account number")
    print("4. Search by reference ID")
    print("5. Back to search menu")
    
    choice = input("\nChoose option (1-5): ").strip()
    
    if choice == '1':
        search_term = input("Enter company email to search: ").strip().lower()
        results = [bill for bill in bills 
                  if search_term in bill.get('company_email', '').lower()]
        display_search_results(results, f"Bills with company email containing '{search_term}'")
        
    elif choice == '2':
        search_term = input("Enter phone number to search: ").strip()
        results = [bill for bill in bills 
                  if (search_term in bill.get('support_phone', '') or 
                      search_term in bill.get('billing_phone', ''))]
        display_search_results(results, f"Bills with phone number containing '{search_term}'")
        
    elif choice == '3':
        search_term = input("Enter account number to search: ").strip()
        results = [bill for bill in bills 
                  if search_term in bill.get('account_number', '')]
        display_search_results(results, f"Bills with account number containing '{search_term}'")
        
    elif choice == '4':
        search_term = input("Enter reference ID to search: ").strip()
        results = [bill for bill in bills 
                  if search_term in bill.get('reference_id', '')]
        display_search_results(results, f"Bills with reference ID containing '{search_term}'")
        
    elif choice == '5':
        return
    else:
        error_msg("Invalid option. Please choose 1-5.")
        input("Press Enter to continue...")
        search_by_contact_info()

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
                bill.get('login_info', ''),
                bill.get('company_email', ''),
                bill.get('support_phone', ''),
                bill.get('billing_phone', ''),
                bill.get('customer_service_hours', ''),
                bill.get('account_number', ''),
                bill.get('reference_id', ''),
                bill.get('support_chat_url', ''),
                bill.get('mobile_app', '')
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
    
    # Show password as asterisks (decrypt if encrypted)
    password = bill.get('password', '')
    if password and CRYPTOGRAPHY_AVAILABLE and password_encryption.fernet:
        # Decrypt password for display
        decrypted_password = password_encryption.decrypt_password(password)
        password_display = '*' * len(decrypted_password) if decrypted_password else 'Not provided'
    else:
        password_display = '*' * len(password) if password else 'Not provided'
    print(f"Password: {Colors.INFO}{password_display}{Colors.RESET}")
    
    # Show billing cycle and reminder
    cycle = bill.get('billing_cycle', 'monthly')
    cycle_color = get_billing_cycle_color(cycle)
    print(f"Billing Cycle: {cycle_color}{cycle.title()}{Colors.RESET}")
    
    reminder_days = bill.get('reminder_days', 7)
    print(f"Reminder: {Colors.WARNING}{reminder_days} days before due date{Colors.RESET}")
    
    # Show contact information
    print(f"\n{Colors.TITLE}📞 Contact Information:{Colors.RESET}")
    if bill.get('company_email'):
        print(f"  📧 Customer Service Email: {Colors.INFO}{bill['company_email']}{Colors.RESET}")
    if bill.get('support_phone'):
        print(f"  📞 Support Phone: {Colors.INFO}{bill['support_phone']}{Colors.RESET}")
    if bill.get('billing_phone'):
        print(f"  💰 Billing Phone: {Colors.INFO}{bill['billing_phone']}{Colors.RESET}")
    if bill.get('customer_service_hours'):
        print(f"  🕒 Service Hours: {Colors.INFO}{bill['customer_service_hours']}{Colors.RESET}")
    if bill.get('account_number'):
        print(f"  🆔 Account Number: {Colors.INFO}{bill['account_number']}{Colors.RESET}")
    if bill.get('reference_id'):
        print(f"  📋 Reference ID: {Colors.INFO}{bill['reference_id']}{Colors.RESET}")
    if bill.get('support_chat_url'):
        print(f"  💬 Live Chat: {Colors.INFO}{bill['support_chat_url']}{Colors.RESET}")
    if bill.get('mobile_app'):
        print(f"  📱 Mobile App: {Colors.INFO}{bill['mobile_app']}{Colors.RESET}")
    
    # Check if no contact info was provided
    contact_fields = ['company_email', 'support_phone', 'billing_phone', 'customer_service_hours', 
                     'account_number', 'reference_id', 'support_chat_url', 'mobile_app']
    if not any(bill.get(field) for field in contact_fields):
        print(f"  {Colors.WARNING}No contact information provided{Colors.RESET}")

# 12. Main application
def main():
    """Main application loop with pagination support and master password protection."""
    clear_console()
    title_msg("Welcome to Bills Tracker! 🏠💳")

    # Require master password before proceeding
    master_password = verify_master_password()

    # Initialize encryption with master password
    if CRYPTOGRAPHY_AVAILABLE:
        password_encryption.initialize_encryption(master_password)

    # Start session timer
    start_session()

    # Load existing bills and templates
    load_bills()
    load_templates()

    while True:
        display_menu()
        choice = colored_input("Choose an option (1-12): ", Colors.PROMPT).strip()
        
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
            clear_console()
            templates_menu()
        elif choice == '10':
            clear_console()
            csv_import_export_menu()
        elif choice == '11':
            show_help_menu()
        elif choice == '12':
            success_msg("Thank you for using Bills Tracker! 👋")
            break
        else:
            error_msg("Invalid option. Please choose 1-12.")
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

    # Show decrypted password for editing
    current_password = bill.get('password', '')
    if current_password and CRYPTOGRAPHY_AVAILABLE and password_encryption.fernet:
        current_password = password_encryption.decrypt_password(current_password)
    
    new_password = colored_input(f"Password [{current_password}]: ", Colors.PROMPT).strip()
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

# 5.1 Template operations
def load_templates():
    """Load bill templates from JSON file."""
    global bill_templates
    try:
        with open(TEMPLATES_FILE, 'r') as f:
            bill_templates = json.load(f)
        
        # Initialize encryption if available and migrate passwords
        if CRYPTOGRAPHY_AVAILABLE:
            password_encryption.initialize_encryption()
            # Migrate passwords to encrypted format if needed
            bill_templates = password_encryption.migrate_passwords(bill_templates)
        
        success_msg(f"Loaded {len(bill_templates)} bill templates")
    except FileNotFoundError:
        bill_templates = []
        info_msg("Starting with empty templates list")
    except json.JSONDecodeError:
        bill_templates = []
        error_msg("Corrupted templates file. Starting fresh.")

def save_templates():
    """Save bill templates to JSON file."""
    try:
        # Encrypt passwords before saving
        templates_to_save = bill_templates.copy()
        if CRYPTOGRAPHY_AVAILABLE and password_encryption.fernet:
            for template in templates_to_save:
                if 'password' in template and template['password']:
                    # Only encrypt if not already encrypted
                    if not template['password'].startswith('gAAAAA'):
                        template['password'] = password_encryption.encrypt_password(template['password'])
        
        with open(TEMPLATES_FILE, 'w') as f:
            json.dump(templates_to_save, f, indent=2)
        success_msg("Templates saved successfully")
    except Exception as e:
        error_msg(f"Template save error: {e}")

def create_template_from_bill(bill):
    """Create a template from an existing bill."""
    template = {
        "name": bill['name'],
        "web_page": bill.get('web_page', ''),
        "login_info": bill.get('login_info', ''),
        "password": bill.get('password', ''),
        "billing_cycle": bill.get('billing_cycle', BillingCycle.MONTHLY),
        "reminder_days": bill.get('reminder_days', 7),
        # Contact information
        "company_email": bill.get('company_email', ''),
        "support_phone": bill.get('support_phone', ''),
        "billing_phone": bill.get('billing_phone', ''),
        "customer_service_hours": bill.get('customer_service_hours', ''),
        "account_number": bill.get('account_number', ''),
        "reference_id": bill.get('reference_id', ''),
        "support_chat_url": bill.get('support_chat_url', ''),
        "mobile_app": bill.get('mobile_app', '')
    }
    return template

def save_bill_as_template():
    """Save an existing bill as a template."""
    if not bills:
        warning_msg("No bills found to create templates from.")
        return
    
    title_msg("Save Bill as Template")
    
    # Show bills for selection
    print(f"\n{Colors.INFO}📋 Available bills:{Colors.RESET}")
    for i, bill in enumerate(bills, 1):
        status = "✓ Paid" if bill.get('paid', False) else "○ Unpaid"
        print(f"{Colors.INFO}  {i}. {bill['name']} [{status}]{Colors.RESET}")
    
    try:
        choice = int(colored_input(f"\nSelect bill to save as template (1-{len(bills)}): ", Colors.PROMPT))
        if 1 <= choice <= len(bills):
            bill = bills[choice - 1]
            
            # Check if template already exists
            existing_template = next((t for t in bill_templates if t['name'] == bill['name']), None)
            if existing_template:
                overwrite = colored_input(f"Template '{bill['name']}' already exists. Overwrite? (y/n): ", Colors.WARNING).strip().lower()
                if overwrite not in ['y', 'yes']:
                    info_msg("Template creation cancelled.")
                    return
                bill_templates.remove(existing_template)
            
            # Create and save template
            template = create_template_from_bill(bill)
            bill_templates.append(template)
            save_templates()
            
            success_msg(f"Template '{bill['name']}' saved successfully!")
            
            # Show template details
            print(f"\n{Colors.INFO}📋 Template details:{Colors.RESET}")
            print(f"  Name: {Colors.TITLE}{template['name']}{Colors.RESET}")
            print(f"  Billing Cycle: {get_billing_cycle_color(template['billing_cycle'])}{template['billing_cycle'].title()}{Colors.RESET}")
            print(f"  Reminder Days: {Colors.INFO}{template['reminder_days']}{Colors.RESET}")
            if template.get('web_page'):
                print(f"  Website: {Colors.INFO}{template['web_page']}{Colors.RESET}")
            if template.get('login_info'):
                print(f"  Login: {Colors.INFO}{template['login_info']}{Colors.RESET}")
        else:
            error_msg("Invalid selection.")
    except ValueError:
        error_msg("Please enter a valid number.")
    
    colored_input("\nPress Enter to continue...", Colors.INFO)

def create_template_manually():
    """Create a new template manually."""
    title_msg("Create New Bill Template")
    info_msg("Type 'cancel' at any time to cancel.")
    
    # Get template name
    while True:
        name = get_required_input("Enter template name")
        if name is None:
            warning_msg("Template creation cancelled.")
            return
        
        # Check for duplicates
        if any(template['name'].lower() == name.lower() for template in bill_templates):
            error_msg(f"A template with the name '{name}' already exists. Please enter a different name.")
        else:
            break
    
    # Get billing cycle
    billing_cycle = get_billing_cycle()
    if billing_cycle is None:
        warning_msg("Template creation cancelled.")
        return
    
    # Get reminder period
    reminder_days = get_valid_reminder_days("Enter reminder days before due date (1-365)")
    if reminder_days is None:
        warning_msg("Template creation cancelled.")
        return
    
    # Get optional fields
    web_page = get_valid_url("Enter the web page for the bill (optional)")
    if web_page is None:
        warning_msg("Template creation cancelled.")
        return
    
    login_info = get_optional_input("Enter the login information for the bill")
    if login_info is None:
        warning_msg("Template creation cancelled.")
        return

    password = get_optional_input("Enter the password for the bill")
    if password is None:
        warning_msg("Template creation cancelled.")
        return

    # Get contact information
    print(f"\n{Colors.TITLE}📞 Contact Information (Optional){Colors.RESET}")
    print(f"{Colors.INFO}Add customer service contact details for this template:{Colors.RESET}")
    
    company_email = get_valid_email("Enter company customer service email: ")
    if company_email is None:
        warning_msg("Template creation cancelled.")
        return
    
    support_phone = get_optional_input("Enter customer support phone number")
    if support_phone is None:
        warning_msg("Template creation cancelled.")
        return
    
    billing_phone = get_optional_input("Enter billing department phone number")
    if billing_phone is None:
        warning_msg("Template creation cancelled.")
        return
    
    customer_service_hours = get_optional_input("Enter customer service hours (e.g., Mon-Fri 9AM-5PM)")
    if customer_service_hours is None:
        warning_msg("Template creation cancelled.")
        return
    
    account_number = get_optional_input("Enter account/customer number")
    if account_number is None:
        warning_msg("Template creation cancelled.")
        return
    
    reference_id = get_optional_input("Enter reference/policy number")
    if reference_id is None:
        warning_msg("Template creation cancelled.")
        return
    
    support_chat_url = get_valid_url("Enter live chat support URL (optional)")
    if support_chat_url is None:
        warning_msg("Template creation cancelled.")
        return
    
    mobile_app = get_optional_input("Enter mobile app information (e.g., 'Netflix App - iOS/Android')")
    if mobile_app is None:
        warning_msg("Template creation cancelled.")
        return

    # Create and save template
    template = {
        "name": name,
        "web_page": web_page,
        "login_info": login_info,
        "password": password,
        "billing_cycle": billing_cycle,
        "reminder_days": reminder_days,
        # Contact information
        "company_email": company_email,
        "support_phone": support_phone,
        "billing_phone": billing_phone,
        "customer_service_hours": customer_service_hours,
        "account_number": account_number,
        "reference_id": reference_id,
        "support_chat_url": support_chat_url,
        "mobile_app": mobile_app
    }
    
    bill_templates.append(template)
    save_templates()
    
    success_msg(f"Template '{name}' created successfully!")
    colored_input("Press Enter to continue...", Colors.INFO)

def view_templates():
    """View all available templates."""
    title_msg("Bill Templates")
    
    if not bill_templates:
        warning_msg("No templates found.")
        colored_input("Press Enter to continue...", Colors.INFO)
        return
    
    for idx, template in enumerate(bill_templates, 1):
        print(f"\n{Colors.INFO}{idx}.{Colors.RESET} {Colors.TITLE}{template['name']}{Colors.RESET}")
        
        # Show billing cycle
        cycle = template.get('billing_cycle', BillingCycle.MONTHLY)
        cycle_color = get_billing_cycle_color(cycle)
        print(f"    Cycle: {cycle_color}{cycle.title()}{Colors.RESET}")
        
        # Show reminder period
        reminder_days = template.get('reminder_days', 7)
        if reminder_days == 1:
            reminder_text = "1 day before"
        else:
            reminder_text = f"{reminder_days} days before"
        print(f"    Reminder: {Colors.WARNING}⏰ {reminder_text}{Colors.RESET}")
        
        if template.get('web_page'):
            print(f"    Website: {Colors.INFO}{template['web_page']}{Colors.RESET}")
        if template.get('login_info'):
            print(f"    Login: {Colors.INFO}{template['login_info']}{Colors.RESET}")
        
        # Show contact information if available
        contact_info = []
        if template.get('company_email'):
            contact_info.append(f"📧 {template['company_email']}")
        if template.get('support_phone'):
            contact_info.append(f"📞 {template['support_phone']}")
        if template.get('billing_phone'):
            contact_info.append(f"💰 {template['billing_phone']}")
        if template.get('account_number'):
            contact_info.append(f"🆔 {template['account_number']}")
        
        if contact_info:
            print(f"    {Colors.INFO}📞 Contact: {', '.join(contact_info[:2])}{'...' if len(contact_info) > 2 else ''}{Colors.RESET}")
    
    # Template management options
    print(f"\n{Colors.MENU}Template Options:{Colors.RESET}")
    print("1. ✏️  Edit a template")
    print("2. 🗑️  Delete a template")
    print("3. 📝 Use template to add bill")
    print("4. 🔙 Back to templates menu")
    
    choice = colored_input("\nChoose option (1-4): ", Colors.PROMPT).strip()
    
    if choice == '1':
        edit_template()
    elif choice == '2':
        delete_template()
    elif choice == '3':
        use_template_to_add_bill()
    elif choice == '4':
        return
    else:
        error_msg("Invalid option.")
        colored_input("Press Enter to continue...", Colors.WARNING)

def edit_template():
    """Edit an existing template."""
    if not bill_templates:
        warning_msg("No templates to edit.")
        return
    
    try:
        choice = int(colored_input(f"Enter template number to edit (1-{len(bill_templates)}): ", Colors.PROMPT))
        if 1 <= choice <= len(bill_templates):
            template = bill_templates[choice - 1]
            print(f"\n--- Editing Template: {template['name']} ---")
            
            # Edit template fields
            new_name = colored_input(f"Name [{template['name']}]: ", Colors.PROMPT).strip()
            if new_name:
                # Check for name conflicts
                if any(t['name'].lower() == new_name.lower() and t != template for t in bill_templates):
                    error_msg(f"A template with the name '{new_name}' already exists.")
                else:
                    template['name'] = new_name
            
            # Billing cycle
            current_cycle = template.get('billing_cycle', BillingCycle.MONTHLY)
            print(f"\nCurrent billing cycle: {current_cycle.title()}")
            change_cycle = colored_input("Change billing cycle? (yes/no): ", Colors.PROMPT).strip().lower()
            if change_cycle in ['yes', 'y']:
                new_billing_cycle = get_billing_cycle()
                if new_billing_cycle is not None:
                    template['billing_cycle'] = new_billing_cycle
            
            # Reminder period
            current_reminder = template.get('reminder_days', 7)
            print(f"\nCurrent reminder period: {current_reminder} days before due date")
            change_reminder = colored_input("Change reminder period? (yes/no): ", Colors.PROMPT).strip().lower()
            if change_reminder in ['yes', 'y']:
                new_reminder_days = get_valid_reminder_days("Enter new reminder days before due date (1-365)", current_reminder)
                if new_reminder_days is not None:
                    template['reminder_days'] = new_reminder_days
            
            # Website
            new_web_page = colored_input(f"Website [{template.get('web_page', '')}]: ", Colors.PROMPT).strip()
            if new_web_page:
                if new_web_page.lower() == 'clear':
                    template['web_page'] = ""
                else:
                    validated_url = validate_url(new_web_page)
                    if validated_url is not None:
                        template['web_page'] = validated_url
                    else:
                        error_msg("Invalid URL format. Keeping the original website.")
            
            # Login info
            new_login_info = colored_input(f"Login Info [{template.get('login_info', '')}]: ", Colors.PROMPT).strip()
            if new_login_info:
                template['login_info'] = new_login_info
            
            # Password
            # Show decrypted password for editing
            current_password = template.get('password', '')
            if current_password and CRYPTOGRAPHY_AVAILABLE and password_encryption.fernet:
                current_password = password_encryption.decrypt_password(current_password)
            
            new_password = colored_input(f"Password [{current_password}]: ", Colors.PROMPT).strip()
            if new_password:
                template['password'] = new_password
            
            # Contact Information
            print(f"\n{Colors.TITLE}📞 Contact Information{Colors.RESET}")
            
            new_company_email = colored_input(f"Company Email [{template.get('company_email', '')}]: ", Colors.PROMPT).strip()
            if new_company_email:
                if new_company_email.lower() == 'clear':
                    template['company_email'] = ""
                    success_msg("Company email cleared.")
                else:
                    validated_email = validate_email(new_company_email)
                    if validated_email is not None:
                        template['company_email'] = validated_email
                    else:
                        error_msg("Invalid email format. Keeping the original email.")

            new_support_phone = colored_input(f"Support Phone [{template.get('support_phone', '')}]: ", Colors.PROMPT).strip()
            if new_support_phone:
                template['support_phone'] = new_support_phone

            new_billing_phone = colored_input(f"Billing Phone [{template.get('billing_phone', '')}]: ", Colors.PROMPT).strip()
            if new_billing_phone:
                template['billing_phone'] = new_billing_phone

            new_service_hours = colored_input(f"Service Hours [{template.get('customer_service_hours', '')}]: ", Colors.PROMPT).strip()
            if new_service_hours:
                template['customer_service_hours'] = new_service_hours

            new_account_number = colored_input(f"Account Number [{template.get('account_number', '')}]: ", Colors.PROMPT).strip()
            if new_account_number:
                template['account_number'] = new_account_number

            new_reference_id = colored_input(f"Reference ID [{template.get('reference_id', '')}]: ", Colors.PROMPT).strip()
            if new_reference_id:
                template['reference_id'] = new_reference_id

            new_support_chat_url = colored_input(f"Support Chat URL [{template.get('support_chat_url', '')}]: ", Colors.PROMPT).strip()
            if new_support_chat_url:
                if new_support_chat_url.lower() == 'clear':
                    template['support_chat_url'] = ""
                    success_msg("Support chat URL cleared.")
                else:
                    validated_url = validate_url(new_support_chat_url)
                    if validated_url is not None:
                        template['support_chat_url'] = validated_url
                    else:
                        error_msg("Invalid URL format. Keeping the original URL.")

            new_mobile_app = colored_input(f"Mobile App [{template.get('mobile_app', '')}]: ", Colors.PROMPT).strip()
            if new_mobile_app:
                template['mobile_app'] = new_mobile_app
            
            save_templates()
            success_msg(f"Template '{template['name']}' updated successfully.")
        else:
            error_msg("Invalid selection.")
    except ValueError:
        error_msg("Please enter a valid number.")
    
    colored_input("Press Enter to continue...", Colors.INFO)

def delete_template():
    """Delete a template."""
    if not bill_templates:
        warning_msg("No templates to delete.")
        return
    
    try:
        choice = int(colored_input(f"Enter template number to delete (1-{len(bill_templates)}): ", Colors.PROMPT))
        if 1 <= choice <= len(bill_templates):
            template = bill_templates[choice - 1]
            confirm = colored_input(f"Are you sure you want to delete template '{template['name']}'? (yes/no): ", Colors.WARNING).strip().lower()
            if confirm in ['yes', 'y']:
                bill_templates.remove(template)
                save_templates()
                success_msg(f"Template '{template['name']}' deleted successfully.")
            else:
                info_msg("Deletion cancelled.")
        else:
            error_msg("Invalid selection.")
    except ValueError:
        error_msg("Please enter a valid number.")
    
    colored_input("Press Enter to continue...", Colors.INFO)

def use_template_to_add_bill():
    """Use a template to quickly add a new bill."""
    if not bill_templates:
        warning_msg("No templates available.")
        colored_input("Press Enter to continue...", Colors.INFO)
        return
    
    try:
        choice = int(colored_input(f"Enter template number to use (1-{len(bill_templates)}): ", Colors.PROMPT))
        if 1 <= choice <= len(bill_templates):
            template = bill_templates[choice - 1]
            
            title_msg(f"Add Bill from Template: {template['name']}")
            
            # Get due date (required for new bill)
            due_date = get_valid_date_with_range_check("Enter the due date for this bill (YYYY-MM-DD)")
            if due_date is None:
                warning_msg("Bill creation cancelled.")
                return
            
            # Create bill from template
            bill = {
                "name": template['name'],
                "due_date": due_date,
                "web_page": template.get('web_page', ''),
                "login_info": template.get('login_info', ''),
                "password": template.get('password', ''),
                "paid": False,
                "billing_cycle": template.get('billing_cycle', BillingCycle.MONTHLY),
                "reminder_days": template.get('reminder_days', 7),
                # Contact information from template
                "company_email": template.get('company_email', ''),
                "support_phone": template.get('support_phone', ''),
                "billing_phone": template.get('billing_phone', ''),
                "customer_service_hours": template.get('customer_service_hours', ''),
                "account_number": template.get('account_number', ''),
                "reference_id": template.get('reference_id', ''),
                "support_chat_url": template.get('support_chat_url', ''),
                "mobile_app": template.get('mobile_app', '')
            }
            
            bills.append(bill)
            save_bills()
            
            success_msg(f"Bill '{template['name']}' added successfully from template!")
            info_msg(f"Due date: {due_date}")
            info_msg(f"Billing cycle: {template.get('billing_cycle', BillingCycle.MONTHLY)}")
            
            # Show contact info if available
            contact_info = []
            if template.get('company_email'):
                contact_info.append(f"📧 {template['company_email']}")
            if template.get('support_phone'):
                contact_info.append(f"📞 {template['support_phone']}")
            if template.get('account_number'):
                contact_info.append(f"🆔 {template['account_number']}")
            
            if contact_info:
                info_msg(f"Contact info included: {', '.join(contact_info[:2])}{'...' if len(contact_info) > 2 else ''}")
            
        else:
            error_msg("Invalid selection.")
    except ValueError:
        error_msg("Please enter a valid number.")
    
    colored_input("Press Enter to continue...", Colors.INFO)

def templates_menu():
    """Display templates management menu."""
    while True:
        clear_console()
        title_msg("Bill Templates Management")
        
        print(f"{Colors.MENU}1.{Colors.RESET} 📋 View all templates")
        print(f"{Colors.MENU}2.{Colors.RESET} 📝 Create new template")
        print(f"{Colors.MENU}3.{Colors.RESET} 💾 Save bill as template")
        print(f"{Colors.MENU}4.{Colors.RESET} 🚪 Back to main menu")
        
        choice = colored_input("\nChoose option (1-4): ", Colors.PROMPT).strip()
        
        if choice == '1':
            clear_console()
            view_templates()
        elif choice == '2':
            clear_console()
            create_template_manually()
        elif choice == '3':
            clear_console()
            save_bill_as_template()
        elif choice == '4':
            break
        else:
            error_msg("Invalid option. Please choose 1-4.")
            colored_input("Press Enter to continue...", Colors.WARNING)

# 5.2 CSV Import/Export operations
def import_bills_from_csv():
    """Import bills from a CSV file."""
    title_msg("Import Bills from CSV")
    info_msg("This will import bills from a CSV file. Make sure your CSV has the correct format.")
    
    # Show CSV format requirements
    print(f"\n{Colors.TITLE}📋 Required CSV Format:{Colors.RESET}")
    print("Your CSV file should have these columns (headers are case-insensitive):")
    print(f"{Colors.INFO}• name{Colors.RESET} - Bill name (required)")
    print(f"{Colors.INFO}• due_date{Colors.RESET} - Due date in YYYY-MM-DD format (required)")
    print(f"{Colors.INFO}• billing_cycle{Colors.RESET} - weekly, bi-weekly, monthly, quarterly, semi-annually, annually, one-time")
    print(f"{Colors.INFO}• reminder_days{Colors.RESET} - Days before due date for reminders (default: 7)")
    print(f"{Colors.INFO}• web_page{Colors.RESET} - Website URL (optional)")
    print(f"{Colors.INFO}• login_info{Colors.RESET} - Login information (optional)")
    print(f"{Colors.INFO}• password{Colors.RESET} - Password (optional)")
    print(f"{Colors.INFO}• company_email{Colors.RESET} - Customer service email (optional)")
    print(f"{Colors.INFO}• support_phone{Colors.RESET} - Support phone number (optional)")
    print(f"{Colors.INFO}• billing_phone{Colors.RESET} - Billing phone number (optional)")
    print(f"{Colors.INFO}• customer_service_hours{Colors.RESET} - Service hours (optional)")
    print(f"{Colors.INFO}• account_number{Colors.RESET} - Account number (optional)")
    print(f"{Colors.INFO}• reference_id{Colors.RESET} - Reference ID (optional)")
    print(f"{Colors.INFO}• support_chat_url{Colors.RESET} - Live chat URL (optional)")
    print(f"{Colors.INFO}• mobile_app{Colors.RESET} - Mobile app info (optional)")
    
    # Get CSV file path
    csv_file = colored_input(f"\n{Colors.PROMPT}Enter the path to your CSV file: {Colors.RESET}").strip()
    
    if not csv_file:
        warning_msg("Import cancelled.")
        return
    
    # Check if file exists
    if not os.path.exists(csv_file):
        error_msg(f"File '{csv_file}' not found.")
        colored_input("Press Enter to continue...", Colors.INFO)
        return
    
    # Validate file extension
    if not csv_file.lower().endswith('.csv'):
        error_msg("File must have a .csv extension.")
        colored_input("Press Enter to continue...", Colors.INFO)
        return
    
    try:
        # Read and parse CSV file
        imported_bills = []
        skipped_bills = []
        errors = []
        
        with open(csv_file, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            # Validate headers
            required_headers = ['name', 'due_date']
            optional_headers = ['billing_cycle', 'reminder_days', 'web_page', 'login_info', 'password',
                              'company_email', 'support_phone', 'billing_phone', 'customer_service_hours',
                              'account_number', 'reference_id', 'support_chat_url', 'mobile_app']
            
            fieldnames = [field.lower() for field in reader.fieldnames] if reader.fieldnames else []
            
            missing_required = [h for h in required_headers if h not in fieldnames]
            if missing_required:
                error_msg(f"Missing required columns: {', '.join(missing_required)}")
                colored_input("Press Enter to continue...", Colors.INFO)
                return
            
            # Process each row
            row_count = 0
            for row in reader:
                row_count += 1
                try:
                    # Validate required fields
                    name = row.get('name', '').strip()
                    due_date = row.get('due_date', '').strip()
                    
                    if not name:
                        errors.append(f"Row {row_count}: Missing bill name")
                        continue
                    
                    if not due_date:
                        errors.append(f"Row {row_count}: Missing due date")
                        continue
                    
                    # Validate date format
                    try:
                        datetime.strptime(due_date, DATE_FORMAT)
                    except ValueError:
                        errors.append(f"Row {row_count}: Invalid date format '{due_date}' (use YYYY-MM-DD)")
                        continue
                    
                    # Check for duplicate names
                    if any(bill['name'].lower() == name.lower() for bill in bills):
                        skipped_bills.append(f"Row {row_count}: '{name}' (duplicate name)")
                        continue
                    
                    # Create bill object
                    bill = {
                        'name': name,
                        'due_date': due_date,
                        'paid': False,
                        'billing_cycle': row.get('billing_cycle', 'monthly').strip().lower(),
                        'reminder_days': int(row.get('reminder_days', 7)),
                        'web_page': row.get('web_page', '').strip(),
                        'login_info': row.get('login_info', '').strip(),
                        'password': row.get('password', '').strip(),
                        'company_email': row.get('company_email', '').strip(),
                        'support_phone': row.get('support_phone', '').strip(),
                        'billing_phone': row.get('billing_phone', '').strip(),
                        'customer_service_hours': row.get('customer_service_hours', '').strip(),
                        'account_number': row.get('account_number', '').strip(),
                        'reference_id': row.get('reference_id', '').strip(),
                        'support_chat_url': row.get('support_chat_url', '').strip(),
                        'mobile_app': row.get('mobile_app', '').strip()
                    }
                    
                    # Validate billing cycle
                    valid_cycles = BillingCycle.get_all_cycles()
                    if bill['billing_cycle'] not in valid_cycles:
                        bill['billing_cycle'] = 'monthly'  # Default to monthly
                        warning_msg(f"Row {row_count}: Invalid billing cycle, defaulting to monthly")
                    
                    # Validate reminder days
                    if not (1 <= bill['reminder_days'] <= 365):
                        bill['reminder_days'] = 7  # Default to 7 days
                        warning_msg(f"Row {row_count}: Invalid reminder days, defaulting to 7")
                    
                    # Validate URLs
                    if bill['web_page']:
                        validated_url = validate_url(bill['web_page'])
                        if validated_url is not None:
                            bill['web_page'] = validated_url
                        else:
                            warning_msg(f"Row {row_count}: Invalid website URL, keeping as-is")
                    
                    if bill['support_chat_url']:
                        validated_url = validate_url(bill['support_chat_url'])
                        if validated_url is not None:
                            bill['support_chat_url'] = validated_url
                        else:
                            warning_msg(f"Row {row_count}: Invalid support chat URL, keeping as-is")
                    
                    # Validate email
                    if bill['company_email']:
                        validated_email = validate_email(bill['company_email'])
                        if validated_email is not None:
                            bill['company_email'] = validated_email
                        else:
                            warning_msg(f"Row {row_count}: Invalid email format, keeping as-is")
                    
                    imported_bills.append(bill)
                    
                except Exception as e:
                    errors.append(f"Row {row_count}: {str(e)}")
        
        # Show import results
        print(f"\n{Colors.TITLE}📊 Import Results:{Colors.RESET}")
        success_msg(f"Successfully imported {len(imported_bills)} bills")
        
        if skipped_bills:
            warning_msg(f"Skipped {len(skipped_bills)} bills (duplicates)")
            for skipped in skipped_bills[:5]:  # Show first 5
                print(f"  • {skipped}")
            if len(skipped_bills) > 5:
                print(f"  ... and {len(skipped_bills) - 5} more")
        
        if errors:
            error_msg(f"Found {len(errors)} errors")
            for error in errors[:5]:  # Show first 5
                print(f"  • {error}")
            if len(errors) > 5:
                print(f"  ... and {len(errors) - 5} more")
        
        # Ask user to confirm import
        if imported_bills:
            confirm = colored_input(f"\n{Colors.WARNING}Import {len(imported_bills)} bills? (yes/no): {Colors.RESET}").strip().lower()
            if confirm in ['yes', 'y']:
                # Add bills to the main list
                bills.extend(imported_bills)
                save_bills()
                success_msg(f"Successfully imported {len(imported_bills)} bills!")
                
                # Show sample of imported bills
                print(f"\n{Colors.INFO}📋 Sample of imported bills:{Colors.RESET}")
                for i, bill in enumerate(imported_bills[:3], 1):
                    print(f"  {i}. {bill['name']} - Due: {bill['due_date']} ({bill['billing_cycle']})")
                if len(imported_bills) > 3:
                    print(f"  ... and {len(imported_bills) - 3} more bills")
            else:
                info_msg("Import cancelled.")
        else:
            warning_msg("No bills to import.")
        
    except Exception as e:
        error_msg(f"Error reading CSV file: {str(e)}")
    
    colored_input("\nPress Enter to continue...", Colors.INFO)

def export_bills_to_csv():
    """Export bills to a CSV file."""
    title_msg("Export Bills to CSV")
    
    if not bills:
        warning_msg("No bills to export.")
        colored_input("Press Enter to continue...", Colors.INFO)
        return
    
    # Get export file path
    default_filename = f"bills_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    csv_file = colored_input(f"{Colors.PROMPT}Enter export filename [{default_filename}]: {Colors.RESET}").strip()
    
    if not csv_file:
        csv_file = default_filename
    
    # Ensure .csv extension
    if not csv_file.lower().endswith('.csv'):
        csv_file += '.csv'
    
    try:
        with open(csv_file, 'w', newline='', encoding='utf-8') as file:
            # Define fieldnames for CSV
            fieldnames = [
                'name', 'due_date', 'paid', 'billing_cycle', 'reminder_days',
                'web_page', 'login_info', 'password', 'company_email',
                'support_phone', 'billing_phone', 'customer_service_hours',
                'account_number', 'reference_id', 'support_chat_url', 'mobile_app'
            ]
            
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            # Write each bill
            for bill in bills:
                row = {
                    'name': bill.get('name', ''),
                    'due_date': bill.get('due_date', ''),
                    'paid': 'yes' if bill.get('paid', False) else 'no',
                    'billing_cycle': bill.get('billing_cycle', 'monthly'),
                    'reminder_days': bill.get('reminder_days', 7),
                    'web_page': bill.get('web_page', ''),
                    'login_info': bill.get('login_info', ''),
                    'password': bill.get('password', ''),
                    'company_email': bill.get('company_email', ''),
                    'support_phone': bill.get('support_phone', ''),
                    'billing_phone': bill.get('billing_phone', ''),
                    'customer_service_hours': bill.get('customer_service_hours', ''),
                    'account_number': bill.get('account_number', ''),
                    'reference_id': bill.get('reference_id', ''),
                    'support_chat_url': bill.get('support_chat_url', ''),
                    'mobile_app': bill.get('mobile_app', '')
                }
                writer.writerow(row)
        
        success_msg(f"Successfully exported {len(bills)} bills to '{csv_file}'")
        info_msg(f"File location: {os.path.abspath(csv_file)}")
        
    except Exception as e:
        error_msg(f"Error exporting to CSV: {str(e)}")
    
    colored_input("Press Enter to continue...", Colors.INFO)

def create_sample_csv():
    """Create a sample CSV file with the correct format."""
    sample_filename = "sample_bills_import.csv"
    
    try:
        with open(sample_filename, 'w', newline='', encoding='utf-8') as file:
            fieldnames = [
                'name', 'due_date', 'billing_cycle', 'reminder_days',
                'web_page', 'login_info', 'password', 'company_email',
                'support_phone', 'billing_phone', 'customer_service_hours',
                'account_number', 'reference_id', 'support_chat_url', 'mobile_app'
            ]
            
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            # Add sample data
            sample_bills = [
                {
                    'name': 'Netflix Subscription',
                    'due_date': '2024-02-15',
                    'billing_cycle': 'monthly',
                    'reminder_days': '7',
                    'web_page': 'https://netflix.com',
                    'login_info': 'user@example.com',
                    'password': 'your_password',
                    'company_email': 'support@netflix.com',
                    'support_phone': '1-800-123-4567',
                    'billing_phone': '1-800-123-4568',
                    'customer_service_hours': '24/7',
                    'account_number': 'NF123456789',
                    'reference_id': '',
                    'support_chat_url': 'https://netflix.com/help',
                    'mobile_app': 'Netflix App - iOS/Android'
                },
                {
                    'name': 'Electric Bill',
                    'due_date': '2024-02-20',
                    'billing_cycle': 'monthly',
                    'reminder_days': '10',
                    'web_page': 'https://electriccompany.com',
                    'login_info': 'account123',
                    'password': 'your_password',
                    'company_email': 'billing@electriccompany.com',
                    'support_phone': '1-800-555-0123',
                    'billing_phone': '1-800-555-0124',
                    'customer_service_hours': 'Mon-Fri 8AM-6PM',
                    'account_number': 'ELEC789012',
                    'reference_id': 'INV-2024-001',
                    'support_chat_url': '',
                    'mobile_app': 'Electric Company App'
                }
            ]
            
            for bill in sample_bills:
                writer.writerow(bill)
        
        success_msg(f"Sample CSV file created: '{sample_filename}'")
        info_msg(f"File location: {os.path.abspath(sample_filename)}")
        print(f"\n{Colors.INFO}📋 Sample file includes:{Colors.RESET}")
        print("  • Netflix Subscription (monthly)")
        print("  • Electric Bill (monthly)")
        print("  • All contact information fields")
        print("  • Proper date format (YYYY-MM-DD)")
        
    except Exception as e:
        error_msg(f"Error creating sample file: {str(e)}")
    
    colored_input("Press Enter to continue...", Colors.INFO)

def csv_import_export_menu():
    """Display CSV import/export menu."""
    while True:
        clear_console()
        title_msg("CSV Import/Export")
        
        print(f"{Colors.MENU}1.{Colors.RESET} 📥 Import bills from CSV")
        print(f"{Colors.MENU}2.{Colors.RESET} 📤 Export bills to CSV")
        print(f"{Colors.MENU}3.{Colors.RESET} 📋 Create sample CSV file")
        print(f"{Colors.MENU}4.{Colors.RESET} 🚪 Back to main menu")
        
        choice = colored_input("\nChoose option (1-4): ", Colors.PROMPT).strip()
        
        if choice == '1':
            clear_console()
            import_bills_from_csv()
        elif choice == '2':
            clear_console()
            export_bills_to_csv()
        elif choice == '3':
            clear_console()
            create_sample_csv()
        elif choice == '4':
            break
        else:
            error_msg("Invalid option. Please choose 1-4.")
            colored_input("Press Enter to continue...", Colors.WARNING)

# 13. Help System
def show_help_menu():
    """Display the main help menu."""
    while True:
        clear_console()
        title_msg("Help & Documentation")
        
        print(f"{Colors.MENU}1.{Colors.RESET} 📖 What is Bills Tracker?")
        print(f"{Colors.MENU}2.{Colors.RESET} 🚀 Getting Started Guide")
        print(f"{Colors.MENU}3.{Colors.RESET} 📝 Adding & Managing Bills")
        print(f"{Colors.MENU}4.{Colors.RESET} 🔍 Searching & Sorting")
        print(f"{Colors.MENU}5.{Colors.RESET} ⏰ Due Bills & Reminders")
        print(f"{Colors.MENU}6.{Colors.RESET} 💰 Paying Bills")
        print(f"{Colors.MENU}7.{Colors.RESET} 📋 Bill Templates")
        print(f"{Colors.MENU}8.{Colors.RESET} 📥 CSV Import/Export")
        print(f"{Colors.MENU}9.{Colors.RESET} 🔧 Tips & Troubleshooting")
        print(f"{Colors.MENU}10.{Colors.RESET} 🚪 Back to main menu")
        
        choice = colored_input("\nChoose help topic (1-10): ", Colors.PROMPT).strip()
        
        if choice == '1':
            clear_console()
            show_what_is_bills_tracker()
        elif choice == '2':
            clear_console()
            show_getting_started_guide()
        elif choice == '3':
            clear_console()
            show_adding_managing_bills()
        elif choice == '4':
            clear_console()
            show_searching_sorting()
        elif choice == '5':
            clear_console()
            show_due_bills_reminders()
        elif choice == '6':
            clear_console()
            show_paying_bills()
        elif choice == '7':
            clear_console()
            show_bill_templates_help()
        elif choice == '8':
            clear_console()
            show_csv_import_export_help()
        elif choice == '9':
            clear_console()
            show_tips_troubleshooting()
        elif choice == '10':
            break
        else:
            error_msg("Invalid option. Please choose 1-10.")
            colored_input("Press Enter to continue...", Colors.WARNING)

def show_what_is_bills_tracker():
    """Explain what Bills Tracker is and its purpose."""
    clear_console()
    title_msg("What is Bills Tracker?")
    
    print(f"{Colors.INFO}Bills Tracker is a comprehensive command-line application designed to help you manage your bills and payments efficiently.{Colors.RESET}")
    print()
    
    print(f"{Colors.TITLE}🎯 Main Purpose:{Colors.RESET}")
    print("• Keep track of all your bills in one place")
    print("• Never miss a payment deadline")
    print("• Organize billing information securely")
    print("• Simplify bill management with templates")
    print()
    
    print(f"{Colors.TITLE}✨ Key Features:{Colors.RESET}")
    print("• 📝 Add, edit, and delete bills")
    print("• 📅 Track due dates with custom reminders")
    print("• 🔄 Handle different billing cycles (weekly, monthly, etc.)")
    print("• 💰 Mark bills as paid with automatic due date updates")
    print("• 🔍 Search and sort bills easily")
    print("• 📋 Use templates for quick bill creation")
    print("• 💾 Automatic backup system")
    print("• 🎨 Color-coded interface for better visibility")
    print()
    
    print(f"{Colors.TITLE}🔒 Data Security:{Colors.RESET}")
    print("• All data is stored locally on your computer")
    print("• Automatic backups protect against data loss")
    print("• No internet connection required")
    print("• Your information stays private")
    print()
    
    colored_input("Press Enter to continue...", Colors.INFO)

def show_getting_started_guide():
    """Show a step-by-step getting started guide."""
    clear_console()
    title_msg("Getting Started Guide")
    
    print(f"{Colors.TITLE}🚀 Step 1: First Launch{Colors.RESET}")
    print("When you first run Bills Tracker, it will:")
    print("• Create necessary files and folders")
    print("• Set up the backup system")
    print("• Load any existing bills (if any)")
    print()
    
    print(f"{Colors.TITLE}📝 Step 2: Add Your First Bill{Colors.RESET}")
    print("1. Choose option 1 from the main menu")
    print("2. Enter the bill name (e.g., 'Netflix Subscription')")
    print("3. Set the due date (YYYY-MM-DD format)")
    print("4. Choose the billing cycle (monthly, weekly, etc.)")
    print("5. Set reminder days (how many days before due date)")
    print("6. Add optional information (website, login, password)")
    print()
    
    print(f"{Colors.TITLE}⏰ Step 3: Check Due Bills{Colors.RESET}")
    print("1. Choose option 5 from the main menu")
    print("2. Select 'Check bills with custom reminder periods'")
    print("3. View bills that are due soon")
    print("4. Use this regularly to stay on top of payments")
    print()
    
    print(f"{Colors.TITLE}💰 Step 4: Pay Bills{Colors.RESET}")
    print("1. Choose option 6 from the main menu")
    print("2. Select the bill you want to pay")
    print("3. Choose payment option (advance cycle or mark as paid)")
    print("4. The due date will update automatically")
    print()
    
    print(f"{Colors.TITLE}📋 Step 5: Create Templates (Optional){Colors.RESET}")
    print("1. Choose option 9 from the main menu")
    print("2. Create templates for bills you add frequently")
    print("3. Use templates to quickly add new bills")
    print()
    
    print(f"{Colors.TITLE}💡 Pro Tips:{Colors.RESET}")
    print("• Check due bills daily or weekly")
    print("• Use templates for recurring bills")
    print("• Set appropriate reminder periods")
    print("• Keep backup files safe")
    print()
    
    colored_input("Press Enter to continue...", Colors.INFO)

def show_adding_managing_bills():
    """Explain how to add and manage bills."""
    clear_console()
    title_msg("Adding & Managing Bills")
    
    print(f"{Colors.TITLE}📝 Adding a New Bill{Colors.RESET}")
    print("1. Choose 'Add a bill' from the main menu")
    print("2. Enter the bill name (required)")
    print("3. Set the due date in YYYY-MM-DD format")
    print("4. Choose billing cycle:")
    print("   • Weekly - Every 7 days")
    print("   • Bi-weekly - Every 14 days")
    print("   • Monthly - Every month")
    print("   • Quarterly - Every 3 months")
    print("   • Semi-annually - Every 6 months")
    print("   • Annually - Every 12 months")
    print("   • One-time - No recurrence")
    print("5. Set reminder days (1-365 days before due)")
    print("6. Add optional website URL")
    print("7. Add optional login information")
    print("8. Add optional password")
    print()
    
    print(f"{Colors.TITLE}✏️ Editing Bills{Colors.RESET}")
    print("1. Choose 'Edit a bill' from the main menu")
    print("2. Select the bill to edit")
    print("3. Modify any field (press Enter to keep current value)")
    print("4. Changes are saved automatically")
    print()
    
    print(f"{Colors.TITLE}🗑️ Deleting Bills{Colors.RESET}")
    print("1. Choose 'Delete a bill' from the main menu")
    print("2. Select the bill to delete")
    print("3. Confirm deletion")
    print("⚠️  Warning: Deletion cannot be undone")
    print()
    
    print(f"{Colors.TITLE}📋 Viewing Bills{Colors.RESET}")
    print("• Choose 'View all bills' to see all bills")
    print("• Bills are color-coded by status:")
    print("  🟢 Green - Paid bills")
    print("  🟡 Yellow - Unpaid bills")
    print("  🔴 Red - Overdue bills")
    print("• Large lists use pagination for better navigation")
    print()
    
    print(f"{Colors.TITLE}🔍 Auto-complete Features{Colors.RESET}")
    print("• Type partial bill names to see suggestions")
    print("• Use '?' to see all available options")
    print("• Type 'cancel' to exit any input")
    print("• Use 'help' for context-sensitive help")
    print()
    
    colored_input("Press Enter to continue...", Colors.INFO)

def show_searching_sorting():
    """Explain search and sort functionality."""
    clear_console()
    title_msg("Searching & Sorting Bills")
    
    print(f"{Colors.TITLE}🔍 Search Options{Colors.RESET}")
    print("1. Search by name - Find bills by partial name match")
    print("2. Search by due date - Find bills due on specific dates")
    print("3. Search by website - Find bills by website URL")
    print("4. Search by contact information")
    print("5. Search all fields - Search across all bill information")
    print()
    
    print(f"{Colors.TITLE}🔍 Search by Name{Colors.RESET}")
    print("• Use auto-complete for bill name suggestions")
    print("• Case-insensitive partial matching")
    print("• Shows similar names if exact match not found")
    print("• Can view, pay, or edit bills from search results")
    print()
    
    print(f"{Colors.TITLE}📅 Search by Date{Colors.RESET}")
    print("• Exact date (YYYY-MM-DD)")
    print("• Month and year (YYYY-MM)")
    print("• Year only (YYYY)")
    print("• Useful for finding bills due in specific periods")
    print()
    
    print(f"{Colors.TITLE}🌐 Search by Website{Colors.RESET}")
    print("• Search by website URL or domain")
    print("• Auto-complete shows previously used websites")
    print("• Useful for finding bills from the same company")
    print()
    
    print(f"{Colors.TITLE}🔄 Sort Options{Colors.RESET}")
    print("1. Sort by due date (earliest first)")
    print("2. Sort by due date (latest first)")
    print("3. Sort by name (A-Z)")
    print("4. Sort by name (Z-A)")
    print("5. Sort by payment status (unpaid first)")
    print("6. Sort by payment status (paid first)")
    print("7. Reset to original order")
    print()
    
    print(f"{Colors.TITLE}💡 Search Tips{Colors.RESET}")
    print("• Use partial words for broader searches")
    print("• Search results show bill status and due dates")
    print("• You can perform actions directly from search results")
    print("• Large result sets use pagination")
    print()
    
    colored_input("Press Enter to continue...", Colors.INFO)

def show_due_bills_reminders():
    """Explain due bills and reminder system."""
    clear_console()
    title_msg("Due Bills & Reminders")
    
    print(f"{Colors.TITLE}⏰ Reminder System{Colors.RESET}")
    print("Bills Tracker uses a smart reminder system:")
    print("• Each bill has its own custom reminder period")
    print("• Default reminder is 7 days before due date")
    print("• You can set reminders from 1 to 365 days")
    print("• Reminders are checked automatically")
    print()
    
    print(f"{Colors.TITLE}📅 Checking Due Bills{Colors.RESET}")
    print("Two ways to check due bills:")
    print()
    print("1. Custom Reminder Periods:")
    print("   • Uses each bill's individual reminder setting")
    print("   • Shows bills that are due within their reminder period")
    print("   • Most personalized approach")
    print()
    print("2. Specific Day Range:")
    print("   • Check bills due within X days")
    print("   • Useful for weekly or monthly planning")
    print("   • Good for bulk payment planning")
    print()
    
    print(f"{Colors.TITLE}🎨 Status Indicators{Colors.RESET}")
    print("Bills are color-coded by urgency:")
    print("🔴 Red - OVERDUE (past due date)")
    print("🟠 Orange - DUE TODAY")
    print("🟡 Yellow - Due within 3 days")
    print("🔵 Blue - Due within reminder period")
    print()
    
    print(f"{Colors.TITLE}📊 Due Bills Features{Colors.RESET}")
    print("• View all due bills in one place")
    print("• Sort by urgency (overdue first)")
    print("• Pay individual bills directly")
    print("• Bulk pay multiple bills")
    print("• Change reminder periods")
    print("• Navigate with pagination for large lists")
    print()
    
    print(f"{Colors.TITLE}💡 Best Practices{Colors.RESET}")
    print("• Check due bills daily or weekly")
    print("• Set appropriate reminder periods for each bill")
    print("• Use bulk payment for multiple due bills")
    print("• Review overdue bills immediately")
    print("• Adjust reminder periods based on your payment habits")
    print()
    
    colored_input("Press Enter to continue...", Colors.INFO)

def show_paying_bills():
    """Explain the bill payment process."""
    clear_console()
    title_msg("Paying Bills")
    
    print(f"{Colors.TITLE}💰 Payment Process{Colors.RESET}")
    print("1. Choose 'Pay a bill' from the main menu")
    print("2. Select the bill you want to pay")
    print("3. Choose payment option")
    print("4. Bill status and due date are updated automatically")
    print()
    
    print(f"{Colors.TITLE}🔄 Payment Options{Colors.RESET}")
    print("For recurring bills, you have two options:")
    print()
    print("1. Pay and Advance to Next Cycle:")
    print("   • Marks current bill as paid")
    print("   • Automatically calculates next due date")
    print("   • Bill remains active for next cycle")
    print("   • Recommended for ongoing subscriptions")
    print()
    print("2. Mark as Permanently Paid:")
    print("   • Marks bill as permanently paid")
    print("   • Bill won't appear in due bills")
    print("   • Use for one-time payments or cancelled services")
    print("   • Can be reactivated by editing the bill")
    print()
    
    print(f"{Colors.TITLE}📅 Due Date Updates{Colors.RESET}")
    print("When you pay a recurring bill:")
    print("• Next due date is calculated automatically")
    print("• Handles different month lengths correctly")
    print("• Respects the billing cycle (weekly, monthly, etc.)")
    print("• One-time bills don't change due dates")
    print()
    
    print(f"{Colors.TITLE}💳 Payment Methods{Colors.RESET}")
    print("Bills Tracker tracks payment status, not actual payments:")
    print("• You pay bills through your usual methods")
    print("• Mark bills as paid in the app")
    print("• Store payment information (websites, login details)")
    print("• Track payment history and due dates")
    print()
    
    print(f"{Colors.TITLE}📋 Bulk Payments{Colors.RESET}")
    print("From the due bills screen:")
    print("• Pay multiple bills at once")
    print("• Useful for monthly bill management")
    print("• Saves time when many bills are due")
    print("• Each bill follows its own payment rules")
    print()
    
    print(f"{Colors.TITLE}💡 Payment Tips{Colors.RESET}")
    print("• Pay bills as soon as they appear in due bills")
    print("• Use bulk payment for efficiency")
    print("• Keep payment information updated")
    print("• Review payment history regularly")
    print("• Set up auto-pay where possible")
    print()
    
    colored_input("Press Enter to continue...", Colors.INFO)

def show_bill_templates_help():
    """Explain bill templates functionality."""
    clear_console()
    title_msg("Bill Templates")
    
    print(f"{Colors.TITLE}📋 What are Templates?{Colors.RESET}")
    print("Templates are reusable bill configurations that save time:")
    print("• Store common bill information")
    print("• Quick bill creation with minimal input")
    print("• Standardize billing cycles and reminders")
    print("• Perfect for recurring bills")
    print()
    
    print(f"{Colors.TITLE}📝 Creating Templates{Colors.RESET}")
    print("Two ways to create templates:")
    print()
    print("1. From Existing Bills:")
    print("   • Choose 'Save bill as template'")
    print("   • Select an existing bill")
    print("   • Template is created with all bill details")
    print("   • Excludes due date (you set this for each new bill)")
    print()
    print("2. Manual Creation:")
    print("   • Choose 'Create new template'")
    print("   • Enter template name and details")
    print("   • Set billing cycle and reminder period")
    print("   • Add optional website and login information")
    print()
    
    print(f"{Colors.TITLE}🚀 Using Templates{Colors.RESET}")
    print("To add a bill from a template:")
    print("1. Choose 'Use template to add bill'")
    print("2. Select the template to use")
    print("3. Enter only the due date")
    print("4. Bill is created with all template details")
    print("5. Much faster than manual entry")
    print()
    
    print(f"{Colors.TITLE}✏️ Managing Templates{Colors.RESET}")
    print("Template management options:")
    print("• View all templates with details")
    print("• Edit template information")
    print("• Delete unused templates")
    print("• Use templates to create bills")
    print("• Templates are saved automatically")
    print()
    
    print(f"{Colors.TITLE}💡 Template Best Practices{Colors.RESET}")
    print("• Create templates for bills you add frequently")
    print("• Use descriptive template names")
    print("• Include website and login information")
    print("• Set appropriate reminder periods")
    print("• Update templates when information changes")
    print("• Delete templates you no longer use")
    print()
    
    print(f"{Colors.TITLE}🔄 Template vs Bill{Colors.RESET}")
    print("Templates:")
    print("• Reusable configurations")
    print("• No due dates")
    print("• Used to create bills quickly")
    print()
    print("Bills:")
    print("• Actual bill instances")
    print("• Have specific due dates")
    print("• Track payment status")
    print("• Can be paid and updated")
    print()
    
    colored_input("Press Enter to continue...", Colors.INFO)

def show_tips_troubleshooting():
    """Show helpful tips and tricks for using Bills Tracker."""
    clear_console()
    title_msg("Tips & Troubleshooting")
    
    print(f"{Colors.TITLE}⚡ Quick Actions{Colors.RESET}")
    print("• Type 'cancel' to exit any input")
    print("• Type 'help' for context-sensitive help")
    print("• Use '?' to see all available options")
    print("• Press Enter to continue after messages")
    print()
    
    print(f"{Colors.TITLE}🎯 Efficient Workflow{Colors.RESET}")
    print("1. Check due bills daily (option 5)")
    print("2. Pay bills as they appear")
    print("3. Use templates for new bills")
    print("4. Search when you need to find something")
    print("5. Sort bills when organizing")
    print("6. Use CSV import for bulk operations")
    print()
    
    print(f"{Colors.TITLE}📅 Date Management{Colors.RESET}")
    print("• Use YYYY-MM-DD format for dates")
    print("• Set appropriate reminder periods")
    print("• Check due bills regularly")
    print("• Use custom reminder periods for different bills")
    print()
    
    print(f"{Colors.TITLE}🔍 Search Strategies{Colors.RESET}")
    print("• Use partial names for broader searches")
    print("• Search by website for company-specific bills")
    print("• Use date searches for monthly planning")
    print("• Search all fields when unsure")
    print("• Use auto-complete for faster input")
    print()
    
    print(f"{Colors.TITLE}📋 Template Strategy{Colors.RESET}")
    print("• Create templates for recurring bills")
    print("• Include website and login information")
    print("• Use descriptive template names")
    print("• Update templates when information changes")
    print("• Save existing bills as templates")
    print()
    
    print(f"{Colors.TITLE}📥 CSV Import/Export Tips{Colors.RESET}")
    print("• Use the sample CSV file as a template")
    print("• Export your data regularly for backup")
    print("• Import is great for migrating from other systems")
    print("• Validate your CSV format before importing")
    print("• Use Excel or Google Sheets to create CSV files")
    print()
    
    print(f"{Colors.TITLE}📞 Contact Information{Colors.RESET}")
    print("• Add customer service details for easy access")
    print("• Include account numbers for quick reference")
    print("• Store support phone numbers for emergencies")
    print("• Add mobile app information for convenience")
    print("• Use live chat URLs when available")
    print()
    
    print(f"{Colors.TITLE}💾 Data Safety{Colors.RESET}")
    print("• Backups are created automatically")
    print("• Keep backup files in a safe location")
    print("• Don't delete the bills.json file")
    print("• Export data regularly for additional backup")
    print("• Use CSV export for data portability")
    print()
    
    print(f"{Colors.TITLE}🎨 Interface Tips{Colors.RESET}")
    print("• Color coding helps identify bill status")
    print("• Use pagination for large lists")
    print("• Pay attention to warning messages")
    print("• Read success messages for confirmation")
    print("• Use the help system for detailed guidance")
    print()
    
    print(f"{Colors.TITLE}🚨 Troubleshooting{Colors.RESET}")
    print("• If the app won't start, check file permissions")
    print("• If bills don't load, check bills.json file")
    print("• If dates are wrong, use YYYY-MM-DD format")
    print("• If you see errors, check the backup files")
    print("• If CSV import fails, check the file format")
    print("• If URLs don't work, ensure they include http:// or https://")
    print("• If emails are invalid, check the format (user@domain.com)")
    print()
    
    print(f"{Colors.TITLE}🔄 Billing Cycles{Colors.RESET}")
    print("• Choose the right billing cycle for each bill")
    print("• One-time bills don't recur after payment")
    print("• Recurring bills automatically update due dates")
    print("• Use custom reminder periods for different bills")
    print("• Check upcoming bills calendar for planning")
    print()
    
    colored_input("Press Enter to continue...", Colors.INFO)

def show_csv_import_export_help():
    """Explain CSV import/export functionality."""
    clear_console()
    title_msg("CSV Import/Export Help")
    
    print(f"{Colors.TITLE}📥 Importing Bills from CSV{Colors.RESET}")
    print("The CSV import feature allows you to add multiple bills at once from a CSV file.")
    print()
    print(f"{Colors.INFO}Step-by-step process:{Colors.RESET}")
    print("1. Prepare your CSV file with the correct format")
    print("2. Choose 'CSV Import/Export' from the main menu")
    print("3. Select 'Import bills from CSV'")
    print("4. Enter the path to your CSV file")
    print("5. Review the import results and confirm")
    print()
    
    print(f"{Colors.TITLE}📤 Exporting Bills to CSV{Colors.RESET}")
    print("Export your bills to a CSV file for backup, sharing, or analysis.")
    print()
    print(f"{Colors.INFO}How to export:{Colors.RESET}")
    print("1. Choose 'CSV Import/Export' from the main menu")
    print("2. Select 'Export bills to CSV'")
    print("3. Enter a filename (or use the default)")
    print("4. Confirm the export")
    print()
    
    print(f"{Colors.TITLE}📋 Required CSV Format{Colors.RESET}")
    print("Your CSV file must have these columns (headers are case-insensitive):")
    print()
    print(f"{Colors.WARNING}Required Columns:{Colors.RESET}")
    print(f"  • {Colors.INFO}name{Colors.RESET} - Bill name (required)")
    print(f"  • {Colors.INFO}due_date{Colors.RESET} - Due date in YYYY-MM-DD format (required)")
    print()
    print(f"{Colors.WARNING}Optional Columns:{Colors.RESET}")
    print(f"  • {Colors.INFO}billing_cycle{Colors.RESET} - weekly, bi-weekly, monthly, quarterly, semi-annually, annually, one-time")
    print(f"  • {Colors.INFO}reminder_days{Colors.RESET} - Days before due date for reminders (default: 7)")
    print(f"  • {Colors.INFO}web_page{Colors.RESET} - Website URL")
    print(f"  • {Colors.INFO}login_info{Colors.RESET} - Login information")
    print(f"  • {Colors.INFO}password{Colors.RESET} - Password")
    print(f"  • {Colors.INFO}company_email{Colors.RESET} - Customer service email")
    print(f"  • {Colors.INFO}support_phone{Colors.RESET} - Support phone number")
    print(f"  • {Colors.INFO}billing_phone{Colors.RESET} - Billing phone number")
    print(f"  • {Colors.INFO}customer_service_hours{Colors.RESET} - Service hours")
    print(f"  • {Colors.INFO}account_number{Colors.RESET} - Account number")
    print(f"  • {Colors.INFO}reference_id{Colors.RESET} - Reference ID")
    print(f"  • {Colors.INFO}support_chat_url{Colors.RESET} - Live chat URL")
    print(f"  • {Colors.INFO}mobile_app{Colors.RESET} - Mobile app info")
    print()
    
    print(f"{Colors.TITLE}✅ Validation Features{Colors.RESET}")
    print("The import process includes comprehensive validation:")
    print(f"  • {Colors.SUCCESS}Date format validation{Colors.RESET} - Ensures YYYY-MM-DD format")
    print(f"  • {Colors.SUCCESS}URL validation{Colors.RESET} - Validates and corrects website URLs")
    print(f"  • {Colors.SUCCESS}Email validation{Colors.RESET} - Validates email formats")
    print(f"  • {Colors.SUCCESS}Duplicate detection{Colors.RESET} - Prevents importing duplicate bills")
    print(f"  • {Colors.SUCCESS}Billing cycle validation{Colors.RESET} - Defaults to monthly if invalid")
    print(f"  • {Colors.SUCCESS}Reminder days validation{Colors.RESET} - Ensures 1-365 day range")
    print()
    
    print(f"{Colors.TITLE}📋 Sample CSV File{Colors.RESET}")
    print("Use the 'Create sample CSV file' option to generate a template with:")
    print("  • Correct column headers")
    print("  • Example data for all fields")
    print("  • Proper date format")
    print("  • Contact information examples")
    print()
    
    print(f"{Colors.TITLE}💡 Tips{Colors.RESET}")
    print("  • Use Excel or Google Sheets to create your CSV file")
    print("  • Save as CSV format (not Excel format)")
    print("  • Use UTF-8 encoding for special characters")
    print("  • Test with a small file first")
    print("  • Backup your data before importing")
    print()
    
    print(f"{Colors.TITLE}🚨 Common Issues{Colors.RESET}")
    print("  • Wrong date format - Use YYYY-MM-DD")
    print("  • Missing required columns - name and due_date are required")
    print("  • Duplicate bill names - Each bill must have a unique name")
    print("  • Invalid URLs - Must be valid website addresses")
    print("  • Invalid email format - Must be a valid email address")
    print()
    
    colored_input("Press Enter to continue...", Colors.INFO)

# 2.1 Master password functions
def set_master_password():
    """Prompt the user to set a new master password and store its hash and salt."""
    print("\n🔒 Set up a master password to protect your Bills Tracker data.")
    while True:
        password = getpass.getpass("Enter a new master password: ")
        confirm = getpass.getpass("Confirm master password: ")
        if password != confirm:
            print("❌ Passwords do not match. Try again.")
            continue
        if len(password) < 6:
            print("❌ Password must be at least 6 characters.")
            continue
        break
    salt = os.urandom(16)
    hash_ = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100_000)
    with open(MASTER_PASSWORD_FILE, 'wb') as f:
        f.write(salt + hash_)
    print("✅ Master password set successfully!")
    return password

def verify_master_password():
    """Prompt for the master password and verify it against the stored hash."""
    if not os.path.exists(MASTER_PASSWORD_FILE):
        return set_master_password()
    with open(MASTER_PASSWORD_FILE, 'rb') as f:
        data = f.read()
        salt, stored_hash = data[:16], data[16:]
    for attempt in range(5):
        password = getpass.getpass("Enter master password: ")
        hash_ = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100_000)
        if hash_ == stored_hash:
            print("✅ Access granted.")
            return password
        else:
            print(f"❌ Incorrect password. Attempts left: {4 - attempt}")
    print("❌ Too many incorrect attempts. Exiting.")
    exit(1)

# Session timeout management functions
def start_session():
    """Start the session timer."""
    global session_start_time, last_activity_time, session_locked
    session_start_time = datetime.now()
    last_activity_time = session_start_time
    session_locked = False

def update_activity():
    """Update the last activity time."""
    global last_activity_time
    last_activity_time = datetime.now()

def exit_session():
    """Exit the session immediately."""
    global session_locked
    session_locked = True
    print(f"\n🔒 Session expired due to {SESSION_TIMEOUT_MINUTES} minutes of inactivity.")
    print("🔄 Exiting application for security...")
    success_msg("Thank you for using Bills Tracker! 👋")
    os._exit(0)  # Force exit immediately

# Note: unlock_session and verify_master_password_hash functions removed
# as the app now exits completely on timeout instead of locking

# Entry point
if __name__ == "__main__":
    main()