#!/usr/bin/env python3
"""
Comprehensive demonstration of the flexible billing cycles feature.
This script showcases all the advanced billing cycle functionality.
"""

import json
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

class BillingCycle:
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

def colored_print(text, color=Colors.RESET):
    print(f"{color}{text}{Colors.RESET}")

def demo_header():
    """Print the demo header."""
    print("=" * 80)
    colored_print("🏠 BILLS TRACKER - FLEXIBLE BILLING CYCLES FEATURE DEMO 🏠", Colors.TITLE + Style.BRIGHT)
    print("=" * 80)
    print()

def demo_billing_cycles_overview():
    """Show overview of all supported billing cycles."""
    colored_print("📅 SUPPORTED BILLING CYCLES", Colors.MENU)
    print("-" * 40)
    
    descriptions = {
        BillingCycle.WEEKLY: "Every 7 days - Perfect for weekly services",
        BillingCycle.BI_WEEKLY: "Every 14 days - Great for bi-weekly payments",
        BillingCycle.MONTHLY: "Every month - Most common billing cycle",
        BillingCycle.QUARTERLY: "Every 3 months - Seasonal services",
        BillingCycle.SEMI_ANNUALLY: "Every 6 months - Insurance, some subscriptions",
        BillingCycle.ANNUALLY: "Every 12 months - Annual memberships",
        BillingCycle.ONE_TIME: "One-time payment - No recurrence"
    }
    
    for cycle in BillingCycle.get_all_cycles():
        colored_print(f"• {cycle.upper():<15} - {descriptions[cycle]}", Colors.INFO)
    
    print()

def demo_real_world_examples():
    """Show real-world examples of different billing cycles."""
    colored_print("🌍 REAL-WORLD EXAMPLES", Colors.MENU)
    print("-" * 40)
    
    examples = [
        ("Netflix Subscription", BillingCycle.MONTHLY, "2025-01-15", "$15.99"),
        ("Gym Membership", BillingCycle.MONTHLY, "2025-01-01", "$45.00"),
        ("Car Insurance", BillingCycle.SEMI_ANNUALLY, "2025-01-01", "$350.00"),
        ("Domain Registration", BillingCycle.ANNUALLY, "2025-03-15", "$12.99"),
        ("Weekly Cleaning Service", BillingCycle.WEEKLY, "2025-01-06", "$80.00"),
        ("Newspaper Delivery", BillingCycle.BI_WEEKLY, "2025-01-01", "$25.00"),
        ("Quarterly Tax Payment", BillingCycle.QUARTERLY, "2025-01-15", "$1,200.00"),
        ("One-time Software License", BillingCycle.ONE_TIME, "2025-01-15", "$299.00"),
    ]
    
    for name, cycle, due_date, amount in examples:
        colored_print(f"📋 {name}", Colors.TITLE)
        print(f"   💰 Amount: {amount}")
        print(f"   📅 Due Date: {due_date}")
        print(f"   🔄 Billing Cycle: {cycle.upper()}")
        
        # Calculate next few payment dates
        print(f"   📆 Next Payment Dates:")
        current_date = due_date
        for i in range(1, 4):
            if cycle == BillingCycle.ONE_TIME:
                if i == 1:
                    print(f"      {i}. One-time payment only")
                break
            else:
                next_date = calculate_next_due_date_demo(current_date, cycle)
                current_date = next_date
                print(f"      {i}. {next_date}")
        print()

def calculate_next_due_date_demo(current_due_date, billing_cycle):
    """Demo version of date calculation."""
    try:
        current_date = datetime.strptime(current_due_date, '%Y-%m-%d')
    except ValueError:
        return current_due_date
    
    if billing_cycle == BillingCycle.WEEKLY:
        next_date = current_date + timedelta(days=7)
    elif billing_cycle == BillingCycle.BI_WEEKLY:
        next_date = current_date + timedelta(days=14)
    elif billing_cycle == BillingCycle.MONTHLY:
        next_date = add_months_demo(current_date, 1)
    elif billing_cycle == BillingCycle.QUARTERLY:
        next_date = add_months_demo(current_date, 3)
    elif billing_cycle == BillingCycle.SEMI_ANNUALLY:
        next_date = add_months_demo(current_date, 6)
    elif billing_cycle == BillingCycle.ANNUALLY:
        next_date = add_months_demo(current_date, 12)
    else:
        return current_due_date
    
    return next_date.strftime('%Y-%m-%d')

