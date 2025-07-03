import customtkinter as ctk
from tkinter import ttk
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "core"))
from db import fetch_all_bills, insert_bill, update_bill, delete_bill
from datetime import datetime
from tkinter import StringVar
from tkinter import IntVar
import re

BILLING_CYCLES = [
    "weekly", "bi-weekly", "monthly", "quarterly", "semi-annually", "annually", "one-time"
]
REMINDER_DAYS = [1, 3, 5, 7, 10, 14, 30]

def show_popup(master, title, message, color="green"):
    popup = ctk.CTkToplevel(master)
    popup.title(title)
    popup.geometry("350x120")
    label = ctk.CTkLabel(popup, text=message, text_color=color, font=("Arial", 14))
    label.pack(pady=20)
    ctk.CTkButton(popup, text="OK", command=popup.destroy).pack(pady=10)
    popup.lift()
    popup.focus_force()
    popup.grab_set()

EMAIL_REGEX = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
PHONE_REGEX = r"^[\d\-\+\(\)\s]+$"

class AddBillDialog(ctk.CTkToplevel):
    def __init__(self, master, on_success):
        super().__init__(master)
        self.title("Add Bill")
        self.geometry("500x500")
        self.on_success = on_success
        self._setup_ui()
        self.lift()
        self.focus_force()
        self.grab_set()

    def _setup_ui(self):
        self.grid_columnconfigure(1, weight=1)
        row = 0
        # Name
        ctk.CTkLabel(self, text="Name:").grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        # Due Date
        ctk.CTkLabel(self, text="Due Date (YYYY-MM-DD):").grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.due_date_entry = ctk.CTkEntry(self)
        self.due_date_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        # Paid
        ctk.CTkLabel(self, text="Paid:").grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.paid_var = ctk.BooleanVar()
        self.paid_checkbox = ctk.CTkCheckBox(self, variable=self.paid_var, text="Yes")
        self.paid_checkbox.grid(row=row, column=1, padx=10, pady=5, sticky="w")
        row += 1
        # Billing Cycle (dropdown)
        ctk.CTkLabel(self, text="Billing Cycle:").grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.billing_cycle_var = StringVar(value=BILLING_CYCLES[2])
        self.billing_cycle_combo = ttk.Combobox(self, textvariable=self.billing_cycle_var, values=BILLING_CYCLES, state="readonly")
        self.billing_cycle_combo.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        # Reminder Days (dropdown)
        ctk.CTkLabel(self, text="Reminder Days:").grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.reminder_days_var = IntVar(value=7)
        self.reminder_days_combo = ttk.Combobox(self, textvariable=self.reminder_days_var, values=REMINDER_DAYS, state="readonly")
        self.reminder_days_combo.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        # Web Page
        ctk.CTkLabel(self, text="Web Page:").grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.web_page_entry = ctk.CTkEntry(self)
        self.web_page_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        # Company Email
        ctk.CTkLabel(self, text="Company Email:").grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.company_email_entry = ctk.CTkEntry(self)
        self.company_email_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        # Support Phone
        ctk.CTkLabel(self, text="Support Phone:").grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.support_phone_entry = ctk.CTkEntry(self)
        self.support_phone_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        # Account Number
        ctk.CTkLabel(self, text="Account Number:").grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.account_number_entry = ctk.CTkEntry(self)
        self.account_number_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        # Error label
        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.grid(row=row, column=0, columnspan=2)
        row += 1
        # Add button
        self.add_button = ctk.CTkButton(self, text="Add", command=self._on_add)
        self.add_button.grid(row=row, column=0, columnspan=2, pady=20)

    def _on_add(self):
        name = self.name_entry.get().strip()
        due_date = self.due_date_entry.get().strip()
        paid = self.paid_var.get()
        billing_cycle = self.billing_cycle_var.get()
        reminder_days = self.reminder_days_var.get()
        web_page = self.web_page_entry.get().strip()
        company_email = self.company_email_entry.get().strip()
        support_phone = self.support_phone_entry.get().strip()
        account_number = self.account_number_entry.get().strip()
        # Basic validation
        if not name or not due_date:
            self.error_label.configure(text="Name and Due Date are required.")
            show_popup(self, "Error", "Name and Due Date are required.", color="red")
            return
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            self.error_label.configure(text="Invalid date format. Use YYYY-MM-DD.")
            show_popup(self, "Error", "Invalid date format. Use YYYY-MM-DD.", color="red")
            return
        if company_email and not re.match(EMAIL_REGEX, company_email):
            self.error_label.configure(text="Invalid email address.")
            show_popup(self, "Error", "Invalid email address.", color="red")
            return
        if support_phone and not re.match(PHONE_REGEX, support_phone):
            self.error_label.configure(text="Invalid phone number.")
            show_popup(self, "Error", "Invalid phone number.", color="red")
            return
        if web_page and not (web_page.startswith("http://") or web_page.startswith("https://")):
            self.error_label.configure(text="Web page must start with http:// or https://")
            show_popup(self, "Error", "Web page must start with http:// or https://", color="red")
            return
        bill_data = {
            "name": name,
            "due_date": due_date,
            "paid": paid,
            "billing_cycle": billing_cycle,
            "reminder_days": reminder_days,
            "web_page": web_page,
            "company_email": company_email,
            "support_phone": support_phone,
            "account_number": account_number
        }
        insert_bill(bill_data)
        show_popup(self, "Success", "Bill added successfully!", color="green")
        self.on_success()
        self.destroy()

