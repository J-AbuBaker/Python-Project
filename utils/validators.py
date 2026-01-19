"""Input validation utilities."""

import re


def validate_email(email):
    """Validate email address format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone):
    """Validate phone number format. Requires at least 7 digits."""
    if not phone:
        return True
    pattern = r'^[\d\s\-\(\)]+$'
    return bool(re.match(pattern, phone)) and len(phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')) >= 10


def validate_required(value, field_name="Field"):
    """Validate required field. Returns (is_valid, error_message)."""
    if not value or not value.strip():
        return False, f"{field_name} is required"
    return True, None


def validate_salary(salary_str):
    """Validate salary value. Returns (is_valid, error_message, salary_value)."""
    if not salary_str or not salary_str.strip():
        return True, None, 0.0
    
    try:
        salary = float(salary_str)
        if salary < 0:
            return False, "Salary cannot be negative", None
        return True, None, salary
    except ValueError:
        return False, "Salary must be a valid number", None


def validate_date(date_str):
    """Validate date format (YYYY-MM-DD). Returns (is_valid, error_message)."""
    if not date_str or not date_str.strip():
        return True, None
    
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(pattern, date_str):
        return False, "Date must be in YYYY-MM-DD format"
    
    try:
        from datetime import datetime
        datetime.strptime(date_str, '%Y-%m-%d')
        return True, None
    except ValueError:
        return False, "Invalid date"

