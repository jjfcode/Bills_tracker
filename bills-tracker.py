import json
from datetime import datetime, timedelta

bills_file = 'bills.json'
bills = []

#Load existing bills from a file JSON
try:
    with open(bills_file, 'r') as f: 
        bills = json.load(f)
except FileNotFoundError:
    bills = []


def save_bills():
    with open(bills_file, 'w') as f:
        json.dump(bills, f, indent=4)

# Function to add a bill
def add_bill():
    print("\n--- Add a New Bill ---")
    name = input("Enter the name of the bill: ")
    due_date = input("Enter the due date of the bill (YYYY-MM-DD): ")
    web_page = input("Enter the web page for the bill: ")
    login_info = input("Enter the login information for the bill: ")
    password = input("Enter the password for the bill: ")

    bill = {
        "name": name,
        "due_date": due_date,
        "web_page": web_page,
        "login_info": login_info,
        "password": password
    }
    bills.append(bill)
    save_bills()
    print(f"Bill '{name}' added successfully!")

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
                print("nvalid date format, Cannot update due date.")
            save_bills()
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input. Please enter a number.")

# Function Principal
def main():
    while True:
        print("--- Bills Tracker ---")
        print("1. Add a bill")
        print("2. View all bills")
        print("3. Verify due bills")
        print("4. Pay a bill")
        print("5. Exit")
        option = input("Choose an option: ")

        if option == '1':
            add_bill()
        elif option == '2':
            view_bills()
        elif option == '3':
            verify_due_bills()
        elif option == '4':
            pay_bill()
        elif option == '5':
            print("Exiting the program.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()