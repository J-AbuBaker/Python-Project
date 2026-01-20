"""
Database Models - Smart Records System

This module contains model classes that handle CRUD (Create, Read, Update, Delete)
operations for employees and departments. These classes act as an interface between
the GUI and the database, making it easy to work with data.

Think of models as "helpers" that know how to save, load, update, and delete
data from the database. The GUI code doesn't need to know SQL - it just calls
these model methods.
"""

# Import DatabaseManager - we need this to execute database queries
# The dot (.) means "from the same package" (database package)
from .db_manager import DatabaseManager


class DepartmentModel:
    """
    Department Model Class
    
    This class handles all operations related to departments:
    - Creating new departments
    - Reading/listing departments
    - Updating department information
    - Deleting departments
    - Checking if a department has employees
    
    Think of this as a "department manager" that knows how to work with department data.
    """
    
    def __init__(self, db_manager):
        """
        Initialize the department model.
        
        Args:
            db_manager: DatabaseManager instance - used to execute database queries
        """
        # Store reference to database manager
        # This allows us to use db_manager.execute_query() and db_manager.execute_update()
        self.db = db_manager
    
    def create(self, name, description=""):
        """
        Create a new department in the database.
        
        Args:
            name (str): Department name (required, must be unique)
            description (str): Optional department description
            
        Returns:
            int: The ID of the newly created department
            
        Example:
            dept_id = department_model.create("IT", "Information Technology Department")
        """
        # Execute INSERT query to create new department
        # execute_update() is used for INSERT, UPDATE, DELETE queries
        # %s placeholders are filled with the values from the tuple (name, description)
        self.db.execute_update(
            "INSERT INTO departments (name, description) VALUES (%s, %s)",
            (name, description)  # Tuple of values to insert
        )
        
        # Return the ID of the department we just created
        # get_last_insert_id() gets the auto-generated ID from the last INSERT
        return self.db.get_last_insert_id()
    
    def get_all(self):
        """
        Get all departments from the database.
        
        Returns:
            list: List of dictionaries, each representing one department
                  Format: [{'id': 1, 'name': 'IT', 'description': '...', ...}, ...]
        """
        # Execute SELECT query to get all departments
        # execute_query() is used for SELECT queries (reading data)
        # ORDER BY name sorts departments alphabetically by name
        return self.db.execute_query("SELECT * FROM departments ORDER BY name")
    
    def get_by_id(self, dept_id):
        """
        Get a specific department by its ID.
        
        Args:
            dept_id (int): The ID of the department to retrieve
            
        Returns:
            dict or None: Department dictionary if found, None if not found
        """
        # Query database for department with matching ID
        # WHERE id = %s filters to only the department with the specified ID
        results = self.db.execute_query(
            "SELECT * FROM departments WHERE id = %s",
            (dept_id,)  # Note: (dept_id,) is a tuple with one element
                        # The comma is required to make it a tuple, not just parentheses
        )
        
        # Return first result if found, None if not found
        # results[0] gets the first (and should be only) department
        # If results is empty, return None
        return results[0] if results else None
    
    def update(self, dept_id, name, description=""):
        """
        Update an existing department's information.
        
        Args:
            dept_id (int): ID of the department to update
            name (str): New department name
            description (str): New department description
            
        Returns:
            bool: True if update was successful (department was found and updated),
                  False if department wasn't found
        """
        # Execute UPDATE query
        # SET name = %s, description = %s updates those fields
        # WHERE id = %s specifies which department to update
        rows_affected = self.db.execute_update(
            "UPDATE departments SET name = %s, description = %s WHERE id = %s",
            (name, description, dept_id)  # Values in order: name, description, dept_id
        )
        
        # Return True if at least one row was updated
        # rows_affected > 0 means the department was found and updated
        return rows_affected > 0
    
    def delete(self, dept_id):
        """
        Delete a department from the database.
        
        Note: If the department has employees, their department_id will be set to NULL
        (due to foreign key constraint ON DELETE SET NULL).
        
        Args:
            dept_id (int): ID of the department to delete
            
        Returns:
            bool: True if deletion was successful, False if department wasn't found
        """
        # Execute DELETE query
        # WHERE id = %s specifies which department to delete
        rows_affected = self.db.execute_update(
            "DELETE FROM departments WHERE id = %s",
            (dept_id,)
        )
        
        # Return True if at least one row was deleted
        return rows_affected > 0
    
    def has_employees(self, dept_id):
        """
        Check if a department has any employees assigned to it.
        
        This is useful before deleting a department - you might want to warn the user
        if employees will be affected.
        
        Args:
            dept_id (int): ID of the department to check
            
        Returns:
            bool: True if department has employees, False otherwise
        """
        try:
            # Count how many employees belong to this department
            # COUNT(*) counts all rows that match the WHERE condition
            # as count gives the result column a name
            results = self.db.execute_query(
                "SELECT COUNT(*) as count FROM employees WHERE department_id = %s",
                (dept_id,)
            )
            
            # Check if we got results and extract the count
            if results and len(results) > 0:
                # Get the count value from the first (and only) result
                # .get('count', 0) safely gets 'count' key, uses 0 as default
                count = results[0].get('count', 0)
                
                # Convert to int and check if greater than 0
                # int(count) converts to integer (in case it's a string or decimal)
                # Return True if count > 0, False otherwise
                return int(count) > 0 if count is not None else False
            
            # If no results, return False
            return False
        except Exception:
            # If anything goes wrong (database error, etc.), return False
            # This is a "safe" default - better to say "no employees" than crash
            return False


