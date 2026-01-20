"""
Database Manager - Smart Records System

This module handles all database operations including:
- Connecting to MySQL database
- Creating database tables (if they don't exist)
- Executing SQL queries (SELECT, INSERT, UPDATE, DELETE)
- Managing database connections

Think of this as a "translator" between Python code and MySQL database.
"""

# Import hashlib - used for hashing passwords (creating default admin user)
import hashlib

# Try to import MySQL connector library
# This is a try/except block - if the library isn't installed, we catch the error
try:
    # Import mysql.connector - the official MySQL driver for Python
    # This library allows Python to communicate with MySQL databases
    import mysql.connector
    
    # Import Error class - used to catch MySQL-specific errors
    from mysql.connector import Error
    
    # Set flag to True - MySQL connector is available
    MYSQL_AVAILABLE = True
except ImportError:
    # If import fails (library not installed), set flag to False
    # This allows us to check later and show helpful error messages
    MYSQL_AVAILABLE = False


class DatabaseManager:
    """
    Database Manager Class
    
    This class manages all database operations for the Smart Records System.
    It handles connections, table creation, and query execution.
    
    Think of this as a "database assistant" that handles all the technical
    database stuff so other parts of the code don't have to worry about it.
    """
    
    def __init__(self, mysql_config=None):
        """
        Initialize the database manager.
        
        Args:
            mysql_config (dict, optional): Dictionary containing database connection settings
                                          If None, uses default values
        """
        # Initialize connection to None - no connection established yet
        # We'll create the connection when needed (lazy connection)
        self.connection = None
        
        # If no config provided, use empty dictionary
        # This prevents errors if mysql_config is None
        if mysql_config is None:
            mysql_config = {}
        
        # Store database configuration with defaults
        # .get() method safely gets a value from dictionary, uses default if key doesn't exist
        self.mysql_config = {
            # Database server address (localhost = same computer)
            'host': mysql_config.get('host', 'localhost'),
            
            # Database server port (3306 is MySQL default port)
            'port': mysql_config.get('port', 3306),
            
            # Database username (root is default admin account)
            'user': mysql_config.get('user', 'root'),
            
            # Database password (empty string if not provided)
            'password': mysql_config.get('password', ''),
            
            # Database name (smart_records is the default database name)
            'database': mysql_config.get('database', 'smart_records')
        }
        
        # Check if MySQL connector library is available
        # If not installed, raise an error with helpful message
        if not MYSQL_AVAILABLE:
            raise ImportError(
                "MySQL connector not available. Install it using: pip install mysql-connector-python"
            )
    
    def connect(self):
        """
        Establish connection to MySQL database.
        
        This uses "lazy connection" - only connects when needed.
        If connection already exists, returns the existing connection.
        
        Returns:
            mysql.connector.connection: Database connection object
            
        Raises:
            ImportError: If MySQL connector library is not installed
            ConnectionError: If connection to database fails
        """
        # Only create new connection if one doesn't exist
        # This prevents creating multiple connections unnecessarily
        if self.connection is None:
            # Double-check MySQL connector is available
            if not MYSQL_AVAILABLE:
                raise ImportError("mysql-connector-python is required for MySQL support")
            
            # Try to connect to database
            try:
                # mysql.connector.connect() creates a connection to MySQL database
                # We pass all the connection parameters from our config
                self.connection = mysql.connector.connect(
                    host=self.mysql_config['host'],      # Database server address
                    port=self.mysql_config['port'],      # Database server port
                    user=self.mysql_config['user'],      # Username
                    password=self.mysql_config['password'],  # Password
                    database=self.mysql_config['database']    # Database name
                )
            except Error as e:
                # If connection fails, raise a more user-friendly error
                # str(e) converts the MySQL error to a readable string
                raise ConnectionError(f"Failed to connect to MySQL: {str(e)}")
        
        # Return the connection (either newly created or existing)
        return self.connection
    
    def close(self):
        """
        Close the database connection.
        
        This should be called when the application exits to free up resources.
        It's good practice to always close database connections when done.
        """
        # Check if connection exists before trying to close it
        if self.connection:
            # Close the connection - releases resources and disconnects from database
            self.connection.close()
            
            # Set to None so we know connection is closed
            self.connection = None
    
    def initialize_database(self):
        """
        Initialize the database - Create all necessary tables if they don't exist.
        
        This method:
        1. Creates users, departments, and employees tables
        2. Creates default admin user if no users exist
        3. Creates sample departments and employees if database is empty
        
        This is called automatically when the application starts.
        """
        # Get database connection (creates connection if needed)
        conn = self.connect()
        
        # Create a cursor - cursor is like a "pointer" that executes SQL commands
        # cursor() creates a cursor object that can execute SQL queries
        cursor = conn.cursor()
        
        # Use try/finally to ensure cursor is always closed, even if errors occur
        try:
            # Create users table if it doesn't exist
            # CREATE TABLE IF NOT EXISTS - only creates if table doesn't already exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,  -- Unique ID, auto-increments
                    username VARCHAR(255) UNIQUE NOT NULL,  -- Username, must be unique
                    password VARCHAR(255) NOT NULL,          -- Hashed password
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- When account was created
                )
            """)
            
            # Create departments table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS departments (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,  -- Unique department ID
                    name VARCHAR(255) UNIQUE NOT NULL,      -- Department name, must be unique
                    description VARCHAR(255),                -- Optional description
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- When department was created
                )
            """)
            
            # Create employees table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,   -- Unique employee ID
                    first_name VARCHAR(255) NOT NULL,       -- Employee's first name
                    last_name VARCHAR(255) NOT NULL,        -- Employee's last name
                    email VARCHAR(255) UNIQUE NOT NULL,     -- Email, must be unique
                    phone VARCHAR(255),                      -- Phone number (optional)
                    position VARCHAR(255),                   -- Job position (optional)
                    salary DECIMAL(10,2),                    -- Salary (10 digits, 2 decimal places)
                    department_id INTEGER,                   -- Foreign key to departments table
                    hire_date DATE,                          -- Date employee was hired
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- When record was created
                    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL
                    -- Foreign key links employee to department
                    -- ON DELETE SET NULL means if department is deleted, employee's department_id becomes NULL
                ) ENGINE=InnoDB
                -- InnoDB engine supports foreign keys and transactions
            """)
            
            # Commit all the CREATE TABLE statements
            # commit() saves changes to database (makes them permanent)
            conn.commit()
            
            # Check if any users exist in the database
            # SELECT COUNT(*) counts how many rows are in the users table
            cursor.execute("SELECT COUNT(*) as count FROM users")
            
            # fetchone() gets the first (and only) row from the result
            result = cursor.fetchone()
            
            # Extract count from result
            # result[0] gets the first column value (the count)
            # If result is None, use 0 as default
            user_count = result[0] if result else 0
            
            # If no users exist, create default admin user
            if user_count == 0:
                # Hash the default password "admin123"
                # We hash it the same way AuthManager does (SHA-256)
                default_password = hashlib.sha256("admin123".encode()).hexdigest()
                
                # Insert default admin user into database
                # %s placeholders prevent SQL injection attacks
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", 
                             ("admin", default_password))
                
                # Commit the insert (save to database)
                conn.commit()
            
            # Check if any departments exist
            cursor.execute("SELECT COUNT(*) as count FROM departments")
            result = cursor.fetchone()
            dept_count = result[0] if result else 0
            
            # If no departments exist, create sample departments
            if dept_count == 0:
                # List of sample departments to create
                # Each tuple contains (name, description)
                sample_departments = [
                    ("Human Resources", "Manages employee relations, recruitment, and benefits"),
                    ("Information Technology", "Handles software development, infrastructure, and technical support"),
                    ("Sales", "Responsible for customer acquisition and revenue generation"),
                    ("Marketing", "Manages brand promotion, advertising, and market research"),
                    ("Finance", "Handles accounting, budgeting, and financial planning"),
                    ("Operations", "Manages daily operations and services"),
                    ("Quality Assurance", "Ensures quality standards and compliance monitoring"),
                    ("Research & Development", "Product development and innovation"),
                    ("Customer Service", "Customer support and service management"),
                    ("Executive Management", "Executive leadership and strategic planning")
                ]
                
                # Insert each department into database
                # Loop through each department tuple
                for dept_name, dept_desc in sample_departments:
                    # Insert department with name and description
                    cursor.execute("INSERT INTO departments (name, description) VALUES (%s, %s)", 
                                 (dept_name, dept_desc))
                
                # Commit all department inserts
                conn.commit()
                
                # Get all department IDs we just created
                # We need these to assign employees to departments
                cursor.execute("SELECT id FROM departments ORDER BY id")
                
                # fetchall() gets all rows from the result
                dept_rows = cursor.fetchall()
                
                # Extract department IDs from results
                dept_ids = []
                for row in dept_rows:
                    # Handle different result formats (tuple, list, or dict)
                    if isinstance(row, (list, tuple)):
                        # If row is tuple/list, get first element (the ID)
                        dept_ids.append(row[0])
                    elif isinstance(row, dict):
                        # If row is dict, get 'id' key
                        dept_ids.append(row.get('id'))
                    else:
                        # Otherwise, assume row itself is the ID
                        dept_ids.append(row)
                
                # List of sample employees to create
                # Each tuple contains: (first_name, last_name, email, phone, position, salary, department_id, hire_date)
                # department_id uses dept_ids list we just created
                sample_employees = [
                    ("Ahmed", "Mohammed", "ahmed.mohammed@company.com", "555-0101", "HR Manager", 85000.00, dept_ids[0] if len(dept_ids) > 0 else None, "2019-03-15"),
                    ("Fatima", "Ali", "fatima.ali@company.com", "555-0102", "Software Engineer", 90000.00, dept_ids[1] if len(dept_ids) > 1 else None, "2018-07-01"),
                    ("Khalid", "Hassan", "khalid.hassan@company.com", "555-0103", "Sales Representative", 65000.00, dept_ids[2] if len(dept_ids) > 2 else None, "2020-05-10"),
                    ("Mariam", "Ibrahim", "mariam.ibrahim@company.com", "555-0104", "Marketing Specialist", 70000.00, dept_ids[3] if len(dept_ids) > 3 else None, "2020-11-20"),
                    ("Youssef", "Abdullah", "youssef.abdullah@company.com", "555-0105", "Financial Analyst", 75000.00, dept_ids[4] if len(dept_ids) > 4 else None, "2021-02-05"),
                    ("Sara", "Ahmed", "sara.ahmed@company.com", "555-0106", "Senior Developer", 100000.00, dept_ids[1] if len(dept_ids) > 1 else None, "2017-09-12"),
                    ("Omar", "Mahmoud", "omar.mahmoud@company.com", "555-0107", "Sales Manager", 85000.00, dept_ids[2] if len(dept_ids) > 2 else None, "2019-06-18"),
                    ("Nora", "Saeed", "nora.saeed@company.com", "555-0108", "HR Coordinator", 60000.00, dept_ids[0] if len(dept_ids) > 0 else None, "2022-03-14"),
                    ("Abdulrahman", "Ali", "abdulrahman.ali@company.com", "555-0109", "Operations Manager", 95000.00, dept_ids[5] if len(dept_ids) > 5 else None, "2018-04-22"),
                    ("Layla", "Mohammed", "layla.mohammed@company.com", "555-0110", "Quality Specialist", 72000.00, dept_ids[6] if len(dept_ids) > 6 else None, "2020-08-30"),
                    ("Tariq", "Hussein", "tariq.hussein@company.com", "555-0111", "Development Engineer", 88000.00, dept_ids[7] if len(dept_ids) > 7 else None, "2019-12-10"),
                    ("Zeinab", "Omar", "zeinab.omar@company.com", "555-0112", "Customer Service Specialist", 58000.00, dept_ids[8] if len(dept_ids) > 8 else None, "2021-07-25"),
                    ("Mustafa", "Ahmed", "mustafa.ahmed@company.com", "555-0113", "Development Manager", 110000.00, dept_ids[7] if len(dept_ids) > 7 else None, "2016-11-05"),
                    ("Hind", "Khalid", "hind.khalid@company.com", "555-0114", "Marketing Manager", 92000.00, dept_ids[3] if len(dept_ids) > 3 else None, "2018-09-15"),
                    ("Salem", "Abdullah", "salem.abdullah@company.com", "555-0115", "Accountant", 68000.00, dept_ids[4] if len(dept_ids) > 4 else None, "2020-01-20"),
                    ("Nasser", "Ali", "nasser.ali@company.com", "555-0116", "Senior Sales Representative", 72000.00, dept_ids[2] if len(dept_ids) > 2 else None, "2019-10-12"),
                    ("Reem", "Hassan", "reem.hassan@company.com", "555-0118", "HR Specialist", 64000.00, dept_ids[0] if len(dept_ids) > 0 else None, "2021-04-18"),
                    ("Waleed", "Ibrahim", "waleed.ibrahim@company.com", "555-0119", "Quality Manager", 89000.00, dept_ids[6] if len(dept_ids) > 6 else None, "2018-02-28"),
                    ("Dana", "Mahmoud", "dana.mahmoud@company.com", "555-0120", "Service Manager", 78000.00, dept_ids[8] if len(dept_ids) > 8 else None, "2020-06-14"),
                    ("Badr", "Saeed", "badr.saeed@company.com", "555-0121", "Software Engineer", 82000.00, dept_ids[1] if len(dept_ids) > 1 else None, "2019-08-22"),
                    ("Lina", "Hussein", "lina.hussein@company.com", "555-0122", "Senior Financial Analyst", 80000.00, dept_ids[4] if len(dept_ids) > 4 else None, "2018-12-05"),
                    ("Abdullah", "Omar", "abdullah.omar@company.com", "555-0123", "Executive Manager", 120000.00, dept_ids[9] if len(dept_ids) > 9 else None, "2015-03-10"),
                    ("Mona", "Ahmed", "mona.ahmed@company.com", "555-0124", "Development Specialist", 76000.00, dept_ids[7] if len(dept_ids) > 7 else None, "2020-10-30"),
                    ("Faisal", "Khalid", "faisal.khalid@company.com", "555-0125", "Regional Sales Manager", 98000.00, dept_ids[2] if len(dept_ids) > 2 else None, "2017-07-20")
                ]
                
                # Insert each employee into database
                for emp in sample_employees:
                    # Insert employee with all fields
                    # The tuple emp contains all 8 values in order
                    cursor.execute("""INSERT INTO employees (first_name, last_name, email, phone, position, salary, department_id, hire_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", emp)
                
                # Commit all employee inserts
                conn.commit()
        finally:
            # Always close cursor, even if errors occurred
            # This ensures resources are freed
            cursor.close()
    
    def execute_query(self, query, params=()):
        """
        Execute a SELECT query and return results.
        
        This method is used for reading data from the database.
        It returns results as a list of dictionaries (one dict per row).
        
        Args:
            query (str): SQL SELECT query string
            params (tuple): Parameters to substitute for %s placeholders in query
                          Prevents SQL injection attacks
                          
        Returns:
            list: List of dictionaries, where each dict represents one row
                  Keys are column names, values are column values
                  
        Example:
            results = db.execute_query("SELECT * FROM employees WHERE id = %s", (1,))
            # Returns: [{'id': 1, 'first_name': 'John', 'last_name': 'Doe', ...}]
        """
        # Get database connection
        conn = self.connect()
        
        # Create cursor with dictionary=True
        # This makes results return as dictionaries instead of tuples
        cursor = conn.cursor(dictionary=True)
        
        try:
            # Execute the SQL query
            # params tuple fills in the %s placeholders safely
            cursor.execute(query, params)
            
            # Fetch all results from the query
            # fetchall() gets all rows returned by the query
            rows = cursor.fetchall()
            
            # Convert to list and return
            # list() ensures we return a proper list
            return list(rows)
        finally:
            # Always close cursor to free resources
            cursor.close()
    
    def execute_update(self, query, params=()):
        """
        Execute INSERT, UPDATE, or DELETE query.
        
        This method is used for modifying data in the database.
        It automatically commits changes (makes them permanent).
        
        Args:
            query (str): SQL INSERT, UPDATE, or DELETE query string
            params (tuple): Parameters to substitute for %s placeholders
            
        Returns:
            int: Number of rows affected by the query
            
        Example:
            rows_affected = db.execute_update(
                "UPDATE employees SET salary = %s WHERE id = %s",
                (50000, 1)
            )
        """
        # Get database connection
        conn = self.connect()
        
        # Create cursor (regular cursor, not dictionary mode)
        cursor = conn.cursor()
        
        try:
            # Execute the SQL query
            cursor.execute(query, params)
            
            # Commit changes to database (make them permanent)
            # Without commit(), changes would be lost when connection closes
            conn.commit()
            
            # Return number of rows affected
            # rowcount tells us how many rows were inserted/updated/deleted
            return cursor.rowcount
        finally:
            # Always close cursor
            cursor.close()
    
    def get_last_insert_id(self):
        """
        Get the ID of the last inserted row.
        
        This is useful after INSERT queries to know what ID was assigned
        to the new record (since IDs are auto-incremented).
        
        Returns:
            int: The ID of the last inserted row, or None if no insert occurred
            
        Example:
            db.execute_update("INSERT INTO employees (...) VALUES (...)")
            new_id = db.get_last_insert_id()  # Gets the new employee's ID
        """
        # Get database connection
        conn = self.connect()
        
        # Create cursor
        cursor = conn.cursor()
        
        try:
            # Return the ID of the last inserted row
            # lastrowid is a property of the cursor that contains the last auto-generated ID
            return cursor.lastrowid
        finally:
            # Always close cursor
            cursor.close()
