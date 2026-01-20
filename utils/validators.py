"""
Input Validation Utilities - Smart Records System

This module provides functions to validate user input before it's saved to the database.
This prevents invalid data from being stored and helps catch errors early.

Think of validators as "quality checkers" that ensure data is correct before saving.
"""

# Import re (regular expressions) - used for pattern matching
# Regular expressions are like a "search pattern" language
# Example: r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$' matches email addresses
import re


def validate_email(email):
    """
    Validate email address format.
    
    This function checks if an email address follows the correct format:
    - Must have characters before @
    - Must have @ symbol
    - Must have domain name
    - Must have top-level domain (.com, .org, etc.)
    
    Args:
        email (str): The email address to validate
        
    Returns:
        bool: True if email format is valid, False otherwise
        
    Examples:
        validate_email("john@example.com")  # Returns: True
        validate_email("invalid-email")     # Returns: False
        validate_email("test@domain")        # Returns: False (missing .com)
    """
    # Regular expression pattern for email validation
    # This pattern matches standard email format:
    # - ^[a-zA-Z0-9._%+-]+ : One or more characters (letters, numbers, dots, underscores, etc.)
    # - @ : The @ symbol (required)
    # - [a-zA-Z0-9.-]+ : Domain name (one or more characters)
    # - \. : A literal dot (escaped with \)
    # - [a-zA-Z]{2,}$ : Top-level domain (2 or more letters, like com, org, edu)
    # - ^ means "start of string", $ means "end of string"
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # re.match() checks if the email matches the pattern
    # Returns a match object if it matches, None if it doesn't
    # bool() converts the result to True/False
    return bool(re.match(pattern, email))


def validate_phone(phone):
    """
    Validate phone number format.
    
    This function checks if a phone number contains only valid characters
    (digits, spaces, dashes, parentheses) and has at least 10 digits.
    
    Args:
        phone (str): The phone number to validate
        
    Returns:
        bool: True if phone format is valid or empty, False otherwise
        
    Examples:
        validate_phone("555-1234")        # Returns: True (if has 10+ digits)
        validate_phone("(555) 123-4567")  # Returns: True
        validate_phone("abc123")          # Returns: False (contains letters)
        validate_phone("")                # Returns: True (empty is allowed)
    """
    # If phone is empty, it's valid (phone is optional)
    if not phone:
        return True
    
    # Pattern allows digits, spaces, dashes, parentheses
    # ^[...]+$ means "string contains only these characters"
    pattern = r'^[\d\s\-\(\)]+$'
    
    # Check if phone matches the pattern
    if not re.match(pattern, phone):
        return False
    
    # Count actual digits (remove spaces, dashes, parentheses)
    # .replace() removes characters, then len() counts remaining digits
    digit_count = len(phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', ''))
    
    # Phone must have at least 10 digits
    return digit_count >= 10


def validate_required(value, field_name="Field"):
    """
    Validate that a required field is not empty.
    
    This function checks if a field has a value (not empty or just whitespace).
    
    Args:
        value (str): The value to check
        field_name (str): Name of the field (used in error message)
        
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
               - is_valid: True if field has value, False if empty
               - error_message: Error message if invalid, None if valid
               
    Examples:
        validate_required("John", "Name")     # Returns: (True, None)
        validate_required("", "Email")        # Returns: (False, "Email is required")
        validate_required("   ", "Name")      # Returns: (False, "Name is required")
    """
    # Check if value is empty or contains only whitespace
    # .strip() removes leading/trailing spaces
    # not value.strip() is True if value is empty or only spaces
    if not value or not value.strip():
        # Return False (invalid) with error message
        return False, f"{field_name} is required"
    
    # Value is valid
    return True, None


def validate_salary(salary_str):
    """
    Validate salary value.
    
    This function checks if a salary string is a valid number and not negative.
    
    Args:
        salary_str (str): The salary string to validate
        
    Returns:
        tuple: (is_valid: bool, error_message: str or None, salary_value: float or None)
               - is_valid: True if salary is valid
               - error_message: Error message if invalid, None if valid
               - salary_value: The salary as a float, or None if invalid
               
    Examples:
        validate_salary("50000")        # Returns: (True, None, 50000.0)
        validate_salary("-1000")       # Returns: (False, "Salary cannot be negative", None)
        validate_salary("abc")         # Returns: (False, "Salary must be a valid number", None)
        validate_salary("")            # Returns: (True, None, 0.0)  # Empty is allowed
    """
    # If salary is empty, it's valid (salary is optional, defaults to 0)
    if not salary_str or not salary_str.strip():
        return True, None, 0.0
    
    # Try to convert string to float
    try:
        # float() converts string to decimal number
        salary = float(salary_str)
        
        # Check if salary is negative
        if salary < 0:
            return False, "Salary cannot be negative", None
        
        # Salary is valid
        return True, None, salary
    except ValueError:
        # If float() fails (string is not a number), return error
        # ValueError is raised when string cannot be converted to float
        return False, "Salary must be a valid number", None


def validate_date(date_str):
    """
    Validate date format (YYYY-MM-DD).
    
    This function checks if a date string follows the format YYYY-MM-DD
    and is a valid date (e.g., not February 30th).
    
    Args:
        date_str (str): The date string to validate (format: YYYY-MM-DD)
        
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
               - is_valid: True if date is valid
               - error_message: Error message if invalid, None if valid
               
    Examples:
        validate_date("2024-01-15")    # Returns: (True, None)
        validate_date("01/15/2024")    # Returns: (False, "Date must be in YYYY-MM-DD format")
        validate_date("2024-02-30")    # Returns: (False, "Invalid date")  # February doesn't have 30 days
        validate_date("")              # Returns: (True, None)  # Empty is allowed
    """
    # If date is empty, it's valid (date is optional)
    if not date_str or not date_str.strip():
        return True, None
    
    # Pattern for YYYY-MM-DD format
    # \d{4} means exactly 4 digits (year)
    # \d{2} means exactly 2 digits (month and day)
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    
    # Check if date matches the pattern
    if not re.match(pattern, date_str):
        return False, "Date must be in YYYY-MM-DD format"
    
    # Try to parse the date to check if it's valid
    # (e.g., check if February 30th is rejected)
    try:
        # Import datetime here (not at top) to avoid circular imports if needed
        from datetime import datetime
        
        # strptime() parses a string into a datetime object
        # '%Y-%m-%d' is the format: Year-Month-Day
        # If date is invalid (like Feb 30), this will raise ValueError
        datetime.strptime(date_str, '%Y-%m-%d')
        
        # Date is valid
        return True, None
    except ValueError:
        # If strptime() fails, date is invalid (e.g., Feb 30, Apr 31)
        return False, "Invalid date"
