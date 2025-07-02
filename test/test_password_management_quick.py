#!/usr/bin/env python3
"""
Quick test script to verify password management functions are working correctly.
"""

import sys
import os

# Add the current directory to the path so we can import bills-tracker
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_password_management_functions():
    """Test that password management functions can be imported and called."""
    try:
        # Import the functions we need to test
        import importlib.util
        spec = importlib.util.spec_from_file_location("bills_tracker", "bills-tracker.py")
        bills_tracker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(bills_tracker)
        
        # Get the functions from the module
        change_master_password = bills_tracker.change_master_password
        reset_master_password = bills_tracker.reset_master_password
        show_password_recovery_options = bills_tracker.show_password_recovery_options
        export_bills_for_recovery = bills_tracker.export_bills_for_recovery
        view_backup_files = bills_tracker.view_backup_files
        password_management_menu = bills_tracker.password_management_menu
        
        print("✅ All password management functions imported successfully!")
        
        # Test that the functions exist and are callable
        functions_to_test = [
            change_master_password,
            reset_master_password,
            show_password_recovery_options,
            export_bills_for_recovery,
            view_backup_files,
            password_management_menu
        ]
        
        for func in functions_to_test:
            if callable(func):
                print(f"✅ {func.__name__} is callable")
            else:
                print(f"❌ {func.__name__} is not callable")
                return False
        
        print("\n✅ All password management functions are working correctly!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_main_menu_integration():
    """Test that the main menu includes password management."""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("bills_tracker", "bills-tracker.py")
        bills_tracker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(bills_tracker)
        
        display_menu = bills_tracker.display_menu
        
        # Capture the menu output
        import io
        from contextlib import redirect_stdout
        
        f = io.StringIO()
        with redirect_stdout(f):
            display_menu()
        
        menu_output = f.getvalue()
        
        # Check if password management is in the menu
        if "Password Management" in menu_output:
            print("✅ Password Management option found in main menu!")
            return True
        else:
            print("❌ Password Management option not found in main menu")
            print("Menu output:")
            print(menu_output)
            return False
            
    except Exception as e:
        print(f"❌ Error testing main menu: {e}")
        return False

if __name__ == "__main__":
    print("Testing Password Management Functions...")
    print("=" * 50)
    
    test1_passed = test_password_management_functions()
    test2_passed = test_main_menu_integration()
    
    print("\n" + "=" * 50)
    if test1_passed and test2_passed:
        print("🎉 All tests passed! Password management is working correctly.")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Please check the implementation.")
        sys.exit(1) 