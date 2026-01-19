"""Database connection and initialization manager."""

import hashlib

try:
    import mysql.connector
    from mysql.connector import Error
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False


class DatabaseManager:
    """Manages MySQL database connection and initialization."""
    
    def __init__(self, mysql_config=None):
        """Initialize database manager."""
        self.connection = None
        
        if mysql_config is None:
            mysql_config = {}
        self.mysql_config = {
            'host': mysql_config.get('host', 'localhost'),
            'port': mysql_config.get('port', 3306),
            'user': mysql_config.get('user', 'root'),
            'password': mysql_config.get('password', ''),
            'database': mysql_config.get('database', 'smart_records')
        }
        
        if not MYSQL_AVAILABLE:
            raise ImportError(
                "MySQL connector not available. Install it using: pip install mysql-connector-python"
            )
    
    def connect(self):
        """Establish database connection."""
        if self.connection is None:
            if not MYSQL_AVAILABLE:
                raise ImportError("mysql-connector-python is required for MySQL support")
            try:
                self.connection = mysql.connector.connect(
                    host=self.mysql_config['host'],
                    port=self.mysql_config['port'],
                    user=self.mysql_config['user'],
                    password=self.mysql_config['password'],
                    database=self.mysql_config['database']
                )
            except Error as e:
                raise ConnectionError(f"Failed to connect to MySQL: {str(e)}")
        return self.connection
    
    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def initialize_database(self):
        """Create all necessary tables if they don't exist."""
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    username VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS departments (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(255) UNIQUE NOT NULL,
                    description VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    first_name VARCHAR(255) NOT NULL,
                    last_name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    phone VARCHAR(255),
                    position VARCHAR(255),
                    salary DECIMAL(10,2),
                    department_id INTEGER,
                    hire_date DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL
                ) ENGINE=InnoDB
            """)
            
            conn.commit()
            
            cursor.execute("SELECT COUNT(*) as count FROM users")
            result = cursor.fetchone()
            user_count = result[0] if result else 0
            if user_count == 0:
                default_password = hashlib.sha256("admin123".encode()).hexdigest()
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", ("admin", default_password))
                conn.commit()
            
            cursor.execute("SELECT COUNT(*) as count FROM departments")
            result = cursor.fetchone()
            dept_count = result[0] if result else 0
            if dept_count == 0:
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
                
                for dept_name, dept_desc in sample_departments:
                    cursor.execute("INSERT INTO departments (name, description) VALUES (%s, %s)", (dept_name, dept_desc))
                
                conn.commit()
                
                # MySQL cursor returns tuples by default, but we handle dict/list formats for compatibility
                cursor.execute("SELECT id FROM departments ORDER BY id")
                dept_rows = cursor.fetchall()
                dept_ids = []
                for row in dept_rows:
                    if isinstance(row, (list, tuple)):
                        dept_ids.append(row[0])
                    elif isinstance(row, dict):
                        dept_ids.append(row.get('id'))
                    else:
                        dept_ids.append(row)
                
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
                
                for emp in sample_employees:
                    cursor.execute("""INSERT INTO employees (first_name, last_name, email, phone, position, salary, department_id, hire_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", emp)
                
                conn.commit()
        finally:
            cursor.close()
    
    def execute_query(self, query, params=()):
        """Execute SELECT query and return results as list of dictionaries."""
        conn = self.connect()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return list(rows)
        finally:
            cursor.close()
    
    def execute_update(self, query, params=()):
        """Execute INSERT, UPDATE, or DELETE query. Returns number of affected rows."""
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
    
    def get_last_insert_id(self):
        """Get the ID of the last inserted row."""
        conn = self.connect()
        cursor = conn.cursor()
        try:
            return cursor.lastrowid
        finally:
            cursor.close()
