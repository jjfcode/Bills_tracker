#!/usr/bin/env python3
"""
Demo script for the improved date selector functionality
Shows all the new date selection features implemented in Bills Tracker v3
"""

import customtkinter as ctk
from datetime import datetime, timedelta
from tkinter import StringVar
import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), "src", "gui"))
from main_window import DateSelectorFrame

class DateSelectorDemo(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Date Selector Demo - Bills Tracker v3")
        self.geometry("600x500")
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(self, text="📅 Improved Date Selector Demo", 
                                  font=ctk.CTkFont(size=20, weight="bold"))
        title_label.grid(row=0, column=0, pady=20)
        
        # Description
        desc_label = ctk.CTkLabel(self, text="This demo shows the new date selection features:\n" +
                                 "• Calendar picker with visual interface\n" +
                                 "• Fallback date picker if calendar is not available\n" +
                                 "• Direct date input in YYYY-MM-DD format",
                                 font=ctk.CTkFont(size=14))
        desc_label.grid(row=1, column=0, pady=10)
        
        # Date selector frame
        self.date_selector = DateSelectorFrame(self)
        self.date_selector.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        
        # Current date display
        self.current_date_var = StringVar()
        self.current_date_var.set(f"Current Date: {datetime.now().strftime('%Y-%m-%d')}")
        current_date_label = ctk.CTkLabel(self, textvariable=self.current_date_var,
                                        font=ctk.CTkFont(size=12))
        current_date_label.grid(row=3, column=0, pady=10)
        
        # Selected date display
        self.selected_date_var = StringVar()
        self.selected_date_var.set("Selected Date: None")
        selected_date_label = ctk.CTkLabel(self, textvariable=self.selected_date_var,
                                         font=ctk.CTkFont(size=14, weight="bold"))
        selected_date_label.grid(row=4, column=0, pady=10)
        
        # Update selected date when it changes
        self.date_selector.selected_date.trace('w', self._on_date_change)
        
        # Instructions
        instructions = ctk.CTkTextbox(self, height=100)
        instructions.grid(row=5, column=0, padx=20, pady=10, sticky="ew")
        instructions.insert("1.0", """Instructions:
1. Click the 📅 button to open a calendar picker
2. Type directly in the date field (YYYY-MM-DD format)
3. Watch the selected date update in real-time

The date selector provides:
• Visual calendar interface
• Fallback date picker if calendar unavailable
• Direct text input with validation""")
        instructions.configure(state="disabled")
    
    def _on_date_change(self, *args):
        """Update the selected date display"""
        selected = self.date_selector.get_date()
        if selected:
            self.selected_date_var.set(f"Selected Date: {selected}")
        else:
            self.selected_date_var.set("Selected Date: None")

def main():
    """Run the date selector demo"""
    print("🚀 Starting Date Selector Demo...")
    print("This demo shows the improved date selection features in Bills Tracker v3")
    print("Features demonstrated:")
    print("• Visual calendar picker")
    print("• Direct date input")
    print("• Fallback date picker")
    print()
    
    app = DateSelectorDemo()
    app.mainloop()

if __name__ == "__main__":
    main() 