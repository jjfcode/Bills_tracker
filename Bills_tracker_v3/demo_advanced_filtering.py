#!/usr/bin/env python3
"""
Demo script for the advanced filtering functionality
Shows the new filtering features implemented in Bills Tracker v3.1
"""

import customtkinter as ctk
from datetime import datetime, timedelta
import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), "src", "core"))
from db import fetch_all_bills

class AdvancedFilteringDemo(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Advanced Filtering Demo - Bills Tracker v3.1")
        self.geometry("800x600")
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(self, text="🔍 Advanced Filtering Demo", 
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.grid(row=0, column=0, pady=20)
        
        # Description
        desc_label = ctk.CTkLabel(self, text="This demo shows the new filtering features:\n" +
                                 "• Default view shows only PENDING bills\n" +
                                 "• Status filter: Pending, Paid, All\n" +
                                 "• Period filter: This Month, Last Month, Previous Month, This Year, Last Year\n" +
                                 "• Combined filtering with search\n" +
                                 "• Real-time bill counter",
                                 font=ctk.CTkFont(size=14))
        desc_label.grid(row=1, column=0, pady=10)
        
        # Demo content frame
        demo_frame = ctk.CTkFrame(self)
        demo_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        demo_frame.grid_columnconfigure(0, weight=1)
        demo_frame.grid_rowconfigure(1, weight=1)
        
        # Filter controls
        filter_controls = ctk.CTkFrame(demo_frame)
        filter_controls.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        filter_controls.grid_columnconfigure(1, weight=1)
        
        # Status filter
        ctk.CTkLabel(filter_controls, text="Status Filter:").grid(row=0, column=0, padx=(10, 5), pady=10)
        self.status_var = ctk.StringVar(value="Pending")
        status_combo = ctk.CTkOptionMenu(filter_controls, variable=self.status_var,
                                        values=["Pending", "Paid", "All"],
                                        command=self.update_demo)
        status_combo.grid(row=0, column=1, padx=5, pady=10, sticky="w")
        
        # Period filter
        ctk.CTkLabel(filter_controls, text="Period Filter:").grid(row=0, column=2, padx=(20, 5), pady=10)
        self.period_var = ctk.StringVar(value="All")
        period_combo = ctk.CTkOptionMenu(filter_controls, variable=self.period_var,
                                        values=["All", "This Month", "Last Month", "Previous Month", "This Year", "Last Year"],
                                        command=self.update_demo)
        period_combo.grid(row=0, column=3, padx=5, pady=10)
        
        # Clear filters button
        clear_btn = ctk.CTkButton(filter_controls, text="Reset to Default", 
                                 command=self.reset_filters, width=120)
        clear_btn.grid(row=0, column=4, padx=10, pady=10)
        
        # Results display
        results_frame = ctk.CTkFrame(demo_frame)
        results_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_rowconfigure(0, weight=1)
        
        # Results text
        self.results_text = ctk.CTkTextbox(results_frame, height=300)
        self.results_text.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Counter label
        self.counter_label = ctk.CTkLabel(demo_frame, text="", font=ctk.CTkFont(size=12))
        self.counter_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        
        # Instructions
        instructions = ctk.CTkTextbox(demo_frame, height=100)
        instructions.grid(row=3, column=0, sticky="ew", padx=10, pady=10)
        instructions.insert("1.0", """Instructions:
1. Change Status Filter to see different bill statuses (Pending/Paid/All)
2. Change Period Filter to see bills from different time periods
3. Click "Reset to Default" to return to Pending bills only
4. Watch the counter update in real-time
5. In the main app, you can also use search filters with these options

Key Features:
• Default view shows only PENDING bills (most useful for daily use)
• Period filters help with monthly/yearly reviews
• Combined filtering allows precise bill management
• Real-time counter shows exactly what you're viewing""")
        instructions.configure(state="disabled")
        
        # Load sample data and update display
        self.load_sample_data()
        self.update_demo()
    
    def load_sample_data(self):
        """Load sample bills data for demonstration"""
        try:
            self.sample_bills = fetch_all_bills()
        except:
            # Fallback sample data if database not available
            today = datetime.now()
            self.sample_bills = [
                {"name": "Electricity Bill", "due_date": today.strftime("%Y-%m-%d"), "paid": False, "category_name": "Utilities"},
                {"name": "Internet Bill", "due_date": (today + timedelta(days=5)).strftime("%Y-%m-%d"), "paid": False, "category_name": "Utilities"},
                {"name": "Netflix Subscription", "due_date": (today - timedelta(days=10)).strftime("%Y-%m-%d"), "paid": True, "category_name": "Subscriptions"},
                {"name": "Car Insurance", "due_date": (today + timedelta(days=15)).strftime("%Y-%m-%d"), "paid": False, "category_name": "Insurance"},
                {"name": "Phone Bill", "due_date": (today - timedelta(days=20)).strftime("%Y-%m-%d"), "paid": True, "category_name": "Utilities"},
                {"name": "Gym Membership", "due_date": (today + timedelta(days=3)).strftime("%Y-%m-%d"), "paid": False, "category_name": "Subscriptions"},
                {"name": "Home Insurance", "due_date": (today - timedelta(days=30)).strftime("%Y-%m-%d"), "paid": True, "category_name": "Insurance"},
                {"name": "Credit Card", "due_date": (today + timedelta(days=7)).strftime("%Y-%m-%d"), "paid": False, "category_name": "Credit Cards"},
            ]
    
    def filter_by_status(self, bills, status):
        """Filter bills by status"""
        if status == "Pending":
            return [bill for bill in bills if not bill.get("paid", False)]
        elif status == "Paid":
            return [bill for bill in bills if bill.get("paid", False)]
        else:  # All
            return bills
    
    def filter_by_period(self, bills, period):
        """Filter bills by time period"""
        today = datetime.now()
        filtered_bills = []
        
        for bill in bills:
            try:
                due_date = datetime.strptime(bill.get("due_date", ""), "%Y-%m-%d")
                
                if period == "This Month":
                    if due_date.year == today.year and due_date.month == today.month:
                        filtered_bills.append(bill)
                        
                elif period == "Last Month":
                    last_month = today.replace(day=1) - timedelta(days=1)
                    if due_date.year == last_month.year and due_date.month == last_month.month:
                        filtered_bills.append(bill)
                        
                elif period == "Previous Month":
                    # Two months ago
                    prev_month = today.replace(day=1) - timedelta(days=1)
                    prev_month = prev_month.replace(day=1) - timedelta(days=1)
                    if due_date.year == prev_month.year and due_date.month == prev_month.month:
                        filtered_bills.append(bill)
                        
                elif period == "This Year":
                    if due_date.year == today.year:
                        filtered_bills.append(bill)
                        
                elif period == "Last Year":
                    if due_date.year == today.year - 1:
                        filtered_bills.append(bill)
                        
            except ValueError:
                continue
        
        return filtered_bills
    
    def update_demo(self, *args):
        """Update the demo display based on current filters"""
        # Apply filters
        filtered_bills = self.sample_bills.copy()
        
        # Status filter
        status_filter = self.status_var.get()
        filtered_bills = self.filter_by_status(filtered_bills, status_filter)
        
        # Period filter
        period_filter = self.period_var.get()
        if period_filter != "All":
            filtered_bills = self.filter_by_period(filtered_bills, period_filter)
        
        # Update results display
        self.results_text.delete("1.0", "end")
        
        if not filtered_bills:
            self.results_text.insert("1.0", "No bills match the current filters.\n\nTry changing the Status or Period filters.")
        else:
            # Sort by due date
            filtered_bills.sort(key=lambda x: x.get("due_date", ""))
            
            for bill in filtered_bills:
                status = "✓ PAID" if bill.get("paid", False) else "☐ PENDING"
                due_date = bill.get("due_date", "")
                name = bill.get("name", "")
                category = bill.get("category_name", "Uncategorized")
                
                line = f"{status} | {due_date} | {name} | {category}\n"
                self.results_text.insert("end", line)
        
        # Update counter
        total_bills = len(self.sample_bills)
        filtered_count = len(filtered_bills)
        
        counter_text = f"Showing {filtered_count} of {total_bills} bills"
        if status_filter != "All":
            counter_text += f" | Status: {status_filter}"
        if period_filter != "All":
            counter_text += f" | Period: {period_filter}"
        
        self.counter_label.configure(text=counter_text)
    
    def reset_filters(self):
        """Reset filters to default (Pending bills only)"""
        self.status_var.set("Pending")
        self.period_var.set("All")
        self.update_demo()

def main():
    """Run the advanced filtering demo"""
    print("🚀 Starting Advanced Filtering Demo...")
    print("This demo shows the new filtering features in Bills Tracker v3.1")
    print("Features demonstrated:")
    print("• Default Pending bills view")
    print("• Status filtering (Pending/Paid/All)")
    print("• Period filtering (This Month, Last Month, etc.)")
    print("• Combined filtering")
    print("• Real-time bill counter")
    print()
    
    app = AdvancedFilteringDemo()
    app.mainloop()

if __name__ == "__main__":
    main() 