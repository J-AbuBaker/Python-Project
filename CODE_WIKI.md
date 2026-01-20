# Smart Records System - Code Wiki & Architecture Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Code Flow & Interactions](#code-flow--interactions)
4. [File Structure & Purpose](#file-structure--purpose)
5. [Key Components Explained](#key-components-explained)
6. [Data Flow Examples](#data-flow-examples)
7. [For Beginners: Understanding Python Concepts](#for-beginners-understanding-python-concepts)

---

## System Overview

The Smart Records System is a **GUI-based database application** built with Python. It allows users to manage employee and department records through a user-friendly interface.

### What This Application Does:
- **User Authentication**: Login and registration system
- **Employee Management**: Add, view, search, update, and delete employees
- **Department Management**: Add, view, update, and delete departments
- **Report Generation**: Generate and export reports in PDF or TXT format

### Technology Stack:
- **Python 3.7+**: Programming language
- **CustomTkinter**: Modern GUI framework (built on tkinter)
- **MySQL**: Database for storing data
- **mysql-connector-python**: Python library to connect to MySQL
- **reportlab**: Library for generating PDF reports

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      USER INTERFACE                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │ Login Window │  │ Main Window   │  │ Form Windows │    │
│  └──────┬───────┘  └──────┬────────┘  └──────┬───────┘    │
│         │                 │                    │            │
└─────────┼─────────────────┼────────────────────┼──────────┘
          │                 │                    │
          ▼                 ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│                    BUSINESS LOGIC LAYER                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │ AuthManager  │  │EmployeeModel │  │DepartmentModel│    │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘    │
│         │                 │                    │            │
└─────────┼─────────────────┼────────────────────┼──────────┘
          │                 │                    │
          └─────────────────┴────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    DATABASE LAYER                            │
│                  ┌─────────────────┐                         │
│                  │ DatabaseManager │                         │
│                  └────────┬────────┘                         │
└───────────────────────────┼──────────────────────────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │  MySQL Database│
                    └───────────────┘
```

### Layer Explanation:

1. **User Interface Layer (GUI)**: 
   - What users see and interact with
   - Windows, buttons, forms, menus
   - Files: `gui/*.py`

2. **Business Logic Layer**:
   - Contains the "rules" and operations
   - Handles validation, calculations, data processing
   - Files: `auth/auth_manager.py`, `database/models.py`

3. **Database Layer**:
   - Handles all database communication
   - Executes SQL queries
   - Files: `database/db_manager.py`

4. **Database**:
   - Stores all data permanently
   - MySQL database with tables: users, employees, departments

---

## Code Flow & Interactions

### Application Startup Flow

```
1. User runs: python main.py
   │
   ▼
2. main.py → SmartRecordsApp.__init__()
   │
   ├─► Loads database config (db_config.py)
   ├─► Creates DatabaseManager
   ├─► Creates EmployeeModel & DepartmentModel
   ├─► Creates AuthManager
   └─► Shows LoginWindow
   │
   ▼
3. User enters credentials → LoginWindow calls AuthManager.login()
   │
   ├─► AuthManager queries database via DatabaseManager
   ├─► Validates password (hashes and compares)
   └─► If successful → calls on_login_success()
   │
   ▼
4. MainWindow is created and shown
   │
   └─► User can now access all features
```

### Adding an Employee Flow

```
1. User clicks "Add Employee" menu
   │
   ▼
2. MainWindow.add_employee() called
   │
   ├─► Clears content area
   └─► Creates EmployeeForm(mode="add")
   │
   ▼
3. User fills form and clicks "Add Employee"
   │
   ▼
4. EmployeeForm.save_employee() called
   │
   ├─► Validates input (using utils/validators.py)
   │   ├─► Checks required fields
   │   ├─► Validates email format
   │   ├─► Validates phone format
   │   └─► Validates salary and date
   │
   ▼
5. If valid → EmployeeModel.create() called
   │
   ├─► EmployeeModel calls DatabaseManager.execute_update()
   │
   ▼
6. DatabaseManager executes SQL INSERT query
   │
   └─► Data saved to MySQL database
   │
   ▼
7. Success message shown to user
```

### Search Employees Flow

```
1. User clicks "Search Employees" menu
   │
   ▼
2. MainWindow.search_employees() called
   │
   └─► Creates EmployeeForm(mode="search")
   │
   ▼
3. User enters search term and clicks "Search"
   │
   ▼
4. EmployeeForm.search_employees() called
   │
   ├─► Gets search term from input field
   └─► Calls EmployeeModel.search(search_term)
   │
   ▼
5. EmployeeModel.search() called
   │
   ├─► Creates search pattern: "%search_term%"
   └─► Calls DatabaseManager.execute_query() with LIKE conditions
   │
   ▼
6. DatabaseManager executes SQL SELECT query
   │
   └─► Returns matching employees
   │
   ▼
7. Results displayed in treeview widget
```

---

## File Structure & Purpose

### Root Level Files

| File | Purpose |
|------|---------|
| `main.py` | **Entry point** - Starts the application, coordinates all components |
| `db_config.py` | **Configuration** - Database connection settings (host, user, password) |
| `requirements.txt` | **Dependencies** - Lists all Python packages needed |

### Directory Structure

```
Smart Records System/
│
├── auth/                    # Authentication module
│   ├── __init__.py         # Package marker (makes auth a Python package)
│   └── auth_manager.py     # Handles login, registration, password hashing
│
├── database/                # Database module
│   ├── __init__.py         # Package marker
│   ├── db_manager.py       # Database connection and SQL execution
│   └── models.py           # EmployeeModel and DepartmentModel classes
│
├── gui/                     # User interface module
│   ├── __init__.py         # Package marker
│   ├── login_window.py     # Login and registration window
│   ├── main_window.py      # Main application window with menus
│   ├── employee_form.py    # Employee CRUD forms (add/view/update/delete/search)
│   ├── department_form.py  # Department CRUD forms
│   └── report_window.py    # Report viewing and export window
│
├── reports/                 # Report generation module
│   ├── __init__.py         # Package marker
│   └── report_generator.py # Generates reports in TXT and PDF format
│
├── utils/                   # Utility functions
│   ├── __init__.py         # Package marker
│   └── validators.py       # Input validation functions (email, phone, etc.)
│
└── reports_output/          # Generated reports are saved here
    ├── report_*.txt        # Text reports
    └── report_*.pdf        # PDF reports
```

---

## Key Components Explained

### 1. DatabaseManager (`database/db_manager.py`)

**Purpose**: Manages all database operations

**Key Methods**:
- `connect()`: Establishes connection to MySQL
- `initialize_database()`: Creates tables and sample data
- `execute_query()`: Runs SELECT queries (reading data)
- `execute_update()`: Runs INSERT/UPDATE/DELETE queries (modifying data)
- `get_last_insert_id()`: Gets ID of last inserted record

**How It Works**:
```python
# Example: Reading data
results = db_manager.execute_query(
    "SELECT * FROM employees WHERE id = %s",
    (1,)  # Parameters prevent SQL injection
)
# Returns: [{'id': 1, 'first_name': 'John', ...}]

# Example: Writing data
db_manager.execute_update(
    "INSERT INTO employees (first_name, last_name) VALUES (%s, %s)",
    ("John", "Doe")
)
```

### 2. Models (`database/models.py`)

**Purpose**: Provide easy-to-use interface for working with data

**EmployeeModel Methods**:
- `create()`: Add new employee
- `get_all()`: Get all employees
- `get_by_id()`: Get one employee by ID
- `search()`: Search employees by name/email/position
- `update()`: Update employee information
- `delete()`: Delete employee
- `get_statistics()`: Get employee statistics (count, avg salary, etc.)

**DepartmentModel Methods**:
- `create()`: Add new department
- `get_all()`: Get all departments
- `get_by_id()`: Get one department by ID
- `update()`: Update department
- `delete()`: Delete department
- `has_employees()`: Check if department has employees

**How It Works**:
```python
# GUI code doesn't need to know SQL!
employee_model = EmployeeModel(db_manager)

# Add employee - simple!
employee_id = employee_model.create(
    first_name="John",
    last_name="Doe",
    email="john@example.com"
)

# Search employees - easy!
results = employee_model.search("John")
```

### 3. AuthManager (`auth/auth_manager.py`)

**Purpose**: Handles user authentication

**Key Methods**:
- `register_user()`: Create new user account
- `login()`: Authenticate user (check username/password)
- `logout()`: End user session
- `is_authenticated()`: Check if user is logged in
- `hash_password()`: Securely hash passwords (SHA-256)

**Security Features**:
- Passwords are **never stored in plain text**
- Passwords are hashed using SHA-256 algorithm
- Example: "admin123" → "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94"

**How It Works**:
```python
# Register new user
success, message = auth_manager.register_user("newuser", "password123")
# Returns: (True, "User registered successfully")

# Login
success, message = auth_manager.login("newuser", "password123")
# Returns: (True, "Login successful")
# Sets auth_manager.current_user = {'id': 1, 'username': 'newuser'}
```

### 4. GUI Components (`gui/*.py`)

**LoginWindow** (`gui/login_window.py`):
- Shows login form (username, password)
- Shows registration dialog
- Calls AuthManager to authenticate users

**MainWindow** (`gui/main_window.py`):
- Main application window with menu bar
- Coordinates all features (employees, departments, reports)
- Creates forms based on menu selection

**EmployeeForm** (`gui/employee_form.py`):
- Handles all employee operations
- Different "modes": add, view, update, delete, search
- Uses EmployeeModel to save/load data
- Uses validators to check input

**DepartmentForm** (`gui/department_form.py`):
- Handles all department operations
- Similar to EmployeeForm but for departments

**ReportWindow** (`gui/report_window.py`):
- Displays reports
- Allows exporting to PDF or TXT
- Uses ReportGenerator to create reports

### 5. Validators (`utils/validators.py`)

**Purpose**: Validate user input before saving to database

**Functions**:
- `validate_email()`: Check if email format is valid
- `validate_phone()`: Check if phone format is valid
- `validate_required()`: Check if field is not empty
- `validate_salary()`: Check if salary is a valid number
- `validate_date()`: Check if date format is YYYY-MM-DD

**How It Works**:
```python
# Check email
is_valid = validate_email("john@example.com")  # Returns: True
is_valid = validate_email("invalid-email")     # Returns: False

# Check required field
is_valid, error = validate_required("", "Name")
# Returns: (False, "Name is required")
```

### 6. ReportGenerator (`reports/report_generator.py`)

**Purpose**: Generate and export reports

**Key Methods**:
- `generate_report_text()`: Creates formatted text report
- `export_to_txt()`: Saves report as .txt file
- `export_to_pdf()`: Saves report as .pdf file

**Report Contents**:
- Summary statistics (total employees, avg salary, etc.)
- Department-wise employee count
- Complete employee listing
- Complete department listing

---

## Data Flow Examples

### Example 1: User Logs In

```
User Action: Enters username "admin" and password "admin123"
    │
    ▼
LoginWindow.handle_login() called
    │
    ├─► Gets username and password from input fields
    └─► Calls auth_manager.login("admin", "admin123")
        │
        ▼
AuthManager.login()
    │
    ├─► Hashes password: "admin123" → "ef92b778..."
    ├─► Queries database: SELECT * FROM users WHERE username = 'admin'
    │   │
    │   └─► DatabaseManager.execute_query() executes SQL
    │       └─► Returns: [{'id': 1, 'username': 'admin', 'password': 'ef92b778...'}]
    │
    ├─► Compares hashed passwords
    ├─► If match: Sets current_user = {'id': 1, 'username': 'admin'}
    └─► Returns: (True, "Login successful")
        │
        ▼
LoginWindow closes, MainWindow opens
```

### Example 2: Adding an Employee

```
User Action: Fills form and clicks "Add Employee"
    │
    ▼
EmployeeForm.save_employee() called
    │
    ├─► Calls validate_form()
    │   │
    │   ├─► validate_required(first_name) → (True, None)
    │   ├─► validate_required(last_name) → (True, None)
    │   ├─► validate_email(email) → True
    │   ├─► validate_phone(phone) → True
    │   └─► validate_salary(salary) → (True, None, 50000.0)
    │
    ├─► If all valid:
    │   │
    │   └─► Calls employee_model.create(...)
    │       │
    │       └─► Calls db_manager.execute_update()
    │           │
    │           └─► Executes SQL: INSERT INTO employees ...
    │               │
    │               └─► Data saved to MySQL database
    │
    └─► Shows success message: "Employee added successfully!"
```

### Example 3: Generating a Report

```
User Action: Clicks "Generate Reports" menu
    │
    ▼
MainWindow.show_reports() called
    │
    └─► Creates ReportWindow
        │
        ▼
ReportWindow.generate_summary() called
    │
    ├─► Calls employee_model.get_statistics()
    │   │
    │   └─► Executes SQL: SELECT COUNT(*), AVG(salary), ...
    │       └─► Returns: {'total_employees': 25, 'avg_salary': 80000, ...}
    │
    ├─► Calls employee_model.get_all()
    │   └─► Returns: [{'id': 1, 'first_name': 'John', ...}, ...]
    │
    ├─► Calls department_model.get_all()
    │   └─► Returns: [{'id': 1, 'name': 'IT', ...}, ...]
    │
    ├─► Formats data into report text
    └─► Displays in text widget
```

---

## For Beginners: Understanding Python Concepts

### Classes and Objects

**What is a Class?**
A class is like a blueprint or template. It defines what an object can do.

**Example**:
```python
class EmployeeModel:
    def __init__(self, db_manager):
        self.db = db_manager  # Store database manager
    
    def create(self, name):
        # Code to create employee
        pass

# Create an object from the class
employee_model = EmployeeModel(db_manager)
# Now employee_model is an "instance" of EmployeeModel
```

**Think of it like**: A class is a cookie cutter, objects are the cookies made from it.

### Methods and Functions

**Method**: A function that belongs to a class
```python
class EmployeeModel:
    def create(self, name):  # This is a METHOD
        pass

# Call the method
employee_model.create("John")
```

**Function**: A standalone function not in a class
```python
def validate_email(email):  # This is a FUNCTION
    return True

# Call the function
validate_email("john@example.com")
```

### Dictionaries

**Dictionary**: A collection of key-value pairs (like a real dictionary: word = key, definition = value)

```python
# Create dictionary
employee = {
    'id': 1,
    'first_name': 'John',
    'last_name': 'Doe',
    'email': 'john@example.com'
}

# Access values
name = employee['first_name']  # Gets 'John'
email = employee.get('email', 'N/A')  # Gets 'john@example.com' or 'N/A' if not found
```

### Lists

**List**: An ordered collection of items

```python
# Create list
employees = [
    {'id': 1, 'name': 'John'},
    {'id': 2, 'name': 'Jane'}
]

# Access items
first_employee = employees[0]  # Gets first employee
total = len(employees)  # Gets count: 2
```

### Tuples

**Tuple**: An ordered, immutable collection (cannot be changed after creation)

```python
# Create tuple
params = ("John", "Doe")  # Note: parentheses and comma

# Use in SQL queries
db.execute_query("SELECT * FROM employees WHERE first_name = %s AND last_name = %s", params)
# %s placeholders are filled with tuple values
```

### Try/Except (Error Handling)

**Purpose**: Handle errors gracefully without crashing

```python
try:
    # Code that might fail
    result = 10 / 0  # This will cause an error!
except ZeroDivisionError:
    # What to do if error occurs
    print("Cannot divide by zero!")
```

### Imports

**Import**: Bring in code from other files/modules

```python
# Import entire module
import customtkinter as ctk

# Import specific class/function
from database.db_manager import DatabaseManager

# Import from same package
from .db_manager import DatabaseManager  # . means "same directory"
```

### SQL Queries (Basic)

**SELECT**: Read data from database
```sql
SELECT * FROM employees WHERE id = 1
-- Gets all columns (*) from employees table where id equals 1
```

**INSERT**: Add new data
```sql
INSERT INTO employees (first_name, last_name) VALUES ('John', 'Doe')
-- Adds new row to employees table
```

**UPDATE**: Modify existing data
```sql
UPDATE employees SET salary = 50000 WHERE id = 1
-- Changes salary to 50000 for employee with id = 1
```

**DELETE**: Remove data
```sql
DELETE FROM employees WHERE id = 1
-- Removes employee with id = 1
```

---

## Common Questions

### Q: How does the application know which database to connect to?
**A**: The `db_config.py` file contains all database connection settings (host, user, password, database name). The `DatabaseManager` reads this file when the application starts.

### Q: Where is user data stored?
**A**: All data is stored in a MySQL database. The database has three main tables:
- `users`: Stores user accounts (username, hashed password)
- `departments`: Stores department information
- `employees`: Stores employee information

### Q: How are passwords secured?
**A**: Passwords are never stored in plain text. They are hashed using SHA-256 algorithm before storing. When a user logs in, their entered password is hashed and compared to the stored hash.

### Q: What happens if I delete a department that has employees?
**A**: The database has a foreign key constraint `ON DELETE SET NULL`. This means if you delete a department, employees in that department will have their `department_id` set to `NULL` (no department). They won't be deleted.

### Q: How do I add new features?
**A**: 
1. Add database tables/columns if needed (in `db_manager.py`)
2. Add model methods if needed (in `models.py`)
3. Add GUI components (in `gui/` directory)
4. Connect GUI to models (call model methods from GUI)

### Q: Can I use a different database?
**A**: Currently, the application is designed for MySQL. To use a different database (like PostgreSQL or SQLite), you would need to modify `db_manager.py` to use a different database connector library.

---

## Summary

The Smart Records System follows a **layered architecture**:

1. **GUI Layer** → User sees and interacts with
2. **Business Logic Layer** → Handles rules and operations
3. **Database Layer** → Stores and retrieves data
4. **Database** → Permanent storage

Each layer communicates with the layer below it, creating a clean separation of concerns. This makes the code:
- **Easy to understand**: Each file has a clear purpose
- **Easy to maintain**: Changes in one layer don't break others
- **Easy to test**: Each component can be tested independently

The code is well-documented with comments explaining what each line does, making it perfect for beginners learning Python!
