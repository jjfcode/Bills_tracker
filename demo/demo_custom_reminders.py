#!/usr/bin/env python3
"""
Test script to demonstrate the Custom Reminder Periods feature.
This script shows how different bills can have different reminder periods.
"""

import json
import os
from datetime import datetime, timedelta
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class Colors:
    SUCCESS = Fore.GREEN
    ERROR = Fore.RED
    WARNING = Fore.YELLOW
    INFO = Fore.CYAN
    TITLE = Fore.MAGENTA
    MENU = Fore.BLUE + Style.BRIGHT
    RESET = Style.RESET_ALL

def colored_print(text, color=Colors.RESET):
    print(f"{color}{text}{Colors.RESET}")

def demo_custom_reminder_periods():
    """Demonstrate custom reminder periods feature."""
    print("=" * 80)
    colored_print("🏠 BILLS TRACKER - CUSTOM REMINDER PERIODS DEMO 🏠", Colors.TITLE + Style.BRIGHT)
    print("=" * 80)
    print()
    
    # Create sample bills with different reminder periods
    sample_bills = [
        {
            "name": "Credit Card Payment",
            "due_date": "2025-07-03",  # 4 days from now
            "billing_cycle": "monthly",
            "reminder_days": 7,
            "paid": False,
            "web_page": "https://mybank.com",
            "login_info": "user@email.com"
        },
        {
            "name": "Rent Payment",
            "due_date": "2025-07-01",  # 2 days from now
            "billing_cycle": "monthly", 
            "reminder_days": 3,
            "paid": False,
            "web_page": "https://propertymanagement.com",
            "login_info": "tenant123"
        },
        {
            "name": "Electricity Bill",
            "due_date": "2025-06-30",  # Due today
            "billing_cycle": "monthly",
            "reminder_days": 5,
            "paid": False,
            "web_page": "https://electriccompany.com",
            "login_info": "account456"
        },
        {
            "name": "Car Insurance Premium",
            "due_date": "2025-07-15",  # 16 days from now
            "billing_cycle": "semi-annually",
            "reminder_days": 14,
            "paid": False,
            "web_page": "https://autoinsurance.com",
            "login_info": "policy789"
        },
        {
            "name": "Gym Membership",
            "due_date": "2025-06-28",  # 1 day overdue
            "billing_cycle": "monthly",
            "reminder_days": 1,
            "paid": False,
            "web_page": "https://fitnessgym.com",
            "login_info": "member001"
        },
        {
            "name": "Phone Bill",
            "due_date": "2025-07-05",  # 6 days from now
            "billing_cycle": "monthly",
            "reminder_days": 10,
            "paid": False,
            "web_page": "https://phonecompany.com",
            "login_info": "line555"
        }
    ]
    
    colored_print("📋 SAMPLE BILLS WITH CUSTOM REMINDER PERIODS", Colors.MENU)
    print("-" * 60)
    
    today = datetime.now()
    
    for idx, bill in enumerate(sample_bills, 1):
        try:
            due_date = datetime.strptime(bill['due_date'], '%Y-%m-%d')
            days_diff = (due_date - today).days
            reminder_days = bill['reminder_days']
            
            # Determine status
            if days_diff < 0:
                status_color = Colors.ERROR
                status_text = f"OVERDUE by {abs(days_diff)} days"
            elif days_diff == 0:
                status_color = Colors.WARNING
                status_text = "DUE TODAY"
            elif days_diff <= reminder_days:
                status_color = Colors.WARNING
                status_text = f"DUE in {days_diff} days (within reminder period)"
            else:
                status_color = Colors.INFO
                status_text = f"Due in {days_diff} days"
            
            colored_print(f"{idx}. {bill['name']}", Colors.TITLE)
            print(f"   Due Date: {bill['due_date']}")
            print(f"   Billing Cycle: {bill['billing_cycle'].title()}")
            colored_print(f"   Reminder Period: ⏰ {reminder_days} days before due date", Colors.INFO)
            colored_print(f"   Status: {status_text}", status_color)
            print()
            
        except ValueError:
            colored_print(f"{idx}. {bill['name']} - Invalid date format", Colors.ERROR)
            print()
    
    print("-" * 60)
    colored_print("🎯 BILLS THAT SHOULD TRIGGER REMINDERS TODAY", Colors.MENU)
    print("-" * 60)
    
    reminder_bills = []
    for bill in sample_bills:
        try:
            due_date = datetime.strptime(bill['due_date'], '%Y-%m-%d')
            days_diff = (due_date - today).days
            reminder_days = bill['reminder_days']
            
            if days_diff <= reminder_days:
                reminder_bills.append((bill, days_diff, reminder_days))
        except ValueError:
            continue
    
    if not reminder_bills:
        colored_print("No bills need reminders today! 🎉", Colors.SUCCESS)
    else:
        # Sort by urgency
        reminder_bills.sort(key=lambda x: x[1])
        
        for bill, days_diff, reminder_days in reminder_bills:
            if days_diff < 0:
                colored_print(f"🚨 {bill['name']} - OVERDUE by {abs(days_diff)} days!", Colors.ERROR)
            elif days_diff == 0:
                colored_print(f"🔥 {bill['name']} - DUE TODAY!", Colors.WARNING)
            else:
                colored_print(f"⚠️  {bill['name']} - Due in {days_diff} days", Colors.WARNING)
            
            colored_print(f"   ⏰ Reminder was set for {reminder_days} days before due date", Colors.INFO)
            print()
    
    print("-" * 60)
    colored_print("💡 HOW CUSTOM REMINDER PERIODS WORK", Colors.MENU)
    print("-" * 60)
    
    explanations = [
        "✅ Each bill can have its own reminder period (1-365 days)",
        "✅ High-priority bills (rent, utilities) can have shorter reminder periods",
        "✅ Less urgent bills (annual memberships) can have longer reminder periods",
        "✅ The system checks if today falls within each bill's reminder window",
        "✅ Bills show up in 'due bills' based on their individual reminder settings",
        "✅ You can still check bills due within a specific number of days",
        "✅ Default reminder period is 7 days for bills created before this feature",
        "✅ Reminder periods can be edited anytime for existing bills"
    ]
    
    for explanation in explanations:
        colored_print(explanation, Colors.SUCCESS)
    
    print()
    print("-" * 60)
    colored_print("🎮 FEATURE USAGE EXAMPLES", Colors.MENU)
    print("-" * 60)
    
    examples = [
        ("Rent Payment", "Set to 3 days - You want early warning for critical payments"),
        ("Credit Card", "Set to 7 days - Standard reminder for monthly bills"),
        ("Car Insurance", "Set to 14 days - Longer notice for expensive semi-annual bills"),
        ("Gym Membership", "Set to 1 day - Just a quick reminder the day before"),
        ("Annual Subscriptions", "Set to 30 days - Month-long notice for yearly renewals"),
        ("Utility Bills", "Set to 5 days - Reasonable time to arrange payment")
    ]
    
    for bill_type, explanation in examples:
        colored_print(f"📋 {bill_type}", Colors.TITLE)
        colored_print(f"   {explanation}", Colors.INFO)
        print()
    
    print("=" * 80)
    colored_print("🎉 CUSTOM REMINDER PERIODS DEMO COMPLETED! 🎉", Colors.SUCCESS + Style.BRIGHT)
    colored_print("This feature gives you complete control over when you're reminded about each bill.", Colors.INFO)
    print("=" * 80)

if __name__ == "__main__":
    demo_custom_reminder_periods()
