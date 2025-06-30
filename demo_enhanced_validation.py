#!/usr/bin/env python3
"""
Enhanced Validation Demonstration for Bills Tracker

This script demonstrates the new validation features implemented in Bills Tracker v3.1:
- URL validation and auto-correction
- Email format validation 
- Date range validation (prevents dates too far in past/future)
- Reminder days validation (1-365 range)
- Interactive error handling with helpful messages

Run this script to see examples of the validation in action.
"""

from datetime import datetime, timedelta
import re
import urllib.parse

def demonstrate_url_validation():
    """Demonstrate URL validation with examples."""
    print("🌐 URL Validation Examples")
    print("=" * 50)
    
    test_cases = [
        ("google.com", "Simple domain"),
        ("www.example.org/path", "Domain with path"),
        ("ftp://files.com", "FTP protocol (converted to HTTPS)"),
        ("invalid url", "Invalid format"),
        ("", "Empty URL (allowed)"),
        ("sub.domain.co.uk", "UK domain"),
    ]
    
    def validate_url(url):
        if not url.strip():
            return ""
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        try:
            parsed = urllib.parse.urlparse(url)
            if not parsed.netloc:
                return None
            domain_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
            if not re.match(domain_pattern, parsed.netloc.split(':')[0]):
                return None
            return url
        except Exception:
            return None
    
    for input_url, description in test_cases:
        result = validate_url(input_url)
        if result is None:
            status = "❌ INVALID"
            output = "Rejected - Invalid format"
        elif result == "":
            status = "✅ VALID"
            output = "Empty URL allowed"
        elif result != input_url:
            status = "✅ CORRECTED"
            output = f"Auto-corrected to: {result}"
        else:
            status = "✅ VALID"
            output = "Accepted as-is"
        
        print(f"{status:<12} '{input_url}' ({description})")
        print(f"             → {output}")
        print()

def demonstrate_email_validation():
    """Demonstrate email validation with examples."""
    print("📧 Email Validation Examples")
    print("=" * 50)
    
    test_cases = [
        ("user@example.com", "Standard email"),
        ("test.email@domain.org", "Email with dots"),
        ("user.name+tag@company.co.uk", "Email with plus and UK domain"),
        ("invalid-email", "Missing @ symbol"),
        ("user@", "Missing domain"),
        ("@domain.com", "Missing username"),
        ("spaces in@email.com", "Spaces not allowed"),
        ("", "Empty email (allowed)"),
    ]
    
    def validate_email(email):
        if not email.strip():
            return ""
        email = email.strip().lower()
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_pattern, email):
            return email
        return None
    
    for input_email, description in test_cases:
        result = validate_email(input_email)
        if result is None:
            status = "❌ INVALID"
            output = "Rejected - Invalid format"
        elif result == "":
            status = "✅ VALID"
            output = "Empty email allowed"
        else:
            status = "✅ VALID"
            output = f"Accepted: {result}"
        
        print(f"{status:<12} '{input_email}' ({description})")
        print(f"             → {output}")
        print()

def demonstrate_date_validation():
    """Demonstrate date range validation with examples."""
    print("📅 Date Range Validation Examples")
    print("=" * 50)
    
    today = datetime.now()
    test_cases = [
        ((today + timedelta(days=1)).strftime('%Y-%m-%d'), "Tomorrow"),
        ((today + timedelta(days=30)).strftime('%Y-%m-%d'), "Next month"),
        ((today - timedelta(days=30)).strftime('%Y-%m-%d'), "Last month (OK)"),
        ((today - timedelta(days=400)).strftime('%Y-%m-%d'), "Over 1 year ago"),
        ((today + timedelta(days=2000)).strftime('%Y-%m-%d'), "Over 5 years future"),
        ("2024-02-30", "Invalid date (Feb 30)"),
        ("invalid-date", "Invalid format"),
    ]
    
    def validate_future_date(date_str):
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            today = datetime.now()
            one_year_ago = today - timedelta(days=365)
            five_years_future = today + timedelta(days=5*365)
            
            if date_obj < one_year_ago:
                return False, "Date is more than 1 year in the past"
            if date_obj > five_years_future:
                return False, "Date is more than 5 years in the future"
            return True, None
        except ValueError:
            return False, "Invalid date format"
    
    for test_date, description in test_cases:
        try:
            datetime.strptime(test_date, '%Y-%m-%d')
            is_valid, error_msg = validate_future_date(test_date)
            if is_valid:
                status = "✅ VALID"
                output = "Date accepted"
            else:
                status = "❌ INVALID"
                output = error_msg
        except ValueError:
            status = "❌ INVALID"
            output = "Invalid date format"
        
        print(f"{status:<12} '{test_date}' ({description})")
        print(f"             → {output}")
        print()