def add_months_demo(date, months):
    """Demo version of add_months with proper month handling."""
    month = date.month - 1 + months
    year = date.year + month // 12
    month = month % 12 + 1
    
    day = date.day
    import calendar
    max_day = calendar.monthrange(year, month)[1]
    if day > max_day:
        day = max_day
    
    return date.replace(year=year, month=month, day=day)

def demo_bill_payment_simulation():
    """Simulate paying a bill and advancing the due date."""
    colored_print("💰 BILL PAYMENT SIMULATION", Colors.MENU)
    print("-" * 40)
    
    # Simulate a monthly Netflix bill
    bill = {
        "name": "Netflix Subscription",
        "due_date": "2025-01-15",
        "billing_cycle": BillingCycle.MONTHLY,
        "amount": "$15.99",
        "paid": False
    }
    
    colored_print("📋 Original Bill:", Colors.TITLE)
    print(f"   Name: {bill['name']}")
    print(f"   Due Date: {bill['due_date']}")
    print(f"   Billing Cycle: {bill['billing_cycle'].upper()}")
    print(f"   Amount: {bill['amount']}")
    print(f"   Status: {'PAID' if bill['paid'] else 'UNPAID'}")
    print()
    
    colored_print("💳 Paying bill...", Colors.WARNING)
    
    # Simulate payment
    bill['paid'] = True
    old_due_date = bill['due_date']
    
    # Calculate next due date
    if bill['billing_cycle'] != BillingCycle.ONE_TIME:
        new_due_date = calculate_next_due_date_demo(bill['due_date'], bill['billing_cycle'])
        bill['due_date'] = new_due_date
        bill['paid'] = False  # Reset for recurring bills
        
        colored_print("✅ Payment successful!", Colors.SUCCESS)
        print(f"   Previous due date: {old_due_date}")
        print(f"   Next due date: {new_due_date}")
        print(f"   Status: UNPAID (reset for next billing cycle)")
    else:
        colored_print("✅ One-time payment completed!", Colors.SUCCESS)
        print(f"   Status: PAID (no further payments needed)")
    
    print()

def demo_feature_highlights():
    """Highlight key features of the billing cycles system."""
    colored_print("🌟 KEY FEATURES", Colors.MENU)
    print("-" * 40)
    
    features = [
        "✅ Seven different billing cycles supported",
        "✅ Smart date calculations handle month-end edge cases",
        "✅ Automatic due date advancement when paying bills",
        "✅ One-time bills don't recur after payment",
        "✅ Recurring bills reset to 'unpaid' with new due date",
        "✅ Proper handling of leap years and month variations",
        "✅ Color-coded display for different billing cycles",
        "✅ Calendar view shows upcoming bills",
        "✅ Search and sort work with billing cycle information",
        "✅ Integration with all existing Bills Tracker features"
    ]
    
    for feature in features:
        colored_print(feature, Colors.SUCCESS)
    
    print()

def demo_how_to_use():
    """Show users how to use the billing cycles feature."""
    colored_print("📖 HOW TO USE", Colors.MENU)
    print("-" * 40)
    
    steps = [
        "1. Run the Bills Tracker: python bills-tracker.py",
        "2. Choose 'Add a bill' from the main menu",
        "3. Enter bill details (name, due date, website, login)",
        "4. Select from 7 billing cycle options when prompted",
        "5. Bill is saved with your chosen billing cycle",
        "6. When you pay the bill, due date automatically advances",
        "7. View bills to see billing cycle information",
        "8. Use the calendar view to see upcoming payment dates"
    ]
    
    for step in steps:
        print(f"   {step}")
    
    print()

def main():
    """Run the complete demonstration."""
    demo_header()
    
    demo_billing_cycles_overview()
    input("Press Enter to continue to real-world examples...")
    print()
    
    demo_real_world_examples()
    input("Press Enter to continue to payment simulation...")
    print()
    
    demo_bill_payment_simulation()
    input("Press Enter to continue to feature highlights...")
    print()
    
    demo_feature_highlights()
    input("Press Enter to continue to usage instructions...")
    print()
    
    demo_how_to_use()
    
    print("=" * 80)
    colored_print("🎉 DEMO COMPLETED! 🎉", Colors.SUCCESS + Style.BRIGHT)
    colored_print("The flexible billing cycles feature is fully implemented and ready to use!", Colors.INFO)
    print("=" * 80)

if __name__ == "__main__":
    main()
