#!/usr/bin/env python3
"""
Demo script for the Auto-Complete feature in Bills Tracker
This script demonstrates the intelligent bill name and website suggestions.
"""

import difflib

def create_sample_bills():
    """Create sample bills for demonstration."""
    return [
        {
            "name": "Netflix Subscription",
            "due_date": "2025-07-15",
            "web_page": "https://netflix.com",
            "login_info": "user@email.com",
            "paid": False,
            "billing_cycle": "monthly"
        },
        {
            "name": "Electric Bill - Pacific Gas",
            "due_date": "2025-07-20",
            "web_page": "https://pge.com",
            "login_info": "customer123",
            "paid": False,
            "billing_cycle": "monthly"
        },
        {
            "name": "Internet Service Provider",
            "due_date": "2025-07-25",
            "web_page": "https://comcast.com",
            "login_info": "homeuser",
            "paid": True,
            "billing_cycle": "monthly"
        },
        {
            "name": "Phone Bill - Verizon",
            "due_date": "2025-07-10",
            "web_page": "https://verizon.com",
            "login_info": "mobile_user",
            "paid": False,
            "billing_cycle": "monthly"
        },
        {
            "name": "Water Bill",
            "due_date": "2025-07-30",
            "web_page": "https://waterworks.com",
            "login_info": "resident456",
            "paid": False,
            "billing_cycle": "monthly"
        }
    ]

class DemoAutoComplete:
    """Demo version of auto-complete functionality."""
    
    @staticmethod
    def get_bill_names(bills):
        """Get all bill names for auto-completion."""
        return [bill['name'] for bill in bills]
    
    @staticmethod
    def get_websites(bills):
        """Get all unique websites for auto-completion."""
        websites = set()
        for bill in bills:
            if bill.get('web_page'):
                websites.add(bill['web_page'])
        return list(websites)
    
    @staticmethod
    def suggest_names(bills, partial_input, max_suggestions=5):
        """Suggest bill names based on partial input."""
        if not partial_input or not bills:
            return []
        
        bill_names = DemoAutoComplete.get_bill_names(bills)
        partial_lower = partial_input.lower()
        
        # Find exact matches first
        exact_matches = [name for name in bill_names if name.lower().startswith(partial_lower)]
        
        # Find fuzzy matches if we need more suggestions
        if len(exact_matches) < max_suggestions:
            fuzzy_matches = difflib.get_close_matches(
                partial_input, 
                bill_names, 
                n=max_suggestions - len(exact_matches),
                cutoff=0.3
            )
            # Remove duplicates
            fuzzy_matches = [name for name in fuzzy_matches if name not in exact_matches]
            exact_matches.extend(fuzzy_matches)
        
        return exact_matches[:max_suggestions]
    
    @staticmethod
    def suggest_websites(bills, partial_input, max_suggestions=3):
        """Suggest websites based on partial input."""
        if not partial_input or not bills:
            return []
        
        websites = DemoAutoComplete.get_websites(bills)
        partial_lower = partial_input.lower()
        
        # Find matches
        matches = [site for site in websites if partial_lower in site.lower()]
        return matches[:max_suggestions]

def demo_autocomplete_features():
    """Demonstrate the auto-complete functionality."""
    print("💡 Auto-Complete Feature Demo")
    print("="*50)
    print()
    
    bills = create_sample_bills()
    
    print("📋 Sample bills:")
    for i, bill in enumerate(bills, 1):
        status = "✓ Paid" if bill.get('paid', False) else "○ Unpaid"
        print(f"  {i}. {bill['name']} [{status}]")
    print()
    
    # Test name suggestions
    print("📝 Testing bill name auto-complete:")
    print()
    
    test_inputs = ["net", "bill", "electric", "phone", "wat", "internet"]
    
    for test_input in test_inputs:
        suggestions = DemoAutoComplete.suggest_names(bills, test_input)
        print(f"Input: '{test_input}'")
        if suggestions:
            print(f"  ✅ Suggestions: {suggestions}")
        else:
            print(f"  ❌ No suggestions found")
        print()
    
    # Test website suggestions
    print("🌐 Testing website auto-complete:")
    print()
    
    websites = DemoAutoComplete.get_websites(bills)
    print(f"Available websites: {websites}")
    print()
    
    website_tests = ["netflix", "com", "verizon", "pge"]
    for test_input in website_tests:
        suggestions = DemoAutoComplete.suggest_websites(bills, test_input)
        print(f"Website input: '{test_input}'")
        if suggestions:
            print(f"  ✅ Suggestions: {suggestions}")
        else:
            print(f"  ❌ No suggestions found")
        print()

