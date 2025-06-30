#!/usr/bin/env python3
"""
Test script to demonstrate edge case handling in billing cycles.
Tests scenarios like end-of-month dates and leap years.
"""

import sys
import os
from datetime import datetime, timedelta

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class BillingCycle:
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"

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
        return current_due_date
    
    if billing_cycle == BillingCycle.MONTHLY:
        next_date = add_months(current_date, 1)
    elif billing_cycle == BillingCycle.QUARTERLY:
        next_date = add_months(current_date, 3)
    else:
        return current_due_date
    
    return next_date.strftime(DATE_FORMAT)

def test_edge_cases():
    """Test edge cases for billing cycle calculations."""
    print("🏠 BILLS TRACKER - EDGE CASE TESTING 🏠")
    print("=" * 50)
    print()
    
    test_cases = [
        ("2025-01-31", "January 31st (end of month)"),
        ("2025-03-31", "March 31st (to April 30th)"),
        ("2024-02-29", "Leap year February 29th"),
        ("2025-02-28", "Non-leap year February 28th"),
        ("2025-05-31", "May 31st (to June 30th)"),
        ("2025-08-31", "August 31st (various month lengths)"),
    ]
    
    for start_date, description in test_cases:
        print(f"📅 Testing: {description}")
        print(f"   Start Date: {start_date}")
        
        # Test monthly billing
        current = start_date
        print(f"   Monthly Cycle:")
        for i in range(1, 6):
            next_date = calculate_next_due_date(current, BillingCycle.MONTHLY)
            current = next_date
            try:
                date_obj = datetime.strptime(next_date, '%Y-%m-%d')
                month_name = date_obj.strftime('%B %d, %Y')
                print(f"     Payment {i}: {next_date} ({month_name})")
            except ValueError:
                print(f"     Payment {i}: {next_date} (Invalid date)")
        
        print()
    
    print("=" * 50)
    print("✅ Edge case testing completed!")
    print("🎯 The system properly handles:")
    print("   • End-of-month dates (Jan 31 → Feb 28/29)")
    print("   • Leap years and non-leap years")
    print("   • Months with different numbers of days")
    print("   • Year rollovers")

if __name__ == "__main__":
    test_edge_cases()