def demonstrate_reminder_validation():
    """Demonstrate reminder days validation with examples."""
    print("⏰ Reminder Days Validation Examples")
    print("=" * 50)
    
    test_cases = [
        ("7", "Default reminder"),
        ("1", "Minimum (1 day)"),
        ("365", "Maximum (1 year)"),
        ("30", "Monthly reminder"),
        ("0", "Below minimum"),
        ("366", "Above maximum"),
        ("-5", "Negative number"),
        ("abc", "Non-numeric"),
        ("7.5", "Decimal not allowed"),
        ("", "Empty (uses default)"),
    ]
    
    def validate_reminder_days(days_str):
        try:
            days = int(days_str)
            return 1 <= days <= 365
        except ValueError:
            return False
    
    for input_days, description in test_cases:
        if input_days == "":
            status = "✅ VALID"
            output = "Uses default (7 days)"
        elif validate_reminder_days(input_days):
            status = "✅ VALID"
            output = f"Accepted: {input_days} days"
        else:
            status = "❌ INVALID"
            output = "Must be 1-365 days"
        
        print(f"{status:<12} '{input_days}' ({description})")
        print(f"             → {output}")
        print()

def show_interactive_benefits():
    """Show benefits of interactive validation."""
    print("🎮 Interactive Validation Benefits")
    print("=" * 50)
    
    benefits = [
        "✅ URL Auto-Correction: 'google.com' → 'https://google.com'",
        "✅ Helpful Error Messages: Clear explanations for invalid input",
        "✅ Cancel Option: Type 'cancel' at any time to abort operations",
        "✅ Default Values: Press Enter for sensible defaults (e.g., 7 days)",
        "✅ Range Validation: Prevents unrealistic dates and values",
        "✅ Format Validation: Ensures proper email and URL formats",
        "✅ User-Friendly: Prompts for re-entry instead of crashing",
        "✅ Visual Feedback: Color-coded success/error messages",
        "✅ Flexible Input: Accepts various formats and corrects them",
        "✅ Data Integrity: Ensures all stored data meets quality standards"
    ]
    
    for benefit in benefits:
        print(f"   {benefit}")
    print()

def main():
    """Run all validation demonstrations."""
    print("🧪 Bills Tracker - Enhanced Validation Demonstration")
    print("=" * 60)
    print("Showcasing the new validation features in Bills Tracker v3.1\n")
    
    demonstrate_url_validation()
    demonstrate_email_validation()
    demonstrate_date_validation()
    demonstrate_reminder_validation()
    show_interactive_benefits()
    
    print("🎉 Enhanced Validation Features Complete!")
    print("=" * 60)
    print("Benefits for Bills Tracker users:")
    print("   • Better data quality with automatic validation")
    print("   • User-friendly error handling and correction")
    print("   • Prevents common input mistakes and typos")
    print("   • Maintains data integrity across all bill fields")
    print("   • Enhanced user experience with helpful guidance")
    print("\nThe Bills Tracker now has robust input validation that makes")
    print("the application more reliable and easier to use!")

if __name__ == "__main__":
    main()
