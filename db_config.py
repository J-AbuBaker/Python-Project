"""
Database Configuration File - Smart Records System

This file contains the database connection settings. You MUST edit this file
with your MySQL database credentials before running the application.

IMPORTANT: Never commit this file to version control with real passwords!
This file should be kept private and secure.
"""

# MySQL Configuration Dictionary
# This dictionary contains all the information needed to connect to your MySQL database
# Think of it as a "key" that unlocks your database
MYSQL_CONFIG = {
    # 'host': The address where your MySQL server is running
    # 'localhost' means the database is on the same computer as this application
    # If your database is on another computer, use that computer's IP address or hostname
    'host': 'localhost',      # MySQL server hostname
    
    # 'port': The port number MySQL is listening on
    # Port 3306 is the default MySQL port (like a door number for the database)
    'port': 3306,              # MySQL server port (default: 3306)
    
    # 'user': Your MySQL username
    # This is the account name you use to log into MySQL
    # 'root' is the default administrator account, but you can create other users
    'user': 'root',            # MySQL username
    
    # 'password': Your MySQL password
    # This is the password for the MySQL user account specified above
    # CHANGE THIS to your actual MySQL password!
    # Example: 'password': 'MySecurePassword123'
    'password': '12345678',    # MySQL password - CHANGE THIS!
    
    # 'database': The name of the database to use
    # This is the specific database where all your data will be stored
    # The application will create this database if it doesn't exist (if you have permissions)
    'database': 'smart_records'  # Database name
}

# HOW TO SET UP:
# 1. Make sure MySQL is installed and running on your computer
# 2. Open MySQL command line or MySQL Workbench
# 3. Create the database: CREATE DATABASE smart_records;
# 4. Note your MySQL username and password
# 5. Edit this file and replace 'password' with your actual MySQL password
# 6. Save this file
# 7. Run the application - it will create all necessary tables automatically