class EditBillDialog(ctk.CTkToplevel):
    def __init__(self, master, bill_data, on_success):
        super().__init__(master)
        self.title("Edit Bill")
        self.geometry("500x500")
        self.bill_data = bill_data
        self.on_success = on_success
        self._setup_ui()
        self.lift()
        self.focus_force()
        self.grab_set()

    def _setup_ui(self):
        self.grid_columnconfigure(1, weight=1)
        row = 0
        # Name
        ctk.CTkLabel(self, text="Name:").grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.insert(0, self.bill_data.get("name", ""))
        self.name_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        # Due Date
        ctk.CTkLabel(self, text="Due Date (YYYY-MM-DD):").grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.due_date_entry = ctk.CTkEntry(self)
        self.due_date_entry.insert(0, self.bill_data.get("due_date", ""))
        self.due_date_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        # Paid
        ctk.CTkLabel(self, text="Paid:").grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.paid_var = ctk.BooleanVar(value=self.bill_data.get("paid", False))
        self.paid_checkbox = ctk.CTkCheckBox(self, variable=self.paid_var, text="Yes")
        self.paid_checkbox.grid(row=row, column=1, padx=10, pady=5, sticky="w")
        row += 1
        # Billing Cycle (dropdown)
        ctk.CTkLabel(self, text="Billing Cycle:").grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.billing_cycle_var = StringVar(value=self.bill_data.get("billing_cycle", BILLING_CYCLES[2]))
        self.billing_cycle_combo = ttk.Combobox(self, textvariable=self.billing_cycle_var, values=BILLING_CYCLES, state="readonly")
        self.billing_cycle_combo.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        # Reminder Days (dropdown)
        ctk.CTkLabel(self, text="Reminder Days:").grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.reminder_days_var = IntVar(value=self.bill_data.get("reminder_days", 7))
        self.reminder_days_combo = ttk.Combobox(self, textvariable=self.reminder_days_var, values=REMINDER_DAYS, state="readonly")
        self.reminder_days_combo.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        # Web Page
        ctk.CTkLabel(self, text="Web Page:").grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.web_page_entry = ctk.CTkEntry(self)
        self.web_page_entry.insert(0, self.bill_data.get("web_page", ""))
        self.web_page_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        # Company Email
        ctk.CTkLabel(self, text="Company Email:").grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.company_email_entry = ctk.CTkEntry(self)
        self.company_email_entry.insert(0, self.bill_data.get("company_email", ""))
        self.company_email_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        # Support Phone
        ctk.CTkLabel(self, text="Support Phone:").grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.support_phone_entry = ctk.CTkEntry(self)
        self.support_phone_entry.insert(0, self.bill_data.get("support_phone", ""))
        self.support_phone_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        # Account Number
        ctk.CTkLabel(self, text="Account Number:").grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.account_number_entry = ctk.CTkEntry(self)
        self.account_number_entry.insert(0, self.bill_data.get("account_number", ""))
        self.account_number_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        # Error label
        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.grid(row=row, column=0, columnspan=2)
        row += 1
        # Save button
        self.save_button = ctk.CTkButton(self, text="Save", command=self._on_save)
        self.save_button.grid(row=row, column=0, columnspan=2, pady=20)

    def _on_save(self):
        name = self.name_entry.get().strip()
        due_date = self.due_date_entry.get().strip()
        paid = self.paid_var.get()
        billing_cycle = self.billing_cycle_var.get()
        reminder_days = self.reminder_days_var.get()
        web_page = self.web_page_entry.get().strip()
        company_email = self.company_email_entry.get().strip()
        support_phone = self.support_phone_entry.get().strip()
        account_number = self.account_number_entry.get().strip()
        if not name or not due_date:
            self.error_label.configure(text="Name and Due Date are required.")
            show_popup(self, "Error", "Name and Due Date are required.", color="red")
            return
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            self.error_label.configure(text="Invalid date format. Use YYYY-MM-DD.")
            show_popup(self, "Error", "Invalid date format. Use YYYY-MM-DD.", color="red")
            return
        if company_email and not re.match(EMAIL_REGEX, company_email):
            self.error_label.configure(text="Invalid email address.")
            show_popup(self, "Error", "Invalid email address.", color="red")
            return
        if support_phone and not re.match(PHONE_REGEX, support_phone):
            self.error_label.configure(text="Invalid phone number.")
            show_popup(self, "Error", "Invalid phone number.", color="red")
            return
        if web_page and not (web_page.startswith("http://") or web_page.startswith("https://")):
            self.error_label.configure(text="Web page must start with http:// or https://")
            show_popup(self, "Error", "Web page must start with http:// or https://", color="red")
            return
        bill_data = self.bill_data.copy()
        bill_data["name"] = name
        bill_data["due_date"] = due_date
        bill_data["paid"] = paid
        bill_data["billing_cycle"] = billing_cycle
        bill_data["reminder_days"] = reminder_days
        bill_data["web_page"] = web_page
        bill_data["company_email"] = company_email
        bill_data["support_phone"] = support_phone
        bill_data["account_number"] = account_number
        update_bill(bill_data["id"], bill_data)
        show_popup(self, "Success", "Bill updated successfully!", color="green")
        self.on_success()
        self.destroy()

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Bills Tracker Desktop")
        self.geometry("900x600")
        self._setup_ui()

    def _setup_ui(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=180, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nswe")
        self.sidebar.grid_rowconfigure(3, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar, text="Bills Tracker", font=("Arial", 20, "bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.bills_button = ctk.CTkButton(self.sidebar, text="Bills", command=self.show_bills_view)
        self.bills_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.categories_button = ctk.CTkButton(self.sidebar, text="Categories", command=self.show_categories_view)
        self.categories_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.settings_button = ctk.CTkButton(self.sidebar, text="Settings", command=self.show_settings_view)
        self.settings_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        # Main content area
        self.content = ctk.CTkFrame(self, corner_radius=10)
        self.content.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        # Initialize views
        self.bills_table_frame = None
        self.categories_frame = None
        self.settings_frame = None
        self.show_bills_view()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_bills_view(self):
        self.clear_content()
        add_btn = ctk.CTkButton(self.content, text="Add Bill", command=self.open_add_bill_dialog)
        add_btn.grid(row=0, column=0, sticky="w", padx=10, pady=(0, 10))

        self.bills_table_frame = ctk.CTkFrame(self.content)
        self.bills_table_frame.grid(row=1, column=0, sticky="nswe")
        self.bills_table_frame.grid_rowconfigure(0, weight=1)
        self.bills_table_frame.grid_columnconfigure(0, weight=1)

        columns = ("Name", "Due Date", "Amount", "Category", "Status")
        self.bills_table = ttk.Treeview(self.bills_table_frame, columns=columns, show="headings", height=15)
        for col in columns:
            self.bills_table.heading(col, text=col)
            self.bills_table.column(col, width=120, anchor="center")

        self.bills_by_id = {}  # id -> bill dict
        bills = fetch_all_bills()
        for bill in bills:
            row = (
                bill.get("name", ""),
                bill.get("due_date", ""),
                bill.get("amount", ""),
                bill.get("category", ""),
                "Paid" if bill.get("paid", False) else "Pending"
            )
            item_id = self.bills_table.insert("", "end", values=row)
            self.bills_by_id[item_id] = bill

        scrollbar = ttk.Scrollbar(self.bills_table_frame, orient="vertical", command=self.bills_table.yview)
        self.bills_table.configure(yscrollcommand=scrollbar.set)
        self.bills_table.grid(row=0, column=0, sticky="nswe")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Edit and Delete buttons
        btn_frame = ctk.CTkFrame(self.content)
        btn_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        edit_btn = ctk.CTkButton(btn_frame, text="Edit", command=self.edit_selected_bill)
        edit_btn.pack(side="left", padx=10)
        delete_btn = ctk.CTkButton(btn_frame, text="Delete", command=self.delete_selected_bill)
        delete_btn.pack(side="left", padx=10)

    def open_add_bill_dialog(self):
        AddBillDialog(self, self.show_bills_view)

    def show_categories_view(self):
        self.clear_content()
        self.categories_frame = ctk.CTkFrame(self.content)
        self.categories_frame.grid(row=0, column=0, sticky="nswe")
        label = ctk.CTkLabel(self.categories_frame, text="Categories View (Coming Soon)", font=("Arial", 18))
        label.pack(padx=40, pady=40)

    def show_settings_view(self):
        self.clear_content()
        self.settings_frame = ctk.CTkFrame(self.content)
        self.settings_frame.grid(row=0, column=0, sticky="nswe")
        label = ctk.CTkLabel(self.settings_frame, text="Settings View (Coming Soon)", font=("Arial", 18))
        label.pack(padx=40, pady=40)

    def edit_selected_bill(self):
        selected = self.bills_table.selection()
        if not selected:
            return
        bill = self.bills_by_id[selected[0]]
        EditBillDialog(self, bill, self.show_bills_view)

    def delete_selected_bill(self):
        selected = self.bills_table.selection()
        if not selected:
            return
        bill = self.bills_by_id[selected[0]]
        # Confirmation dialog
        confirm = ctk.CTkToplevel(self)
        confirm.title("Confirm Delete")
        confirm.geometry("300x120")
        ctk.CTkLabel(confirm, text=f"Delete bill '{bill.get('name', '')}'?").pack(pady=20)
        def do_delete():
            delete_bill(bill["id"])
            show_popup(self, "Success", "Bill deleted successfully!", color="green")
            self.show_bills_view()
            confirm.destroy()
        ctk.CTkButton(confirm, text="Delete", fg_color="red", command=do_delete).pack(side="left", padx=20, pady=10)
        ctk.CTkButton(confirm, text="Cancel", command=confirm.destroy).pack(side="right", padx=20, pady=10)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop() 