class EmployeeModel:
    """
    Employee Model Class
    
    This class handles all operations related to employees:
    - Creating new employees
    - Reading/listing employees
    - Searching employees
    - Updating employee information
    - Deleting employees
    - Getting employee statistics
    
    Think of this as an "employee manager" that knows how to work with employee data.
    """
    
    def __init__(self, db_manager):
        """
        Initialize the employee model.
        
        Args:
            db_manager: DatabaseManager instance - used to execute database queries
        """
        # Store reference to database manager
        self.db = db_manager
    
    def create(self, first_name, last_name, email, phone="", position="", salary=0.0, department_id=None, hire_date=""):
        """
        Create a new employee in the database.
        
        Args:
            first_name (str): Employee's first name (required)
            last_name (str): Employee's last name (required)
            email (str): Employee's email address (required, must be unique)
            phone (str): Employee's phone number (optional)
            position (str): Employee's job position (optional)
            salary (float): Employee's salary (optional, defaults to 0.0)
            department_id (int): ID of the department employee belongs to (optional)
            hire_date (str): Date employee was hired, format YYYY-MM-DD (optional)
            
        Returns:
            int: The ID of the newly created employee
        """
        # Execute INSERT query to create new employee
        # Multi-line string makes the SQL query more readable
        # All 8 fields are inserted: first_name through hire_date
        self.db.execute_update(
            """INSERT INTO employees 
               (first_name, last_name, email, phone, position, salary, department_id, hire_date)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (first_name, last_name, email, phone, position, salary, department_id, hire_date)
        )
        
        # Return the ID of the employee we just created
        return self.db.get_last_insert_id()
    
    def get_all(self):
        """
        Get all employees from the database, including their department names.
        
        This uses a JOIN query to combine employee data with department data.
        
        Returns:
            list: List of dictionaries, each representing one employee
                  Each dict includes employee fields plus 'department_name'
        """
        # Execute SELECT query with JOIN
        # e.* means "all columns from employees table" (e is alias for employees)
        # d.name as department_name gets department name and calls it 'department_name'
        # LEFT JOIN means include employees even if they don't have a department
        # ORDER BY sorts employees by last name, then first name
        return self.db.execute_query("""
            SELECT e.*, d.name as department_name 
            FROM employees e
            LEFT JOIN departments d ON e.department_id = d.id
            ORDER BY e.last_name, e.first_name
        """)
    
    def get_by_id(self, emp_id):
        """
        Get a specific employee by their ID.
        
        Args:
            emp_id (int): The ID of the employee to retrieve
            
        Returns:
            dict or None: Employee dictionary if found, None if not found
        """
        # Query database for employee with matching ID
        # Includes department name via JOIN
        results = self.db.execute_query("""
            SELECT e.*, d.name as department_name 
            FROM employees e
            LEFT JOIN departments d ON e.department_id = d.id
            WHERE e.id = %s
        """, (emp_id,))
        
        # Return first result if found, None if not found
        return results[0] if results else None
    
    def search(self, search_term):
        """
        Search for employees by name, email, or position.
        
        This performs a "fuzzy" search - it finds employees whose name, email,
        or position contains the search term (case-insensitive).
        
        Args:
            search_term (str): The text to search for
            
        Returns:
            list: List of employee dictionaries matching the search term
        """
        # Create search pattern with wildcards
        # % is SQL wildcard meaning "any characters"
        # f"%{search_term}%" creates pattern like "%john%" which matches "john", "johnson", etc.
        search_pattern = f"%{search_term}%"
        
        # Execute SELECT query with LIKE conditions
        # LIKE performs pattern matching (similar to "contains")
        # OR means match if ANY of the conditions are true
        # We search in first_name, last_name, email, and position fields
        return self.db.execute_query("""
            SELECT e.*, d.name as department_name 
            FROM employees e
            LEFT JOIN departments d ON e.department_id = d.id
            WHERE e.first_name LIKE %s OR e.last_name LIKE %s 
               OR e.email LIKE %s OR e.position LIKE %s
            ORDER BY e.last_name, e.first_name
        """, (search_pattern, search_pattern, search_pattern, search_pattern))
        # Note: We pass search_pattern 4 times (once for each LIKE condition)
    
    def get_by_department(self, dept_id):
        """
        Get all employees in a specific department.
        
        Args:
            dept_id (int): ID of the department
            
        Returns:
            list: List of employee dictionaries in that department
        """
        # Query employees filtered by department_id
        # WHERE e.department_id = %s filters to only employees in specified department
        return self.db.execute_query("""
            SELECT e.*, d.name as department_name 
            FROM employees e
            LEFT JOIN departments d ON e.department_id = d.id
            WHERE e.department_id = %s
            ORDER BY e.last_name, e.first_name
        """, (dept_id,))
    
    def update(self, emp_id, first_name, last_name, email, phone="", position="", salary=0.0, department_id=None, hire_date=""):
        """
        Update an existing employee's information.
        
        Args:
            emp_id (int): ID of the employee to update
            first_name (str): Updated first name
            last_name (str): Updated last name
            email (str): Updated email address
            phone (str): Updated phone number
            position (str): Updated position
            salary (float): Updated salary
            department_id (int): Updated department ID
            hire_date (str): Updated hire date
            
        Returns:
            bool: True if update was successful, False if employee wasn't found
        """
        # Execute UPDATE query
        # SET updates all the specified fields
        # WHERE id = %s specifies which employee to update
        rows_affected = self.db.execute_update(
            """UPDATE employees SET first_name = %s, last_name = %s, email = %s, phone = %s, 
               position = %s, salary = %s, department_id = %s, hire_date = %s WHERE id = %s""",
            (first_name, last_name, email, phone, position, salary, department_id, hire_date, emp_id)
            # Note: emp_id is last in the tuple (matches WHERE id = %s at end of query)
        )
        
        # Return True if at least one row was updated
        return rows_affected > 0
    
    def delete(self, emp_id):
        """
        Delete an employee from the database.
        
        Args:
            emp_id (int): ID of the employee to delete
            
        Returns:
            bool: True if deletion was successful, False if employee wasn't found
        """
        # Execute DELETE query
        rows_affected = self.db.execute_update("DELETE FROM employees WHERE id = %s", (emp_id,))
        
        # Return True if at least one row was deleted
        return rows_affected > 0
    
    def get_statistics(self):
        """
        Get statistical information about all employees.
        
        This calculates:
        - Total number of employees
        - Average salary
        - Minimum salary
        - Maximum salary
        - Total salary budget
        
        Returns:
            dict: Dictionary with statistics:
                  {
                      'total_employees': int,
                      'avg_salary': float,
                      'min_salary': float,
                      'max_salary': float,
                      'total_salary': float
                  }
        """
        try:
            # Execute SELECT query with aggregate functions
            # COUNT(*) counts total rows (employees)
            # AVG(salary) calculates average salary
            # MIN(salary) finds minimum salary
            # MAX(salary) finds maximum salary
            # SUM(salary) calculates total of all salaries
            results = self.db.execute_query("""
                SELECT 
                    COUNT(*) as total_employees,
                    AVG(salary) as avg_salary,
                    MIN(salary) as min_salary,
                    MAX(salary) as max_salary,
                    SUM(salary) as total_salary
                FROM employees
            """)
            
            # Check if we got results
            if results and len(results) > 0:
                # Return the first (and only) result
                # This contains all the statistics
                return results[0]
            else:
                # If no results (no employees), return zeros
                return {
                    'total_employees': 0,
                    'avg_salary': 0,
                    'min_salary': 0,
                    'max_salary': 0,
                    'total_salary': 0
                }
        except Exception:
            # If anything goes wrong (database error, etc.), return zeros
            # This prevents crashes and provides safe defaults
            return {
                'total_employees': 0,
                'avg_salary': 0,
                'min_salary': 0,
                'max_salary': 0,
                'total_salary': 0
            }
