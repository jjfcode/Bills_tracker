import customtkinter as ctk
from tkinter import ttk
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "core"))
from db import fetch_all_bills, insert_bill, update_bill, delete_bill
from datetime import datetime, timedelta
from tkinter import StringVar
from tkinter import IntVar
import re
import csv
from tkinter import filedialog

BILLING_CYCLES = [
    "weekly", "bi-weekly", "monthly", "quarterly", "semi-annually", "annually", "one-time"
]
REMINDER_DAYS = [1, 3, 5, 7, 10, 14, 30]

def show_popup(master, title, message, color="green"):
    try:
        popup = ctk.CTkToplevel(master)
        popup.title(title)
        popup.geometry("350x120")
        
        def close_popup():
            try:
                if popup.winfo_exists():
                    popup.destroy()
            except:
                pass
        
        label = ctk.CTkLabel(popup, text=message, text_color=color, font=("Arial", 14))
        label.pack(pady=20)
        ctk.CTkButton(popup, text="OK", command=close_popup).pack(pady=10)
        
        # Use after() to delay the focus operations
        def set_focus():
            try:
                if popup.winfo_exists():
                    popup.lift()
                    popup.focus_force()
                    popup.grab_set()
            except:
                pass
        
        popup.after(100, set_focus)
        
    except Exception as e:
        # If popup creation fails, just print the message to console
        print(f"Popup Error: {title} - {message}")

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
        self.title("Bills Tracker v3")
        self.geometry("1200x800")
        self._setup_ui()
        self.pending_changes = {}  # item_id -> bill_data for pending changes

    def _setup_ui(self):
        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.grid(row=0, column=0, sticky="nswe")
        self.sidebar.grid_rowconfigure(4, weight=1)

        # Sidebar buttons
        ctk.CTkLabel(self.sidebar, text="Bills Tracker", font=("Arial", 20, "bold")).grid(row=0, column=0, padx=20, pady=(20, 10))
        ctk.CTkButton(self.sidebar, text="Bills", command=self.show_bills_view).grid(row=1, column=0, padx=20, pady=10)
        ctk.CTkButton(self.sidebar, text="Categories", command=self.show_categories_view).grid(row=2, column=0, padx=20, pady=10)
        ctk.CTkButton(self.sidebar, text="Settings", command=self.show_settings_view).grid(row=3, column=0, padx=20, pady=10)

        # Main content area
        self.content = ctk.CTkFrame(self)
        self.content.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

        # Show bills view by default
        self.show_bills_view()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_bills_view(self):
        self.clear_content()
        
        # Button frame for Add, Export, Import
        btn_frame = ctk.CTkFrame(self.content)
        btn_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(0, 10))
        btn_frame.grid_columnconfigure(3, weight=1)
        
        add_btn = ctk.CTkButton(btn_frame, text="Add Bill", command=self.open_add_bill_dialog)
        add_btn.grid(row=0, column=0, padx=(0, 10), pady=10)
        
        export_btn = ctk.CTkButton(btn_frame, text="Export CSV", command=self.export_bills)
        export_btn.grid(row=0, column=1, padx=(0, 10), pady=10)
        
        import_btn = ctk.CTkButton(btn_frame, text="Import CSV", command=self.import_bills)
        import_btn.grid(row=0, column=2, padx=(0, 10), pady=10)

        # Search/Filter bar
        search_frame = ctk.CTkFrame(self.content)
        search_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        search_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(search_frame, text="Search:").grid(row=0, column=0, padx=(10, 5), pady=10)
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var)
        self.search_entry.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        self.search_var.trace("w", self.filter_bills)
        
        self.search_field_var = ctk.StringVar(value="Name")
        search_field_combo = ttk.Combobox(search_frame, textvariable=self.search_field_var, 
                                         values=["Name", "Due Date", "Category", "Status", "Paid"], 
                                         state="readonly", width=15)
        search_field_combo.grid(row=0, column=2, padx=5, pady=10)
        
        clear_btn = ctk.CTkButton(search_frame, text="Clear", command=self.clear_filter, width=60)
        clear_btn.grid(row=0, column=3, padx=5, pady=10)

        self.bills_table_frame = ctk.CTkFrame(self.content)
        self.bills_table_frame.grid(row=2, column=0, sticky="nswe")
        self.bills_table_frame.grid_rowconfigure(0, weight=1)
        self.bills_table_frame.grid_columnconfigure(0, weight=1)

        columns = ("Paid", "Name", "Due Date", "Amount", "Category", "Status")
        self.bills_table = ttk.Treeview(self.bills_table_frame, columns=columns, show="headings", height=15)
        self._sort_column = None
        self._sort_reverse = False
        
        # Configure columns
        self.bills_table.heading("Paid", text="Paid", command=lambda c="Paid": self.sort_by_column(c))
        self.bills_table.column("Paid", width=60, anchor="center")
        
        for col in ["Name", "Due Date", "Amount", "Category", "Status"]:
            self.bills_table.heading(col, text=col, command=lambda c=col: self.sort_by_column(c))
            self.bills_table.column(col, width=120, anchor="center")
        
        # Bind checkbox click event
        self.bills_table.bind("<Button-1>", self.on_table_click)

        self.bills_by_id = {}  # id -> bill dict
        self._bills_data = fetch_all_bills()
        self._filtered_bills = self._bills_data.copy()
        self.populate_bills_table(self._filtered_bills)

        scrollbar = ttk.Scrollbar(self.bills_table_frame, orient="vertical", command=self.bills_table.yview)
        self.bills_table.configure(yscrollcommand=scrollbar.set)
        self.bills_table.grid(row=0, column=0, sticky="nswe")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Edit, Delete, Apply, and Refresh buttons
        action_btn_frame = ctk.CTkFrame(self.content)
        action_btn_frame.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        edit_btn = ctk.CTkButton(action_btn_frame, text="Edit", command=self.edit_selected_bill)
        edit_btn.pack(side="left", padx=10)
        delete_btn = ctk.CTkButton(action_btn_frame, text="Delete", command=self.delete_selected_bill)
        delete_btn.pack(side="left", padx=10)
        refresh_btn = ctk.CTkButton(action_btn_frame, text="Refresh Data", command=self.refresh_bills_data, fg_color="blue")
        refresh_btn.pack(side="right", padx=10)
        self.apply_btn = ctk.CTkButton(action_btn_frame, text="Apply Changes", command=self.apply_pending_changes, fg_color="green")
        self.apply_btn.pack(side="right", padx=10)

    def filter_bills(self, *args):
        search_term = self.search_var.get().lower()
        search_field = self.search_field_var.get()
        
        if not search_term:
            self._filtered_bills = self._bills_data.copy()
        else:
            self._filtered_bills = []
            for bill in self._bills_data:
                if search_field == "Name":
                    if search_term in bill.get("name", "").lower():
                        self._filtered_bills.append(bill)
                elif search_field == "Due Date":
                    if search_term in bill.get("due_date", "").lower():
                        self._filtered_bills.append(bill)
                elif search_field == "Category":
                    if search_term in bill.get("category", "").lower():
                        self._filtered_bills.append(bill)
                elif search_field == "Status":
                    status = "Paid" if bill.get("paid", False) else "Pending"
                    if search_term in status.lower():
                        self._filtered_bills.append(bill)
                elif search_field == "Paid":
                    paid_status = "paid" if bill.get("paid", False) else "unpaid"
                    if search_term in paid_status.lower():
                        self._filtered_bills.append(bill)
        
        # Maintain current sort order
        if self._sort_column:
            self.sort_by_column(self._sort_column)
        else:
            self.populate_bills_table(self._filtered_bills)

    def clear_filter(self):
        self.search_var.set("")
        self._filtered_bills = self._bills_data.copy()
        if self._sort_column:
            self.sort_by_column(self._sort_column)
        else:
            self.populate_bills_table(self._filtered_bills)

    def populate_bills_table(self, bills):
        for row in self.bills_table.get_children():
            self.bills_table.delete(row)
        self.bills_by_id = {}
        for bill in bills:
            paid_status = "✓" if bill.get("paid", False) else "☐"
            row = (
                paid_status,
                bill.get("name", ""),
                bill.get("due_date", ""),
                bill.get("amount", ""),
                bill.get("category", ""),
                "Paid" if bill.get("paid", False) else "Pending"
            )
            item_id = self.bills_table.insert("", "end", values=row)
            self.bills_by_id[item_id] = bill

    def sort_by_column(self, col):
        col_map = {
            "Paid": "paid",
            "Name": "name",
            "Due Date": "due_date",
            "Amount": "amount",
            "Category": "category",
            "Status": "paid"
        }
        key = col_map.get(col, col)
        reverse = False
        if self._sort_column == col:
            reverse = not self._sort_reverse
        self._sort_column = col
        self._sort_reverse = reverse
        # For status, sort by paid boolean
        if key == "paid":
            sorted_bills = sorted(self._filtered_bills, key=lambda b: b.get("paid", False), reverse=reverse)
        else:
            sorted_bills = sorted(self._filtered_bills, key=lambda b: (b.get(key) or ""), reverse=reverse)
        self.populate_bills_table(sorted_bills)
        # Update header text to show sort order
        for c in ("Paid", "Name", "Due Date", "Amount", "Category", "Status"):
            arrow = ""
            if c == col:
                arrow = " ↓" if reverse else " ↑"
            self.bills_table.heading(c, text=c + arrow, command=lambda c=c: self.sort_by_column(c))

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
        
        try:
            # Confirmation dialog
            confirm = ctk.CTkToplevel(self)
            confirm.title("Confirm Delete")
            confirm.geometry("300x120")
            
            def safe_destroy():
                try:
                    if confirm.winfo_exists():
                        confirm.destroy()
                except:
                    pass
            
            ctk.CTkLabel(confirm, text=f"Delete bill '{bill.get('name', '')}'?").pack(pady=20)
            
            def do_delete():
                try:
                    delete_bill(bill["id"])
                    show_popup(self, "Success", "Bill deleted successfully!", color="green")
                    self.show_bills_view()
                except Exception as e:
                    show_popup(self, "Error", f"Failed to delete bill: {str(e)}", color="red")
                safe_destroy()
            
            ctk.CTkButton(confirm, text="Delete", fg_color="red", command=do_delete).pack(side="left", padx=20, pady=10)
            ctk.CTkButton(confirm, text="Cancel", command=safe_destroy).pack(side="right", padx=20, pady=10)
            
            # Use after() to delay the focus operations
            def set_focus():
                try:
                    if confirm.winfo_exists():
                        confirm.lift()
                        confirm.focus_force()
                        confirm.grab_set()
                except:
                    pass
            
            confirm.after(100, set_focus)
            
        except Exception as e:
            print(f"Delete confirm dialog error: {e}")
            # Fallback: delete directly
            try:
                delete_bill(bill["id"])
                show_popup(self, "Success", "Bill deleted successfully!", color="green")
                self.show_bills_view()
            except Exception as e:
                show_popup(self, "Error", f"Failed to delete bill: {str(e)}", color="red")

    def export_bills(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export Bills to CSV"
        )
        if not file_path:
            return
        
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['name', 'due_date', 'billing_cycle', 'reminder_days', 'web_page', 
                             'company_email', 'support_phone', 'account_number', 'paid']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for bill in self._bills_data:
                    writer.writerow({
                        'name': bill.get('name', ''),
                        'due_date': bill.get('due_date', ''),
                        'billing_cycle': bill.get('billing_cycle', ''),
                        'reminder_days': bill.get('reminder_days', ''),
                        'web_page': bill.get('web_page', ''),
                        'company_email': bill.get('company_email', ''),
                        'support_phone': bill.get('support_phone', ''),
                        'account_number': bill.get('account_number', ''),
                        'paid': 'Yes' if bill.get('paid', False) else 'No'
                    })
            
            show_popup(self, "Success", f"Exported {len(self._bills_data)} bills to {os.path.basename(file_path)}", color="green")
        except Exception as e:
            show_popup(self, "Error", f"Failed to export bills: {str(e)}", color="red")

    def import_bills(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Import Bills from CSV"
        )
        if not file_path:
            return
        
        try:
            imported_count = 0
            skipped_count = 0
            
            with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Basic validation
                    if not row.get('name') or not row.get('due_date'):
                        skipped_count += 1
                        continue
                    
                    # Check for duplicate by name and due date
                    is_duplicate = False
                    for existing_bill in self._bills_data:
                        if (existing_bill.get('name') == row['name'] and 
                            existing_bill.get('due_date') == row['due_date']):
                            is_duplicate = True
                            break
                    
                    if is_duplicate:
                        skipped_count += 1
                        continue
                    
                    # Prepare bill data
                    bill_data = {
                        'name': row.get('name', ''),
                        'due_date': row.get('due_date', ''),
                        'billing_cycle': row.get('billing_cycle', 'monthly'),
                        'reminder_days': int(row.get('reminder_days', 7)),
                        'web_page': row.get('web_page', ''),
                        'company_email': row.get('company_email', ''),
                        'support_phone': row.get('support_phone', ''),
                        'account_number': row.get('account_number', ''),
                        'paid': row.get('paid', 'No').lower() == 'yes'
                    }
                    
                    insert_bill(bill_data)
                    imported_count += 1
            
            # Refresh the bills data and table
            self._bills_data = fetch_all_bills()
            self._filtered_bills = self._bills_data.copy()
            if self._sort_column:
                self.sort_by_column(self._sort_column)
            else:
                self.populate_bills_table(self._filtered_bills)
            
            message = f"Imported {imported_count} bills successfully!"
            if skipped_count > 0:
                message += f" Skipped {skipped_count} bills (duplicates or invalid data)."
            show_popup(self, "Success", message, color="green")
            
        except Exception as e:
            show_popup(self, "Error", f"Failed to import bills: {str(e)}", color="red")

    def on_table_click(self, event):
        """Handle clicks on the table, specifically for checkbox column"""
        region = self.bills_table.identify("region", event.x, event.y)
        if region == "cell":
            column = self.bills_table.identify_column(event.x)
            if column == "#1":  # Paid column (first column)
                item = self.bills_table.identify_row(event.y)
                if item:
                    self.toggle_paid_status(item)
    
    def toggle_paid_status(self, item_id):
        """Toggle the paid status of a bill in the table and store as pending change"""
        if item_id in self.bills_by_id:
            bill = self.bills_by_id[item_id]
            current_paid = bill.get("paid", False)
            new_paid = not current_paid
            
            # Create a copy of the bill for pending changes
            pending_bill = bill.copy()
            pending_bill["paid"] = new_paid
            
            # Store the pending change (keep original due date for current bill)
            self.pending_changes[item_id] = pending_bill
            
            # Update the display
            paid_status = "✓" if new_paid else "☐"
            values = list(self.bills_table.item(item_id, "values"))
            values[0] = paid_status  # Update paid column
            values[5] = "Paid" if new_paid else "Pending"  # Update status column
            # Keep the original due date in the display
            self.bills_table.item(item_id, values=values)
            
            # Update the button text to show pending changes
            pending_count = len(self.pending_changes)
            if pending_count > 0:
                self.apply_btn.configure(text=f"Apply Changes ({pending_count})", fg_color="orange")
            else:
                self.apply_btn.configure(text="Apply Changes", fg_color="green")
    
    def _calculate_next_due_date(self, current_due_date, billing_cycle):
        """Calculate the next due date based on billing cycle"""
        try:
            current_date = datetime.strptime(current_due_date, "%Y-%m-%d")
        except ValueError:
            return current_due_date
        
        if billing_cycle == "weekly":
            next_date = current_date + timedelta(weeks=1)
        elif billing_cycle == "bi-weekly":
            next_date = current_date + timedelta(weeks=2)
        elif billing_cycle == "monthly":
            # Add one month, handling year rollover
            if current_date.month == 12:
                next_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                next_date = current_date.replace(month=current_date.month + 1)
        elif billing_cycle == "quarterly":
            # Add 3 months
            new_month = current_date.month + 3
            new_year = current_date.year + (new_month - 1) // 12
            new_month = ((new_month - 1) % 12) + 1
            next_date = current_date.replace(year=new_year, month=new_month)
        elif billing_cycle == "semi-annually":
            # Add 6 months
            new_month = current_date.month + 6
            new_year = current_date.year + (new_month - 1) // 12
            new_month = ((new_month - 1) % 12) + 1
            next_date = current_date.replace(year=new_year, month=new_month)
        elif billing_cycle == "annually":
            next_date = current_date.replace(year=current_date.year + 1)
        else:  # one-time or unknown
            return current_due_date
        
        return next_date.strftime("%Y-%m-%d")
    
    def apply_pending_changes(self):
        """Apply all pending changes to the database"""
        if not self.pending_changes:
            show_popup(self, "Info", "No changes to apply.", color="blue")
            return
        
        try:
            applied_count = 0
            new_bills_created = 0
            
            for item_id, pending_bill in self.pending_changes.items():
                # Update the current bill in the database (mark as paid)
                update_bill(pending_bill["id"], pending_bill)
                
                # Update the main bills data
                for i, main_bill in enumerate(self._bills_data):
                    if main_bill["id"] == pending_bill["id"]:
                        self._bills_data[i] = pending_bill.copy()
                        break
                
                # Update the bills_by_id reference
                self.bills_by_id[item_id] = pending_bill.copy()
                
                # If the bill was marked as paid, create a new bill for the next cycle
                if pending_bill.get("paid", False):
                    # Get the original bill data to calculate the next due date
                    original_bill = None
                    for main_bill in self._bills_data:
                        if main_bill["id"] == pending_bill["id"]:
                            original_bill = main_bill
                            break
                    
                    if original_bill:
                        # Calculate the next due date based on the original bill's due date and billing cycle
                        next_due_date = self._calculate_next_due_date(
                            original_bill.get("due_date", ""), 
                            original_bill.get("billing_cycle", "monthly")
                        )
                        
                        # Create new bill data for next cycle
                        next_bill_data = pending_bill.copy()
                        next_bill_data["paid"] = False  # New bill is unpaid
                        next_bill_data["due_date"] = next_due_date  # Use the calculated next due date
                        
                        # Remove the id so it creates a new entry
                        if "id" in next_bill_data:
                            del next_bill_data["id"]
                        
                        # Insert the new bill into the database
                        insert_bill(next_bill_data)
                        new_bills_created += 1
                
                applied_count += 1
            
            # Clear pending changes
            self.pending_changes.clear()
            
            # Reset button appearance
            self.apply_btn.configure(text="Apply Changes", fg_color="green")
            
            # Refresh the data to show the new bills
            self._bills_data = fetch_all_bills()
            self._filtered_bills = self._bills_data.copy()
            if self._sort_column:
                self.sort_by_column(self._sort_column)
            else:
                self.populate_bills_table(self._filtered_bills)
            
            # Show success message
            message = f"Applied {applied_count} changes successfully!"
            if new_bills_created > 0:
                message += f" Created {new_bills_created} new bill(s) for next cycle."
            show_popup(self, "Success", message, color="green")
            
        except Exception as e:
            show_popup(self, "Error", f"Failed to apply changes: {str(e)}", color="red")
    
    def refresh_bills_data(self):
        """Refresh bills data from database"""
        # Check if there are pending changes
        if self.pending_changes:
            # Ask user if they want to discard pending changes
            try:
                confirm = ctk.CTkToplevel(self)
                confirm.title("Confirm Refresh")
                confirm.geometry("400x150")
                
                def safe_destroy():
                    try:
                        if confirm.winfo_exists():
                            confirm.destroy()
                    except:
                        pass
                
                ctk.CTkLabel(confirm, text=f"You have {len(self.pending_changes)} pending changes.\nDo you want to discard them and refresh?", 
                            font=("Arial", 12)).pack(pady=20)
                
                def do_refresh():
                    try:
                        self._bills_data = fetch_all_bills()
                        self._filtered_bills = self._bills_data.copy()
                        if self._sort_column:
                            self.sort_by_column(self._sort_column)
                        else:
                            self.populate_bills_table(self._filtered_bills)
                        # Clear pending changes
                        self.pending_changes.clear()
                        self.apply_btn.configure(text="Apply Changes", fg_color="green")
                        show_popup(self, "Success", "Data refreshed successfully!", color="green")
                    except Exception as e:
                        show_popup(self, "Error", f"Failed to refresh data: {str(e)}", color="red")
                    safe_destroy()
                
                def cancel_refresh():
                    safe_destroy()
                
                ctk.CTkButton(confirm, text="Discard & Refresh", fg_color="red", command=do_refresh).pack(side="left", padx=20, pady=10)
                ctk.CTkButton(confirm, text="Cancel", command=cancel_refresh).pack(side="right", padx=20, pady=10)
                
                # Use after() to delay the focus operations
                def set_focus():
                    try:
                        if confirm.winfo_exists():
                            confirm.lift()
                            confirm.focus_force()
                            confirm.grab_set()
                    except:
                        pass
                
                confirm.after(100, set_focus)
                
            except Exception as e:
                print(f"Confirm dialog error: {e}")
                # Fallback: refresh directly
                self._refresh_data_direct()
        else:
            # No pending changes, refresh directly
            self._refresh_data_direct()
    
    def _refresh_data_direct(self):
        """Helper method to refresh data directly"""
        try:
            self._bills_data = fetch_all_bills()
            self._filtered_bills = self._bills_data.copy()
            if self._sort_column:
                self.sort_by_column(self._sort_column)
            else:
                self.populate_bills_table(self._filtered_bills)
            show_popup(self, "Success", "Data refreshed successfully!", color="green")
        except Exception as e:
            show_popup(self, "Error", f"Failed to refresh data: {str(e)}", color="red")

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop() 