def interactive_demo():
    """Interactive auto-complete demonstration."""
    print("🎮 Interactive Auto-Complete Demo")
    print("="*50)
    print()
    
    bills = create_sample_bills()
    
    print("📋 Available bills:")
    for i, bill in enumerate(bills, 1):
        status = "✓ Paid" if bill.get('paid', False) else "○ Unpaid"
        print(f"  {i}. {bill['name']} [{status}]")
    print()
    
    print("🔍 Try typing partial bill names to see suggestions!")
    print("💡 Tips:")
    print("  • Type 'net' to see Netflix suggestions")
    print("  • Type 'bill' to see bills containing 'bill'")
    print("  • Type 'electric' to see electric bill suggestions")
    print("  • Type 'quit' to exit")
    print()
    
    while True:
        try:
            user_input = input("Enter partial bill name: ").strip()
            
            if user_input.lower() == 'quit':
                break
            
            if not user_input:
                print("Please enter something to search for.")
                continue
            
            suggestions = DemoAutoComplete.suggest_names(bills, user_input)
            
            if suggestions:
                print(f"✅ Suggestions for '{user_input}':")
                for i, suggestion in enumerate(suggestions, 1):
                    # Highlight the matching part
                    if user_input.lower() in suggestion.lower():
                        start = suggestion.lower().find(user_input.lower())
                        highlighted = (suggestion[:start] + 
                                     f"[{suggestion[start:start+len(user_input)]}]" +
                                     suggestion[start+len(user_input):])
                        print(f"  {i}. {highlighted}")
                    else:
                        print(f"  {i}. {suggestion}")
            else:
                print(f"❌ No suggestions found for '{user_input}'")
            
            print()
            
        except KeyboardInterrupt:
            print("\n\nDemo interrupted.")
            break
        except EOFError:
            print("\n\nDemo completed.")
            break

def main():
    """Main demo function."""
    print("🎨 Bills Tracker - Auto-Complete Feature Demo")
    print("=" * 60)
    print()
    
    print("✨ New Feature: Auto-Complete for Bill Names and Websites!")
    print()
    print("🎯 Features demonstrated:")
    print("  • Intelligent bill name suggestions while typing")
    print("  • Website auto-completion based on existing bills")
    print("  • Fuzzy matching for partial inputs")
    print("  • Exact prefix matching for quick selection")
    print()
    
    while True:
        print("Demo Options:")
        print("1. � Auto-complete algorithm demo")
        print("2. 🎮 Interactive auto-complete demo")
        print("3. � View feature documentation")
        print("4. 🚪 Exit demo")
        print()
        
        choice = input("Choose demo option (1-4): ").strip()
        
        if choice == '1':
            print()
            demo_autocomplete_features()
            input("Press Enter to continue...")
            print()
        elif choice == '2':
            print()
            interactive_demo()
            print()
        elif choice == '3':
            print()
            show_documentation()
            input("Press Enter to continue...")
            print()
        elif choice == '4':
            print("👋 Thanks for trying the auto-complete demo!")
            break
        else:
            print("❌ Invalid option. Please choose 1-4.")
            print()

def show_documentation():
    """Show auto-complete feature documentation."""
    print("📚 Auto-Complete Feature Documentation")
    print("="*50)
    print()
    print("🔧 Implementation Details:")
    print("  • Uses Python's difflib for fuzzy matching")
    print("  • Exact prefix matches are prioritized")
    print("  • Configurable maximum number of suggestions")
    print("  • Case-insensitive matching")
    print()
    print("🎯 Use Cases:")
    print("  • Search bills by name with suggestions")
    print("  • Search bills by website with suggestions")
    print("  • Prevent duplicate bill names during creation")
    print("  • Quick reference to existing bills")
    print()
    print("⌨️  User Interface:")
    print("  • Type partial names to see suggestions")
    print("  • Use numbers to select suggestions")
    print("  • Type '?' to see all available options")
    print("  • Type 'cancel' to cancel operations")
    print("  • Type 'help' for assistance")
    print()
    print("🔍 Enhanced Search Experience:")
    print("  • No more guessing exact bill names")
    print("  • Faster bill lookup and selection")
    print("  • Reduced typing errors")
    print("  • Better user experience")

if __name__ == "__main__":
    main()
