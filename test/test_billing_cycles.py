#!/usr/bin/env python3
"""
Test script to demonstrate flexible billing cycles feature in Bills Tracker.
This script shows how the billing cycle functionality works without interactive input.
"""

import sys
import os
from datetime import datetime, timedelta

# Add the parent directory to the path to import from bills-tracker.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the billing cycle functions from the main application
# Note: We'll copy the relevant classes and functions here for demonstration

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

def add_months(date, months):
    """Add months to a date, handling month/year rollover properly."""
    month = date.month - 1 + months
    year = date.year + month // 12
    month = month % 12 + 1
    
    # Handle day overflow (e.g., Jan 31 + 1 month should be Feb 28/29)
    day = date.day
    import calendar
    max_day = calendar.monthrange(year, month)[1]
    if day > max_day:
        day = max_day
    
    return date.replace(year=year, month=month, day=day)

def calculate_next_due_date(current_due_date, billing_cycle):
    """Calculate the next due date based on billing cycle."""
    DATE_FORMAT = '%Y-%m-%d'
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

def demonstrate_billing_cycles():
    """Demonstrate how different billing cycles work."""
    print("🏠 BILLS TRACKER - FLEXIBLE BILLING CYCLES DEMO 🏠")
    print("=" * 60)
    print()
    
    # Start date for demonstration
    start_date = "2025-01-15"  # January 15, 2025
    print(f"Starting Date: {start_date}")
    print()
    
    # Demonstrate each billing cycle
    cycles = BillingCycle.get_all_cycles()
    
    for cycle in cycles:
        print(f"📅 {cycle.upper()} BILLING CYCLE")
        print(f"   Description: {BillingCycle.get_cycle_description(cycle)}")
        
        current_date = start_date
        print(f"   Payment 1: {current_date}")
        
        # Show next 5 payment dates for this cycle
        for i in range(2, 7):
            if cycle == BillingCycle.ONE_TIME:
                print(f"   Payment {i}: No further payments (One-time only)")
                break
            else:
                next_date = calculate_next_due_date(current_date, cycle)
                current_date = next_date
                print(f"   Payment {i}: {current_date}")
        
        print()
    
    print("=" * 60)
    print("✅ Demo completed! The Bills Tracker supports all these billing cycles.")
    print("📝 When adding a bill, you can choose any of these cycles.")
    print("💰 When paying a bill, the next due date is automatically calculated.")
    print("🔄 Recurring bills will reset to 'unpaid' with the new due date.")
    print("🎯 One-time bills stay marked as 'paid' and don't recur.")

if __name__ == "__main__":
    demonstrate_billing_cycles()
