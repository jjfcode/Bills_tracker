import json
import os
from datetime import datetime, timedelta

bills_file = 'bills.json'
bills = []

# Function to clear the console
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

#Load existing bills from a file JSON
try:
    with open(bills_file, 'r') as f: 
        bills = json.load(f)
except FileNotFoundError:
    bills = []

# Function to save bills to a file JSON
def save_bills():
    with open(bills_file, 'w') as f:
        json.dump(bills, f, indent=4)

# Function input required
def input_required(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        else:
            clear_console()
            print("This field is required. Please enter a value or type 'cancel' to cancel.")

# Helper function to input with cancel option
def input_with_cancel(prompt):
    value = input(prompt).strip()
    if value.lower() == 'cancel':
        clear_console()
        return None
    if value:
        return value
    print("This field is required. Please enter a value or type 'cancel' to cancel.")
    return value

# Function to add a bill with duplicate check
def add_bill():
    print("\n--- Add a New Bill ---")
    print("Type 'cancel' at any time to cancel.\n")

    # Ask for bill name and check for duplicates
    while True:
        name = input_required("Enter the name of the bill:")
        if name.lower() == 'cancel':
            print("Bill addition cancelled.")
            clear_console()
            return
        # Check if a bill with the same name already exists
        if any(bill['name'].lower() == name.lower() for bill in bills):
            clear_console()
            print(f"A bill with the name '{name}' already exists. Please enter a different name.")
        else:
            break

    # Continue asking for other details
    due_date = input_required("Enter the due date of the bill (YYYY-MM-DD):")
    if due_date.lower() == 'cancel':
        print("Bill addition cancelled.")
        clear_console()
        return
    
    web_page = input("Enter the web page for the bill:")
    if web_page.lower() == 'cancel':
        print("Bill addition cancelled.")
        clear_console()
        return
    
    login_info = input_with_cancel("Enter the login information for the bill:")
    if login_info.lower() == 'cancel':
        print("Bill addition cancelled.")
        clear_console()
        return
    
    password = input_with_cancel("Enter the password for the bill:")
    if password is None:
        print("Bill addition cancelled.")
        clear_console()
        return

    # Add the bill if all fields are provided
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
    print(f"Bill '{name}' added successfully!")
    clear_console()

# Function to view all bills
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

# Function to Verify Due Bills
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

# Function to Pay a Bill
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
                clear_console()
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
                clear_console()
                print(f"Bill '{bill['name']}' marked as paid. Next due date set to {bill['due_date']}.")
            except ValueError:
                clear_console()
                print("Invalid date format, Cannot update due date.")
            save_bills()
        else:
            clear_console()
            print("Invalid selection.")
    except ValueError:
        print("Invalid input. Please enter a number.")

# Function to Edit a Bill
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
            clear_console()
            print(f"Bill '{bill['name']}' updated successfully.")
        else:
            clear_console()
            print("Invalid selection.")
    except ValueError:
        print("Invalid input. Please enter a number.")

# Function Principal
def main():
    clear_console()
    while True:
        print("--- Bills Tracker ---")
        print("1. Add a bill")
        print("2. View all bills")
        print("3. Verify due bills")
        print("4. Pay a bill")
        print("5. Edit a bill")
        print("6. Exit")
        option = input("Choose an option: ")

        if option == '1':
            clear_console()
            add_bill()
        elif option == '2':
            clear_console()
            view_bills()
        elif option == '3':
            clear_console()
            verify_due_bills()
        elif option == '4':
            clear_console()
            pay_bill()
        elif option == '5':
            clear_console()
            edit_bill()
        elif option == '6':
            print("Exiting the program.")
            clear_console()
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()