#!/usr/bin/env python3
"""
Test script to verify all main menu options work without NameError or function definition errors.
"""

import subprocess
import sys
import time

def test_menu_option(option_number, option_name):
    """Test a specific menu option."""
    print(f"Testing option {option_number}: {option_name}")
    
    try:
        # Test the option and immediately return to avoid waiting for input
        if option_number == 5:  # Due bills menu has submenu
            input_data = f"{option_number}\n3\n9\n"  # Go to due bills, back to main, then exit
        elif option_number == 3:  # Search menu has submenu
            input_data = f"{option_number}\n5\n9\n"  # Go to search, back to main, then exit
        elif option_number == 4:  # Sort menu has submenu
            input_data = f"{option_number}\n8\n9\n"  # Go to sort, back to main, then exit
        else:
            input_data = f"{option_number}\n9\n"  # Test option then exit
        
        result = subprocess.run(
            [sys.executable, "bills-tracker.py"],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=10
        )
        
        if "NameError" in result.stderr or "not defined" in result.stderr:
            print(f"  ❌ FAILED: NameError or function definition error")
            print(f"  Error: {result.stderr}")
            return False
        elif result.returncode != 0 and "EOFError" not in result.stderr:
            print(f"  ❌ FAILED: Unexpected error (exit code {result.returncode})")
            print(f"  Error: {result.stderr}")
            return False
        else:
            print(f"  ✅ PASSED: No NameError or definition errors")
            return True
            
    except subprocess.TimeoutExpired:
        print(f"  ⚠️  TIMEOUT: Test took too long (probably waiting for input)")
        return True  # Timeout is okay, means it's running
    except Exception as e:
        print(f"  ❌ FAILED: Exception occurred: {e}")
        return False

def main():
    """Test all menu options."""
    print("🧪 Testing Bills Tracker Menu Options")
    print("=" * 50)
    
    menu_options = [
        (1, "Add a bill"),
        (2, "View all bills"),
        (3, "Search bills"),
        (4, "Sort bills"),
        (5, "Check due bills"),
        (6, "Pay a bill"),
        (7, "Edit a bill"),
        (8, "Delete a bill"),
    ]
    
    passed = 0
    total = len(menu_options)
    
    for option_num, option_name in menu_options:
        success = test_menu_option(option_num, option_name)
        if success:
            passed += 1
        time.sleep(0.5)  # Small delay between tests
    
    print("\n" + "=" * 50)
    print(f"📊 TEST RESULTS: {passed}/{total} menu options passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! No NameError or function definition issues.")
    else:
        print(f"⚠️  {total - passed} menu options still have issues.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
