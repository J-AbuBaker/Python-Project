# Smart Records System

A comprehensive GUI-based database application for managing employee and department records with user authentication, CRUD operations, and report generation capabilities.

## 📋 Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
- [Project Structure](#project-structure)
- [Documentation](#documentation)
- [Database Schema](#database-schema)
- [Troubleshooting](#troubleshooting)
- [For Beginners](#for-beginners)

---

## ✨ Features

- **🔐 User Authentication**: Secure login system with password hashing (SHA-256) and user registration
- **💾 Database Integration**: Full MySQL database support with automatic table creation
- **📝 CRUD Operations**: Complete Create, Read, Update, Delete functionality for employees and departments
- **📊 Report Generation**: Generate comprehensive summary reports and export to PDF or TXT format
- **🎨 Modern GUI**: Clean, modern interface built with CustomTkinter
- **✅ Input Validation**: Comprehensive validation for email, phone, salary, and dates
- **🔍 Search Functionality**: Search employees by name, email, or position
- **📈 Statistics**: View employee statistics (total count, average salary, min/max salary, etc.)

---

## 📦 Requirements

### Software Requirements
- **Python 3.7 or higher** (Python 3.8+ recommended)
- **MySQL Server** (5.7+ or 8.0+)
- **Windows, macOS, or Linux** operating system

### Python Dependencies
All dependencies are listed in `requirements.txt`. Main packages:
- `customtkinter` - Modern GUI framework
- `reportlab` - PDF report generation
- `mysql-connector-python` - MySQL database connector

---

## 🚀 Installation

### Step 1: Clone or Download the Repository

```bash
git clone https://github.com/J-AbuBaker/Python-Project.git
cd Python-Project
```

Or download and extract the ZIP file.

### Step 2: Install Python Dependencies

Open a terminal/command prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

Or install packages individually:

```bash
pip install customtkinter reportlab mysql-connector-python
```

**Note for Windows users**: If you encounter issues installing `customtkinter`, try:
```bash
pip install --upgrade pip
pip install customtkinter
```

### Step 3: Setup MySQL Database

#### Option A: Using MySQL Command Line

1. **Start MySQL server** (if not already running)

2. **Open MySQL command line**:
   ```bash
   mysql -u root -p
   ```
   Enter your MySQL root password when prompted.

3. **Create the database**:
   ```sql
   CREATE DATABASE smart_records CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   EXIT;
   ```

#### Option B: Using phpMyAdmin

1. Navigate to `http://localhost/phpmyadmin` in your web browser
2. Click "New" in the left sidebar
3. Enter database name: `smart_records`
4. Select collation: `utf8mb4_unicode_ci`
5. Click "Create"

#### Option C: Using MySQL Workbench

1. Open MySQL Workbench
2. Connect to your MySQL server
3. Click "Create Schema" (or right-click → Create Schema)
4. Name: `smart_records`
5. Default collation: `utf8mb4 - utf8mb4_unicode_ci`
6. Click "Apply"

### Step 4: Configure Database Connection

Create a file named `db_config.py` in the project root directory with the following content:

   ```python
# Database Configuration File
   MYSQL_CONFIG = {
    'host': 'localhost',      # MySQL server address (use 'localhost' if on same computer)
    'port': 3306,             # MySQL port (default is 3306)
    'user': 'root',           # Your MySQL username
    'password': 'YOUR_PASSWORD',  # ⚠️ CHANGE THIS to your MySQL password!
    'database': 'smart_records'  # Database name (created in Step 3)
}
```

**⚠️ Important**: Replace `'YOUR_PASSWORD'` with your actual MySQL root password!

---

## 🎯 Quick Start

1. **Make sure MySQL is running** on your computer

2. **Run the application**:
```bash
python main.py
```

3. **Login with default credentials**:
- **Username**: `admin`
- **Password**: `admin123`

4. **⚠️ Change the default password** after first login for security!

The application will automatically:
- Connect to your MySQL database
- Create all necessary tables (if they don't exist)
- Create default admin user (if no users exist)
- Create sample departments and employees (if database is empty)

---

## 📖 Usage Guide

### Employee Management

#### Add Employee
1. Click **Employees** → **Add Employee** from the menu bar
2. Fill in the form:
   - **First Name*** (required)
   - **Last Name*** (required)
   - **Email*** (required, must be unique)
   - **Phone** (optional)
   - **Position** (optional)
   - **Salary** (optional)
   - **Department** (optional, select from dropdown)
   - **Hire Date** (optional, format: YYYY-MM-DD)
3. Click **Add Employee** button
4. Success message will appear

#### View All Employees
1. Click **Employees** → **View All Employees**
2. A table showing all employees will be displayed
3. Scroll to see more employees

#### Search Employees
1. Click **Employees** → **Search Employees**
2. Enter search term in the search box
3. Click **Search** button or press Enter
4. Results matching name, email, or position will be shown

#### Update Employee
1. Click **Employees** → **Update Employee**
2. Select employee from dropdown
3. Modify the fields you want to change
4. Click **Update Employee** button

#### Delete Employee
1. Click **Employees** → **Delete Employee**
2. Select employee from dropdown
3. Review employee information
4. Click **Delete Employee** button
5. Confirm deletion in the popup dialog

### Department Management

#### Add Department
1. Click **Departments** → **Add Department**
2. Enter department name* (required)
3. Enter description (optional)
4. Click **Add Department** button

#### View All Departments
1. Click **Departments** → **View All Departments**
2. A table showing all departments will be displayed

#### Update Department
1. Click **Departments** → **Update Department**
2. Select department from dropdown
3. Modify name and/or description
4. Click **Update Department** button

#### Delete Department
1. Click **Departments** → **Delete Department**
2. Select department from dropdown
3. Review department information
4. **Note**: If department has employees, they will be notified
5. Click **Delete Department** button and confirm

### Reports

#### View Reports
1. Click **Reports** → **Generate Reports**
2. A comprehensive report will be displayed showing:
   - Summary statistics (total employees, average salary, etc.)
   - Department-wise employee count
   - Complete employee listing
   - Complete department listing

#### Export Reports
- **Export to TXT**: Click **Export to TXT** button (saves to `reports_output/` folder)
- **Export to PDF**: Click **Export to PDF** button (requires `reportlab` package)

Reports are saved with timestamps in the filename (e.g., `report_20240115_143022.txt`)

---

## 📁 Project Structure

```
Smart Records System/
│
├── main.py                    # 🚀 Application entry point - starts the app
├── db_config.py              # ⚙️ Database configuration (edit with your MySQL credentials)
├── requirements.txt          # 📦 Python package dependencies
├── README.md                 # 📖 This file - user guide
├── CODE_WIKI.md             # 📚 Comprehensive code documentation (for developers)
│
├── auth/                     # 🔐 Authentication module
│   ├── __init__.py
│   └── auth_manager.py     # Handles login, registration, password hashing
│
├── database/                 # 💾 Database module
│   ├── __init__.py
│   ├── db_manager.py        # Database connection and SQL execution
│   └── models.py            # EmployeeModel and DepartmentModel classes
│
├── gui/                      # 🎨 User interface module
│   ├── __init__.py
│   ├── login_window.py      # Login and registration window
│   ├── main_window.py        # Main application window with menus
│   ├── employee_form.py     # Employee CRUD forms
│   ├── department_form.py   # Department CRUD forms
│   └── report_window.py     # Report viewing window
│
├── reports/                  # 📊 Report generation module
│   ├── __init__.py
│   └── report_generator.py  # Generates TXT and PDF reports
│
├── utils/                    # 🛠️ Utility functions
│   ├── __init__.py
│   └── validators.py        # Input validation functions
│
└── reports_output/           # 📁 Generated reports are saved here
    ├── report_*.txt
    └── report_*.pdf
```

---

## 📚 Documentation

### For Users
- **This README.md**: Installation, usage, and troubleshooting guide
- **In-app Help**: Click **Help** → **About** in the application menu

### For Developers
- **CODE_WIKI.md**: Comprehensive code documentation including:
  - System architecture and design patterns
  - Code flow and interactions
  - File-by-file explanations
  - Data flow examples
  - Python concepts for beginners
  - Common questions and answers

### Code Documentation
Every Python file is **extensively documented** with:
- Line-by-line comments explaining what each line does
- Function/method docstrings explaining purpose, parameters, and return values
- Examples and usage patterns
- Notes for beginners learning Python

**Recommended reading order for developers**:
1. `CODE_WIKI.md` - Understand the overall architecture
2. `main.py` - See how the application starts
3. `database/db_manager.py` - Understand database operations
4. `database/models.py` - See how data models work
5. `gui/main_window.py` - Understand GUI structure
6. Other files as needed

---

## 🗄️ Database Schema

The application uses three main tables:

### Users Table
Stores user accounts for authentication.
- `id` (INTEGER, PRIMARY KEY, AUTO_INCREMENT)
- `username` (VARCHAR(255), UNIQUE, NOT NULL)
- `password` (VARCHAR(255), NOT NULL) - **Stored as SHA-256 hash**
- `created_at` (TIMESTAMP) - Auto-set when account is created

### Departments Table
Stores department information.
- `id` (INTEGER, PRIMARY KEY, AUTO_INCREMENT)
- `name` (VARCHAR(255), UNIQUE, NOT NULL)
- `description` (VARCHAR(255))
- `created_at` (TIMESTAMP)

### Employees Table
Stores employee information.
- `id` (INTEGER, PRIMARY KEY, AUTO_INCREMENT)
- `first_name` (VARCHAR(255), NOT NULL)
- `last_name` (VARCHAR(255), NOT NULL)
- `email` (VARCHAR(255), UNIQUE, NOT NULL)
- `phone` (VARCHAR(255))
- `position` (VARCHAR(255))
- `salary` (DECIMAL(10,2))
- `department_id` (INTEGER, FOREIGN KEY → departments.id)
- `hire_date` (DATE)
- `created_at` (TIMESTAMP)

**Foreign Key Relationship**:
- `employees.department_id` → `departments.id`
- **ON DELETE SET NULL**: If a department is deleted, employees' `department_id` is set to NULL (employees are not deleted)

---

## 🔧 Troubleshooting

### Application Won't Start

**Problem**: Error when running `python main.py`

**Solutions**:
1. **Check Python version**: Run `python --version` (must be 3.7+)
2. **Install dependencies**: Run `pip install -r requirements.txt`
3. **Check db_config.py**: Make sure file exists and has correct MySQL credentials
4. **Check MySQL**: Make sure MySQL server is running

### MySQL Connection Failed

**Problem**: "Failed to connect to MySQL" error

**Solutions**:
1. **Verify MySQL is running**:
   - Windows: Check Services (search "services.msc"), look for "MySQL"
   - macOS/Linux: Run `sudo systemctl status mysql` or `brew services list`
2. **Check credentials**: Verify username and password in `db_config.py`
3. **Check database exists**: Run `mysql -u root -p` and check: `SHOW DATABASES;`
4. **Create database**: If `smart_records` doesn't exist, create it (see Installation Step 3)
5. **Check port**: Default MySQL port is 3306, verify in `db_config.py`

### PDF Export Fails

**Problem**: "Failed to export PDF" error

**Solutions**:
1. **Install reportlab**: Run `pip install reportlab`
2. **Check permissions**: Make sure `reports_output/` folder is writable
3. **Check disk space**: Ensure you have enough disk space

### Login Issues

**Problem**: Cannot login with default credentials

**Solutions**:
1. **Check username/password**: Default is `admin` / `admin123` (case-sensitive)
2. **Database not initialized**: Delete database and recreate it, then run the app
3. **Check database**: Verify users table exists and has admin user

### Import Errors

**Problem**: "ModuleNotFoundError" or "ImportError"

**Solutions**:
1. **Install missing package**: Run `pip install <package-name>`
2. **Check Python path**: Make sure you're running from the project root directory
3. **Virtual environment**: If using virtual environment, make sure it's activated

### GUI Not Displaying Correctly

**Problem**: Buttons/widgets look wrong or don't appear

**Solutions**:
1. **Update customtkinter**: Run `pip install --upgrade customtkinter`
2. **Check Python version**: CustomTkinter requires Python 3.7+
3. **Try different theme**: The code uses "blue" theme, you can modify in `main.py`

---

## 🎓 For Beginners

### What is This Application?

This is a **desktop application** (runs on your computer) that helps you manage employee and department records. Think of it like a digital filing cabinet where you can:
- Store employee information (name, email, salary, etc.)
- Organize employees into departments
- Search for specific employees
- Generate reports

### Key Concepts

**GUI (Graphical User Interface)**: The windows, buttons, and forms you see and click. Built with CustomTkinter.

**Database**: Where all your data is permanently stored. This app uses MySQL.

**CRUD**: Create, Read, Update, Delete - the four basic operations for managing data.

**Authentication**: Login system to protect your data from unauthorized access.

### Learning Python?

This project is **perfect for learning Python** because:
- ✅ Every file is extensively documented with line-by-line comments
- ✅ Uses common Python concepts (classes, functions, dictionaries, lists)
- ✅ Follows best practices and clean code structure
- ✅ Real-world application (not just a tutorial example)

**Recommended learning path**:
1. Read `CODE_WIKI.md` to understand the architecture
2. Start with `main.py` - see how the app starts
3. Look at `utils/validators.py` - simple functions, easy to understand
4. Explore `database/models.py` - see how data operations work
5. Study `gui/` files - understand how user interfaces are built

### Need Help?

- **Code questions**: Read `CODE_WIKI.md` for detailed explanations
- **Usage questions**: Check this README.md
- **Python basics**: Check online Python tutorials (Python.org, Real Python, etc.)

---

## 📝 License

This project is open source. Feel free to use, modify, and distribute.

---

## 👥 Credits

Original repository: [J-AbuBaker/Python-Project](https://github.com/J-AbuBaker/Python-Project)

---

## 🎉 Getting Started Checklist

- [ ] Python 3.7+ installed
- [ ] MySQL server installed and running
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Database `smart_records` created
- [ ] `db_config.py` file created with correct credentials
- [ ] Application runs successfully (`python main.py`)
- [ ] Can login with default credentials (`admin` / `admin123`)
- [ ] Read `CODE_WIKI.md` for code understanding (if developing)

**Happy coding! 🚀**
