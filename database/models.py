"""Database models and CRUD operations."""

from .db_manager import DatabaseManager


class DepartmentModel:
    """Model for department operations."""
    
    def __init__(self, db_manager):
        """Initialize department model."""
        self.db = db_manager
    
    def create(self, name, description=""):
        """Create a new department. Returns department ID."""
        self.db.execute_update(
            "INSERT INTO departments (name, description) VALUES (%s, %s)",
            (name, description)
        )
        return self.db.get_last_insert_id()
    
    def get_all(self):
        """Get all departments."""
        return self.db.execute_query("SELECT * FROM departments ORDER BY name")
    
    def get_by_id(self, dept_id):
        """Get department by ID. Returns department dict or None."""
        results = self.db.execute_query(
            "SELECT * FROM departments WHERE id = %s",
            (dept_id,)
        )
        return results[0] if results else None
    
    def update(self, dept_id, name, description=""):
        """Update department. Returns True if successful."""
        rows_affected = self.db.execute_update(
            "UPDATE departments SET name = %s, description = %s WHERE id = %s",
            (name, description, dept_id)
        )
        return rows_affected > 0
    
    def delete(self, dept_id):
        """Delete department. Returns True if successful."""
        rows_affected = self.db.execute_update(
            "DELETE FROM departments WHERE id = %s",
            (dept_id,)
        )
        return rows_affected > 0
    
    def has_employees(self, dept_id):
        """Check if department has employees."""
        try:
            # Check employee count to prevent deletion of departments with active employees
            results = self.db.execute_query(
                "SELECT COUNT(*) as count FROM employees WHERE department_id = %s",
                (dept_id,)
            )
            if results and len(results) > 0:
                count = results[0].get('count', 0)
                return int(count) > 0 if count is not None else False
            return False
        except Exception:
            return False


class EmployeeModel:
    """Model for employee operations."""
    
    def __init__(self, db_manager):
        """Initialize employee model."""
        self.db = db_manager
    
    def create(self, first_name, last_name, email, phone="", position="", salary=0.0, department_id=None, hire_date=""):
        """Create new employee. Returns employee ID."""
        self.db.execute_update(
            """INSERT INTO employees 
               (first_name, last_name, email, phone, position, salary, department_id, hire_date)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (first_name, last_name, email, phone, position, salary, department_id, hire_date)
        )
        return self.db.get_last_insert_id()
    
    def get_all(self):
        """Get all employees with department information."""
        return self.db.execute_query("""
            SELECT e.*, d.name as department_name 
            FROM employees e
            LEFT JOIN departments d ON e.department_id = d.id
            ORDER BY e.last_name, e.first_name
        """)
    
    def get_by_id(self, emp_id):
        """Get employee by ID. Returns employee dict or None."""
        results = self.db.execute_query("""
            SELECT e.*, d.name as department_name 
            FROM employees e
            LEFT JOIN departments d ON e.department_id = d.id
            WHERE e.id = %s
        """, (emp_id,))
        return results[0] if results else None
    
    def search(self, search_term):
        """Search employees by name, email, or position."""
        search_pattern = f"%{search_term}%"
        return self.db.execute_query("""
            SELECT e.*, d.name as department_name 
            FROM employees e
            LEFT JOIN departments d ON e.department_id = d.id
            WHERE e.first_name LIKE %s OR e.last_name LIKE %s 
               OR e.email LIKE %s OR e.position LIKE %s
            ORDER BY e.last_name, e.first_name
        """, (search_pattern, search_pattern, search_pattern, search_pattern))
    
    def get_by_department(self, dept_id):
        """Get all employees in a specific department."""
        return self.db.execute_query("""
            SELECT e.*, d.name as department_name 
            FROM employees e
            LEFT JOIN departments d ON e.department_id = d.id
            WHERE e.department_id = %s
            ORDER BY e.last_name, e.first_name
        """, (dept_id,))
    
    def update(self, emp_id, first_name, last_name, email, phone="", position="", salary=0.0, department_id=None, hire_date=""):
        """Update employee. Returns True if successful."""
        rows_affected = self.db.execute_update(
            """UPDATE employees SET first_name = %s, last_name = %s, email = %s, phone = %s, 
               position = %s, salary = %s, department_id = %s, hire_date = %s WHERE id = %s""",
            (first_name, last_name, email, phone, position, salary, department_id, hire_date, emp_id)
        )
        return rows_affected > 0
    
    def delete(self, emp_id):
        """Delete employee. Returns True if successful."""
        rows_affected = self.db.execute_update("DELETE FROM employees WHERE id = %s", (emp_id,))
        return rows_affected > 0
    
    def get_statistics(self):
        """Get employee statistics (total, avg_salary, etc.)."""
        try:
            results = self.db.execute_query("""
                SELECT 
                    COUNT(*) as total_employees,
                    AVG(salary) as avg_salary,
                    MIN(salary) as min_salary,
                    MAX(salary) as max_salary,
                    SUM(salary) as total_salary
                FROM employees
            """)
            if results and len(results) > 0:
                return results[0]
            else:
                return {
                    'total_employees': 0,
                    'avg_salary': 0,
                    'min_salary': 0,
                    'max_salary': 0,
                    'total_salary': 0
                }
        except Exception:
            return {
                'total_employees': 0,
                'avg_salary': 0,
                'min_salary': 0,
                'max_salary': 0,
                'total_salary': 0
            }

