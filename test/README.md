# Test Scripts 🧪

This folder contains test scripts that validate the Bills Tracker application's functionality, edge cases, and error handling.

## Available Test Scripts

### ✅ Input Validation Tests
**File:** `test_validation.py`
- **Purpose:** Tests all input validation functions
- **Tests Covered:**
  - URL validation and correction
  - Email format validation
  - Date range validation
  - Reminder period validation
  - Edge cases and error scenarios
- **Usage:** `python test_validation.py`

### 🔄 Billing Cycle Tests
**File:** `test_billing_cycles.py`
- **Purpose:** Tests billing cycle calculations and edge cases
- **Tests Covered:**
  - All billing cycle types (weekly, monthly, etc.)
  - Month-end date handling (Jan 31 → Feb 28/29)
  - Leap year calculations
  - Year boundary transitions
- **Usage:** `python test_billing_cycles.py`

### ⚠️ Edge Case Tests
**File:** `test_edge_cases.py`
- **Purpose:** Tests unusual scenarios and edge cases
- **Tests Covered:**
  - Invalid date formats
  - Extreme date ranges
  - Boundary conditions
  - Error recovery scenarios
- **Usage:** `python test_edge_cases.py`

### 🖥️ Menu Options Tests
**File:** `test_menu_options.py`
- **Purpose:** Tests all main menu options for errors
- **Tests Covered:**
  - All menu options (1-9)
  - NameError detection
  - Function definition validation
  - Error handling verification
- **Usage:** `python test_menu_options.py`

### 💡 Auto-Complete Tests
**File:** `test_autocomplete.py`
- **Purpose:** Tests auto-complete functionality and algorithms
- **Tests Covered:**
  - Bill name suggestion algorithms
  - Website auto-completion
  - Fuzzy matching capabilities
  - Edge case handling
  - Performance with large datasets
  - Case sensitivity testing
- **Usage:** `python test_autocomplete.py`

## How to Run Test Scripts

### Run Individual Tests
```bash
cd test
python test_validation.py
python test_billing_cycles.py
python test_edge_cases.py
python test_menu_options.py
python test_autocomplete.py
```

### Run from Main Directory
```bash
python test/test_validation.py
python test/test_billing_cycles.py
python test/test_edge_cases.py
python test/test_menu_options.py
python test/test_autocomplete.py
```

### Run All Tests at Once
```bash
cd test
for test in test_*.py; do echo "Running $test" && python "$test" && echo; done
```

## Test Results Format

Each test script provides:
- ✅ **PASSED** - Test completed successfully
- ❌ **FAILED** - Test found an issue
- ⚠️ **WARNING** - Test completed with warnings
- 📊 **SUMMARY** - Overall test results

## Test Categories

### Unit Tests
- Test individual functions
- Validate input/output behavior
- Check error handling

### Integration Tests
- Test feature interactions
- Validate end-to-end workflows
- Check data persistence

### Edge Case Tests
- Boundary conditions
- Invalid inputs
- Extreme scenarios
- Error recovery

### Regression Tests
- Ensure new features don't break existing functionality
- Validate bug fixes
- Check backward compatibility

## Test Development Guidelines

When creating new test scripts:

1. **Clear Test Names:** Use descriptive function/test names
2. **Expected vs Actual:** Always compare expected with actual results
3. **Error Handling:** Test both success and failure scenarios
4. **Documentation:** Comment what each test validates
5. **Independence:** Tests shouldn't depend on other tests
6. **Cleanup:** Clean up any test data or state changes

### Example Test Structure
```python
def test_url_validation():
    """Test URL validation function with various inputs."""
    # Test valid URLs
    assert validate_url("google.com") == "https://google.com"
    
    # Test invalid URLs
    assert validate_url("not-a-url") is None
    
    # Test edge cases
    assert validate_url("") == ""
```

## Continuous Testing

These tests should be run:
- Before committing code changes
- After adding new features
- When fixing bugs
- Before releasing new versions

## Test Data

Test scripts use:
- **Isolated test data** that doesn't affect production bills
- **Predictable inputs** for consistent results
- **Varied scenarios** to catch different issues
- **Edge cases** to test boundaries

## Integration with CI/CD

These tests can be integrated into:
- Git hooks (pre-commit, pre-push)
- Continuous integration pipelines
- Automated testing workflows
- Code quality checks

---

*Test scripts ensure the Bills Tracker application works correctly and reliably.*
