# Smart Records System

A GUI-based database application for managing employee and department records with user authentication, CRUD operations, and report generation capabilities.

## Features

- **User Authentication**: Secure login system with password hashing and user registration
- **Database Integration**: MySQL database support
- **CRUD Operations**: Full Create, Read, Update, Delete functionality for employees and departments
- **Report Generation**: Generate summary reports and export to PDF or TXT format
- **Modern GUI**: Clean interface built with CustomTkinter
- **Input Validation**: Comprehensive validation for email, phone, salary, and dates
- **Search Functionality**: Search employees by name, email, or position

## Requirements

- Python 3.7 or higher
- Dependencies: `customtkinter`, `reportlab`, `mysql-connector-python` (for MySQL)

## Installation

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install customtkinter reportlab mysql-connector-python
```

### Step 2: Setup MySQL Database

1. **Install and start MySQL** (AppServ, Standalone MySQL, or MySQL Workbench)

2. **Create database** using one of these methods:
   - **phpMyAdmin**: Navigate to `http://localhost/phpmyadmin`, click "New", enter `smart_records`, click "Create"
   - **Command Line**: `mysql -u root -p` then `CREATE DATABASE smart_records CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`
   - **MySQL Workbench**: Create new schema named `smart_records`

3. **Configure application**:
   Create `db_config.py` file in the project root with the following content:
   ```python
   MYSQL_CONFIG = {
       'host': 'localhost',
       'port': 3306,
       'user': 'root',
       'password': 'YOUR_PASSWORD',
       'database': 'smart_records'
   }
   ```

### Step 3: Run Application

```bash
python main.py
```

## Default Login

- **Username**: `admin`
- **Password**: `admin123`

> Change the default password after first login!

## Usage

### Employee Management
- **Add Employee**: Employees → Add Employee (fill required fields: First Name, Last Name, Email)
- **View All**: Employees → View All Employees
- **Search**: Employees → Search Employees (enter search term)
- **Update**: Employees → Update Employee (select from dropdown, edit fields)
- **Delete**: Employees → Delete Employee (select from dropdown, confirm)

### Department Management
- **Add Department**: Departments → Add Department (name required)
- **View All**: Departments → View All Departments
- **Update**: Departments → Update Department (select from dropdown, edit)
- **Delete**: Departments → Delete Department (select from dropdown, confirm)

### Reports
- **View Reports**: Reports → View Reports (shows statistics and listings)
- **Export**: Click "Export to TXT" or "Export to PDF" (PDF requires `reportlab`)

## Project Structure

```
Python Project/
├── main.py                    # Application entry point
├── requirements.txt          # Dependencies
├── db_config.py              # Database configuration
├── database/                 # Database layer
├── gui/                      # User interface
├── auth/                     # Authentication
├── reports/                  # Report generation
└── utils/                    # Utilities
```

## Database Schema

**Users**: id, username, password (hashed), created_at  
**Departments**: id, name, description, created_at  
**Employees**: id, first_name, last_name, email, phone, position, salary, department_id (FK), hire_date, created_at

## Troubleshooting

**Application won't start**: Install dependencies with `pip install -r requirements.txt`

**MySQL connection failed**: 
- Verify MySQL service is running
- Check credentials in `db_config.py`
- Ensure database `smart_records` exists

**PDF export fails**: Install `reportlab` with `pip install reportlab`

**Login issues**: Use default credentials `admin` / `admin123` (case-sensitive)

## System Requirements

- Python 3.7+
- Windows, macOS, or Linux
- ~50MB disk space