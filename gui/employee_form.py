"""
Employee Management Forms - Smart Records System

This module creates forms for managing employees. It supports multiple "modes":
- add: Form to add new employees
- view: Table showing all employees
- update: Form to update existing employees
- delete: Interface to delete employees
- search: Search interface with results table

GUI CONCEPTS EXPLAINED:
- CTkScrollableFrame: Frame that can scroll if content is too large
- CTkEntry: Text input field
- CTkComboBox: Dropdown selection box
- ttk.Treeview: Table widget for displaying data in rows/columns
- StringVar: Variable that tracks text value (used with ComboBox)
- grid() layout: Positions widgets in rows and columns
- pack() layout: Positions widgets sequentially
"""

# Import CustomTkinter for modern GUI widgets
import customtkinter as ctk

# Import tkinter for StringVar and Treeview
import tkinter as tk

# Import ttk (themed tkinter) for Treeview widget (data table)
# Import messagebox for popup dialogs
from tkinter import ttk, messagebox

# Import validation functions from utils
# These check if user input is valid before saving
from utils.validators import (
    validate_email,      # Check email format
    validate_phone,      # Check phone format
    validate_required,   # Check if field is not empty
    validate_salary,     # Check if salary is valid number
    validate_date        # Check if date format is correct
)


class EmployeeForm(ctk.CTkScrollableFrame):
    """
    Employee Form Class - Handles All Employee Operations
    
    This class inherits from CTkScrollableFrame, which means:
    - It can scroll if content is larger than visible area
    - It's a container that can hold other widgets
    
    The form works in different "modes" based on what the user wants to do:
    - "add": Show form to add new employee
    - "view": Show table of all employees
    - "update": Show form to update existing employee
    - "delete": Show interface to delete employee
    - "search": Show search box and results table
    """
    
    def __init__(self, parent, employee_model, department_model, mode="view"):
        """
        Initialize employee form.
        
        Args:
            parent: Parent widget (usually content_frame from MainWindow)
            employee_model: EmployeeModel instance - handles employee data operations
            department_model: DepartmentModel instance - loads departments for dropdown
            mode: Form mode string - determines what interface to show
                 Options: 'add', 'view', 'update', 'delete', 'search'
        """
        # Call parent class constructor
        # super() refers to CTkScrollableFrame parent class
        # This initializes the scrollable frame
        super().__init__(parent)
        
        # Store references to models
        # These are used to save/load employee and department data
        self.employee_model = employee_model
        self.department_model = department_model
        
        # Store form mode
        # This determines which interface to display
        self.mode = mode
        
        # Create widgets based on mode
        # This calls the appropriate method to create the interface
        self.create_widgets()
        
        # If mode is "view", load employees immediately
        # This displays the employee table right away
        if mode == "view":
            self.load_employees()
        # If mode is "search", show search interface
        elif mode == "search":
            self.show_search_interface()
    
    def create_widgets(self):
        """
        Create form widgets based on current mode.
        
        This method acts as a router - it calls the appropriate method
        based on the form mode to create the correct interface.
        """
        # Check mode and call appropriate method
        if self.mode == "add":
            # Create form for adding new employees
            self.create_add_form()
        elif self.mode == "update":
            # Create form for updating existing employees
            self.create_update_form()
        elif self.mode == "delete":
            # Create interface for deleting employees
            self.create_delete_form()
        elif self.mode == "view":
            # Create table view of all employees
            self.create_view_list()
        elif self.mode == "search":
            # Search interface is created in show_search_interface()
            # (called in __init__), so we don't need to do anything here
            pass
    
    def create_add_form(self):
        """
        Create form for adding new employees.
        
        This method creates:
        - Input fields for all employee data (name, email, phone, etc.)
        - Department dropdown (loaded from database)
        - Add and Clear buttons
        
        The form uses grid() layout manager for organized rows and columns.
        """
        # Create frame to contain the form
        # CTkFrame creates a container/widget group
        form_frame = ctk.CTkFrame(self)
        
        # Pack frame to fill available space
        # fill="both" fills horizontally and vertically
        # expand=True allows frame to grow
        # padx=20, pady=20 adds padding around frame
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create title label
        # grid() positions widget in a grid (rows and columns)
        # row=0, column=0 means first row, first column
        # columnspan=2 means it spans 2 columns (full width)
        # pady=10 adds vertical padding
        ctk.CTkLabel(
            form_frame, 
            text="Add New Employee", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=10)
        
        # ========== FIRST NAME FIELD ==========
        # Create label for first name
        # sticky="w" aligns label to west (left side)
        ctk.CTkLabel(form_frame, text="First Name *:").grid(
            row=1, column=0, sticky="w", pady=5, padx=10
        )
        
        # Create input field for first name
        # CTkEntry creates a text input box
        # width=250 sets field width to 250 pixels
        # Store reference in self.first_name_entry so we can access it later
        self.first_name_entry = ctk.CTkEntry(form_frame, width=250)
        self.first_name_entry.grid(row=1, column=1, pady=5, padx=10)
        
        # ========== LAST NAME FIELD ==========
        ctk.CTkLabel(form_frame, text="Last Name *:").grid(
            row=2, column=0, sticky="w", pady=5, padx=10
        )
        self.last_name_entry = ctk.CTkEntry(form_frame, width=250)
        self.last_name_entry.grid(row=2, column=1, pady=5, padx=10)
        
        # ========== EMAIL FIELD ==========
        # Email is required (indicated by *)
        ctk.CTkLabel(form_frame, text="Email *:").grid(
            row=3, column=0, sticky="w", pady=5, padx=10
        )
        self.email_entry = ctk.CTkEntry(form_frame, width=250)
        self.email_entry.grid(row=3, column=1, pady=5, padx=10)
        
        # ========== PHONE FIELD ==========
        # Phone is optional (no *)
        ctk.CTkLabel(form_frame, text="Phone:").grid(
            row=4, column=0, sticky="w", pady=5, padx=10
        )
        self.phone_entry = ctk.CTkEntry(form_frame, width=250)
        self.phone_entry.grid(row=4, column=1, pady=5, padx=10)
        
        # ========== POSITION FIELD ==========
        ctk.CTkLabel(form_frame, text="Position:").grid(
            row=5, column=0, sticky="w", pady=5, padx=10
        )
        self.position_entry = ctk.CTkEntry(form_frame, width=250)
        self.position_entry.grid(row=5, column=1, pady=5, padx=10)
        
        # ========== SALARY FIELD ==========
        ctk.CTkLabel(form_frame, text="Salary:").grid(
            row=6, column=0, sticky="w", pady=5, padx=10
        )
        self.salary_entry = ctk.CTkEntry(form_frame, width=250)
        self.salary_entry.grid(row=6, column=1, pady=5, padx=10)
        
        # ========== DEPARTMENT DROPDOWN ==========
        ctk.CTkLabel(form_frame, text="Department:").grid(
            row=7, column=0, sticky="w", pady=5, padx=10
        )
        
        # Create StringVar to track selected department
        # StringVar is a special variable that widgets can bind to
        # When value changes, widgets automatically update
        self.department_var = tk.StringVar()
        
        # Create dropdown (ComboBox) for department selection
        # variable=self.department_var binds it to the StringVar
        # state="readonly" prevents typing (user must select from list)
        self.department_combo = ctk.CTkComboBox(
            form_frame, 
            variable=self.department_var, 
            width=250, 
            state="readonly"
        )
        self.department_combo.grid(row=7, column=1, pady=5, padx=10)
        
        # Load departments into dropdown
        # This queries database and populates the dropdown
        self.load_departments()
        
        # ========== HIRE DATE FIELD ==========
        ctk.CTkLabel(form_frame, text="Hire Date (YYYY-MM-DD):").grid(
            row=8, column=0, sticky="w", pady=5, padx=10
        )
        self.hire_date_entry = ctk.CTkEntry(form_frame, width=250)
        self.hire_date_entry.grid(row=8, column=1, pady=5, padx=10)
        
        # ========== BUTTONS ==========
        # Create frame for buttons (transparent background)
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=9, column=0, columnspan=2, pady=20)
        
        # Create "Add Employee" button
        # command=self.save_employee calls save_employee() when clicked
        add_button = ctk.CTkButton(
            button_frame, 
            text="Add Employee", 
            command=self.save_employee, 
            width=120
        )
        add_button.pack(side="left", padx=5)
        
        # Create "Clear" button
        # command=self.clear_form clears all input fields
        clear_button = ctk.CTkButton(
            button_frame, 
            text="Clear", 
            command=self.clear_form, 
            width=120
        )
        clear_button.pack(side="left", padx=5)
    
    def create_update_form(self):
        """
        Create form for updating existing employees.
        
        This form has two parts:
        1. Dropdown to select which employee to update
        2. Form fields (shown after selection) to edit employee data
        
        The form is dynamic - it changes when user selects an employee.
        """
        # Create frame for employee selection dropdown
        select_frame = ctk.CTkFrame(self)
        # fill="x" makes it fill horizontally (full width)
        select_frame.pack(fill="x", padx=20, pady=10)
        
        # Create label for selection section
        ctk.CTkLabel(
            select_frame, 
            text="Select Employee to Update", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=5)
        
        # Create frame for dropdown and label (transparent)
        selection_input_frame = ctk.CTkFrame(select_frame, fg_color="transparent")
        selection_input_frame.pack(pady=5)
        
        # Create label for dropdown
        ctk.CTkLabel(selection_input_frame, text="Employee:").pack(side="left", padx=5)
        
        # Create StringVar to track selected employee
        self.emp_select_var = tk.StringVar()
        
        # Create dropdown for employee selection
        # command=self.on_employee_selected is called when selection changes
        # This automatically loads the employee form when user selects someone
        self.emp_select_combo = ctk.CTkComboBox(
            selection_input_frame, 
            variable=self.emp_select_var, 
            width=300, 
            state="readonly", 
            command=self.on_employee_selected
        )
        self.emp_select_combo.pack(side="left", padx=5)
        
        # Load employees into dropdown
        # This queries database and populates dropdown with employee list
        self.load_employees_for_selection()
        
        # Create frame for the actual update form
        # This will be populated when user selects an employee
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Initialize selected employee ID to None
        # This will be set when user selects an employee
        self.selected_emp_id = None
    
    def create_delete_form(self):
        """
        Create interface for deleting employees.
        
        This interface:
        1. Shows dropdown to select employee
        2. Displays employee information when selected
        3. Shows delete button (enabled only after selection)
        4. Confirms deletion before actually deleting
        """
        # Create frame for delete interface
        delete_frame = ctk.CTkFrame(self)
        delete_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create title label
        ctk.CTkLabel(
            delete_frame, 
            text="Delete Employee", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Create label for dropdown
        ctk.CTkLabel(delete_frame, text="Select Employee:").grid(
            row=1, column=0, sticky="w", pady=5, padx=10
        )
        
        # Create StringVar for employee selection
        self.delete_emp_var = tk.StringVar()
        
        # Create dropdown for employee selection
        # command=self.on_delete_employee_selected is called on selection
        self.delete_emp_combo = ctk.CTkComboBox(
            delete_frame, 
            variable=self.delete_emp_var, 
            width=350, 
            state="readonly", 
            command=self.on_delete_employee_selected
        )
        # sticky="ew" makes it expand horizontally
        self.delete_emp_combo.grid(row=1, column=1, pady=5, padx=10, sticky="ew")
        
        # Configure column to expand (allows dropdown to grow)
        delete_frame.grid_columnconfigure(1, weight=1)
        
        # Load employees into dropdown
        self.load_employees_for_delete_selection()
        
        # Create label to display employee information
        # This will show employee details when selected
        self.delete_info_label = ctk.CTkLabel(
            delete_frame, 
            text="", 
            font=ctk.CTkFont(size=12)
        )
        self.delete_info_label.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Create delete button (disabled initially)
        # state="disabled" means button is grayed out and can't be clicked
        # It will be enabled when user selects an employee
        self.delete_button = ctk.CTkButton(
            delete_frame, 
            text="Delete Employee", 
            command=self.delete_employee, 
            state="disabled", 
            width=200
        )
        self.delete_button.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Initialize delete employee ID to None
        self.delete_emp_id = None
    
    def create_view_list(self):
        """
        Create table view showing all employees.
        
        This method creates a Treeview widget (table) that displays:
        - Employee ID
        - Name (first + last)
        - Email
        - Phone
        - Position
        - Salary
        - Department
        - Hire Date
        
        The table includes a scrollbar for long lists.
        """
        # Create frame to contain the table
        list_frame = ctk.CTkFrame(self)
        list_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create title label
        ctk.CTkLabel(
            list_frame, 
            text="All Employees", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        # Create container for table and scrollbar
        tree_container = ctk.CTkFrame(list_frame)
        tree_container.pack(fill="both", expand=True, pady=10)
        
        # Create scrollbar for table
        # ttk.Scrollbar creates a scrollbar widget
        scrollbar = ttk.Scrollbar(tree_container)
        # side="right" places scrollbar on right side
        # fill="y" makes it fill vertically
        scrollbar.pack(side="right", fill="y")
        
        # Create Treeview widget (table)
        # columns=() defines column names
        # show="headings" shows column headers but not tree column
        # yscrollcommand=scrollbar.set connects scrollbar to table
        self.tree = ttk.Treeview(
            tree_container, 
            columns=("ID", "Name", "Email", "Phone", "Position", "Salary", "Department", "Hire Date"),
            show="headings", 
            yscrollcommand=scrollbar.set
        )
        
        # Connect scrollbar to table
        # When user scrolls scrollbar, table scrolls
        scrollbar.config(command=self.tree.yview)
        
        # Set column headings (header text)
        # heading() sets the text displayed in column header
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Position", text="Position")
        self.tree.heading("Salary", text="Salary")
        self.tree.heading("Department", text="Department")
        self.tree.heading("Hire Date", text="Hire Date")
        
        # Set column widths (in pixels)
        # column() sets properties of a column
        self.tree.column("ID", width=50)
        self.tree.column("Name", width=150)
        self.tree.column("Email", width=150)
        self.tree.column("Phone", width=100)
        self.tree.column("Position", width=100)
        self.tree.column("Salary", width=100)
        self.tree.column("Department", width=120)
        self.tree.column("Hire Date", width=100)
        
        # Pack table to fill container
        self.tree.pack(fill="both", expand=True)
    
    def show_search_interface(self):
        """
        Create search interface with search box and results table.
        
        This interface allows users to search employees by:
        - Name (first or last)
        - Email
        - Position
        
        Results are displayed in a table below the search box.
        """
        # Create frame for search input
        search_frame = ctk.CTkFrame(self)
        search_frame.pack(fill="x", padx=20, pady=10)
        
        # Create title label
        ctk.CTkLabel(
            search_frame, 
            text="Search Employees", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=5)
        
        # Create frame for search input and button
        search_input_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
        search_input_frame.pack(pady=5)
        
        # Create label for search box
        ctk.CTkLabel(search_input_frame, text="Search:").pack(side="left", padx=5)
        
        # Create search input field
        self.search_entry = ctk.CTkEntry(search_input_frame, width=250)
        self.search_entry.pack(side="left", padx=5)
        
        # Bind Enter key to search function
        # When user presses Enter, it searches
        self.search_entry.bind('<Return>', lambda e: self.search_employees())
        
        # Create Search button
        search_button = ctk.CTkButton(
            search_input_frame, 
            text="Search", 
            command=self.search_employees, 
            width=100
        )
        search_button.pack(side="left", padx=5)
        
        # Create frame for search results table
        results_frame = ctk.CTkFrame(self)
        results_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create label for results section
        ctk.CTkLabel(
            results_frame, 
            text="Search Results", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=5)
        
        # Create container for results table
        tree_container = ctk.CTkFrame(results_frame)
        tree_container.pack(fill="both", expand=True, pady=10)
        
        # Create scrollbar for results table
        scrollbar = ttk.Scrollbar(tree_container)
        scrollbar.pack(side="right", fill="y")
        
        # Create Treeview for search results
        # This is separate from self.tree (used for view mode)
        self.search_tree = ttk.Treeview(
            tree_container, 
            columns=("ID", "Name", "Email", "Phone", "Position", "Salary", "Department"),
            show="headings", 
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.search_tree.yview)
        
        # Set column headings and widths
        for col in ("ID", "Name", "Email", "Phone", "Position", "Salary", "Department"):
            self.search_tree.heading(col, text=col)
            self.search_tree.column(col, width=120)
        
        # Pack results table
        self.search_tree.pack(fill="both", expand=True)
    
    def load_departments(self):
        """
        Load departments from database and populate dropdown.
        
        This method:
        1. Queries database for all departments
        2. Formats them as "ID: Name" strings
        3. Adds "None" option for employees without department
        4. Populates the department dropdown
        """
        try:
            # Get all departments from database
            # get_all() returns list of department dictionaries
            departments = self.department_model.get_all()
            
            # Create list of department strings for dropdown
            # Format: "ID: Name" (e.g., "1: IT Department")
            # ["None"] adds option for no department
            dept_list = ["None"] + [
                f"{d.get('id', '')}: {d.get('name', '')}" 
                for d in departments
            ]
            
            # Check if department_combo exists (it might not in all modes)
            if hasattr(self, 'department_combo'):
                # Configure dropdown with department list
                # configure() changes widget properties
                self.department_combo.configure(values=dept_list)
                
                # Set default selection to "None"
                if dept_list:
                    self.department_combo.set("None")
        except Exception:
            # If error occurs (database issue, etc.), silently fail
            # This prevents crashes if departments can't be loaded
            pass
    
    def get_selected_department_id(self):
        """
        Extract department ID from dropdown selection.
        
        The dropdown shows "ID: Name" format (e.g., "1: IT Department").
        This method extracts just the ID number.
        
        Returns:
            int or None: Department ID if selected, None if "None" selected
        """
        # Get selected value from dropdown
        selection = self.department_var.get()
        
        # If "None" or empty, return None
        if not selection or selection == "None":
            return None
        
        try:
            # Split by ":" and take first part (the ID)
            # "1: IT Department".split(":")[0] = "1"
            # int() converts string to integer
            return int(selection.split(":")[0])
        except (ValueError, IndexError, AttributeError):
            # If parsing fails, return None
            # This handles malformed selections gracefully
            return None
    
    def validate_form(self):
        """
        Validate all form inputs before saving.
        
        This method checks:
        - Required fields are not empty (first name, last name, email)
        - Email format is valid
        - Phone format is valid (if provided)
        - Salary is a valid number (if provided)
        - Date format is correct (if provided)
        
        Returns:
            tuple: (is_valid: bool, error_message: str)
                   - is_valid: True if all validations pass
                   - error_message: Error message if validation fails, empty string if valid
        """
        # Validate first name (required)
        # validate_required() returns (is_valid, error_message)
        valid, msg = validate_required(self.first_name_entry.get(), "First name")
        if not valid:
            return False, msg
        
        # Validate last name (required)
        valid, msg = validate_required(self.last_name_entry.get(), "Last name")
        if not valid:
            return False, msg
        
        # Validate email (required and must be valid format)
        email = self.email_entry.get().strip()
        valid, msg = validate_required(email, "Email")
        if not valid:
            return False, msg
        
        # Check email format
        if not validate_email(email):
            return False, "Invalid email format"
        
        # Validate phone (optional, but must be valid format if provided)
        phone = self.phone_entry.get().strip()
        if phone and not validate_phone(phone):
            return False, "Invalid phone number format"
        
        # Validate salary (optional, but must be valid number if provided)
        salary_str = self.salary_entry.get().strip()
        if salary_str:
            # validate_salary() returns (is_valid, error_message, salary_value)
            valid, msg, _ = validate_salary(salary_str)
            if not valid:
                return False, msg
        
        # Validate hire date (optional, but must be valid format if provided)
        hire_date = self.hire_date_entry.get().strip()
        if hire_date:
            valid, msg = validate_date(hire_date)
            if not valid:
                return False, msg
        
        # All validations passed
        return True, ""
    
    def save_employee(self):
        """
        Save new employee to database.
        
        This method:
        1. Validates form inputs
        2. Converts salary string to float
        3. Gets selected department ID
        4. Calls EmployeeModel.create() to save to database
        5. Shows success/error message
        6. Clears form if successful
        """
        # Validate form inputs
        valid, error_msg = self.validate_form()
        if not valid:
            # Show error dialog if validation fails
            messagebox.showerror("Validation Error", error_msg)
            return  # Exit early if validation fails
        
        # Try to save employee
        try:
            # Get salary from input field
            salary_str = self.salary_entry.get().strip()
            
            # Validate and convert salary
            # validate_salary() returns (is_valid, error_message, salary_value)
            valid, _, salary = validate_salary(salary_str)
            # Use validated salary, or 0.0 if invalid/empty
            salary = salary if valid else 0.0
            
            # Get selected department ID (None if "None" selected)
            dept_id = self.get_selected_department_id()
            
            # Get hire date (empty string if not provided)
            hire_date = self.hire_date_entry.get().strip()
            
            # Create employee in database
            # employee_model.create() saves to database and returns employee ID
            self.employee_model.create(
                first_name=self.first_name_entry.get().strip(),
                last_name=self.last_name_entry.get().strip(),
                email=self.email_entry.get().strip(),
                phone=self.phone_entry.get().strip(),
                position=self.position_entry.get().strip(),
                salary=salary,
                department_id=dept_id,
                hire_date=hire_date
            )
            
            # Show success message
            messagebox.showinfo("Success", "Employee added successfully!")
            
            # Clear form so user can add another employee
            self.clear_form()
        except Exception as e:
            # If error occurs (database error, duplicate email, etc.), show error
            messagebox.showerror("Error", f"Failed to add employee: {str(e)}")
    
    def clear_form(self):
        """
        Clear all input fields in the form.
        
        This method resets all entry fields to empty, allowing user to
        start fresh when adding a new employee.
        """
        # Clear each input field
        # delete(0, "end") removes all text from field
        # 0 is start position, "end" is end position
        self.first_name_entry.delete(0, "end")
        self.last_name_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.phone_entry.delete(0, "end")
        self.position_entry.delete(0, "end")
        self.salary_entry.delete(0, "end")
        self.hire_date_entry.delete(0, "end")
        
        # Reset department dropdown to "None"
        if hasattr(self, 'department_combo'):
            self.department_combo.set("None")
    
    def load_employees_for_selection(self):
        """
        Load employees into update/delete selection dropdowns.
        
        This method queries database and formats employees as:
        "ID: FirstName LastName (email)"
        
        Used for update and delete forms.
        """
        try:
            # Get all employees from database
            employees = self.employee_model.get_all()
            
            # Create list of employee strings for dropdown
            # Format: "ID: FirstName LastName (email)"
            emp_list = ["-- Select an Employee --"] + [
                f"{emp.get('id', '')}: {emp.get('first_name', '')} {emp.get('last_name', '')} ({emp.get('email', '')})"
                for emp in employees
            ]
            
            # Check if combo box exists (it might not in all modes)
            if hasattr(self, 'emp_select_combo'):
                # Configure dropdown with employee list
                self.emp_select_combo.configure(values=emp_list)
                # Set default to first item (the "-- Select --" option)
                if emp_list:
                    self.emp_select_combo.set(emp_list[0])
        except Exception:
            # Silently fail if error occurs
            pass
    
    def on_employee_selected(self, choice=None):
        """
        Handle employee selection from update dropdown.
        
        This method is called automatically when user selects an employee
        from the dropdown in update mode. It loads the employee's data
        into the form fields.
        
        Args:
            choice: Selected value (optional, can also get from StringVar)
        """
        # Check if selection variable exists
        if not hasattr(self, 'emp_select_var'):
            return
        
        # Get selected value
        selection = self.emp_select_var.get()
        
        # If no selection or default option, clear form
        if not selection or selection == "-- Select an Employee --":
            # Remove all widgets from form frame
            for widget in self.form_frame.winfo_children():
                widget.destroy()
            # Clear selected employee ID
            self.selected_emp_id = None
            return
        
        try:
            # Extract employee ID from selection string
            # "1: John Doe (john@example.com)".split(":")[0] = "1"
            emp_id = int(selection.split(":")[0])
            
            # Load employee data into form
            self.load_employee_for_update(emp_id)
        except (ValueError, IndexError):
            # If parsing fails, show error
            messagebox.showerror("Error", "Invalid selection")
    
    def load_employee_for_update(self, emp_id=None):
        """
        Load employee data into update form fields.
        
        This method:
        1. Queries database for employee data
        2. Clears existing form widgets
        3. Creates new form fields with employee data pre-filled
        4. Creates update button that saves changes
        
        Args:
            emp_id: Employee ID to load (if None, uses self.selected_emp_id)
        """
        try:
            # Get employee ID (use parameter or stored value)
            if emp_id is None:
                # If no ID provided, check if we have stored ID
                if not hasattr(self, 'selected_emp_id') or self.selected_emp_id is None:
                    return  # No employee selected, exit
                emp_id = self.selected_emp_id
            else:
                # Store ID for later use
                self.selected_emp_id = emp_id
            
            # Get employee data from database
            employee = self.employee_model.get_by_id(emp_id)
            
            # Check if employee exists
            if not employee:
                messagebox.showerror("Error", "Employee not found")
                return
            
            # Clear existing form widgets
            # This removes any previously displayed form
            for widget in self.form_frame.winfo_children():
                widget.destroy()
            
            # Create title label
            ctk.CTkLabel(
                self.form_frame, 
                text="Update Employee", 
                font=ctk.CTkFont(size=16, weight="bold")
            ).grid(row=0, column=0, columnspan=2, pady=10)
            
            # ========== CREATE FORM FIELDS WITH PRE-FILLED DATA ==========
            
            # First Name field
            ctk.CTkLabel(self.form_frame, text="First Name *:").grid(
                row=1, column=0, sticky="w", pady=5, padx=10
            )
            first_name_entry = ctk.CTkEntry(self.form_frame, width=250)
            # insert(0, value) adds text at position 0 (beginning)
            first_name_entry.insert(0, employee.get('first_name', ''))
            first_name_entry.grid(row=1, column=1, pady=5, padx=10)
            
            # Last Name field
            ctk.CTkLabel(self.form_frame, text="Last Name *:").grid(
                row=2, column=0, sticky="w", pady=5, padx=10
            )
            last_name_entry = ctk.CTkEntry(self.form_frame, width=250)
            last_name_entry.insert(0, employee.get('last_name', ''))
            last_name_entry.grid(row=2, column=1, pady=5, padx=10)
            
            # Email field
            ctk.CTkLabel(self.form_frame, text="Email *:").grid(
                row=3, column=0, sticky="w", pady=5, padx=10
            )
            email_entry = ctk.CTkEntry(self.form_frame, width=250)
            email_entry.insert(0, employee.get('email', ''))
            email_entry.grid(row=3, column=1, pady=5, padx=10)
            
            # Phone field
            ctk.CTkLabel(self.form_frame, text="Phone:").grid(
                row=4, column=0, sticky="w", pady=5, padx=10
            )
            phone_entry = ctk.CTkEntry(self.form_frame, width=250)
            # Use empty string if phone is None
            phone_entry.insert(0, employee.get('phone') or "")
            phone_entry.grid(row=4, column=1, pady=5, padx=10)
            
            # Position field
            ctk.CTkLabel(self.form_frame, text="Position:").grid(
                row=5, column=0, sticky="w", pady=5, padx=10
            )
            position_entry = ctk.CTkEntry(self.form_frame, width=250)
            position_entry.insert(0, employee.get('position') or "")
            position_entry.grid(row=5, column=1, pady=5, padx=10)
            
            # Salary field
            ctk.CTkLabel(self.form_frame, text="Salary:").grid(
                row=6, column=0, sticky="w", pady=5, padx=10
            )
            salary_entry = ctk.CTkEntry(self.form_frame, width=250)
            # Convert salary to string, use 0 if None
            salary_entry.insert(0, str(employee.get('salary') or 0))
            salary_entry.grid(row=6, column=1, pady=5, padx=10)
            
            # Department dropdown
            ctk.CTkLabel(self.form_frame, text="Department:").grid(
                row=7, column=0, sticky="w", pady=5, padx=10
            )
            dept_var = tk.StringVar()
            dept_combo = ctk.CTkComboBox(
                self.form_frame, 
                variable=dept_var, 
                width=250, 
                state="readonly"
            )
            
            # Load departments into dropdown
            departments = self.department_model.get_all()
            dept_list = ["None"] + [
                f"{d.get('id', '')}: {d.get('name', '')}" 
                for d in departments
            ]
            dept_combo.configure(values=dept_list)
            
            # Set dropdown to employee's current department
            dept_id = employee.get('department_id')
            if dept_id:
                # Find matching department in list
                for i, d in enumerate(departments, 1):  # Start at 1 to skip "None"
                    if d.get('id') == dept_id:
                        dept_combo.set(dept_list[i])
                        break
                else:
                    # If not found, set to "None"
                    dept_combo.set("None")
            else:
                dept_combo.set("None")
            dept_combo.grid(row=7, column=1, pady=5, padx=10)
            
            # Hire Date field
            ctk.CTkLabel(self.form_frame, text="Hire Date (YYYY-MM-DD):").grid(
                row=8, column=0, sticky="w", pady=5, padx=10
            )
            hire_date_entry = ctk.CTkEntry(self.form_frame, width=250)
            hire_date_entry.insert(0, employee.get('hire_date') or "")
            hire_date_entry.grid(row=8, column=1, pady=5, padx=10)
            
            # Define update function (nested function)
            # This function is called when user clicks "Update Employee" button
            def update_employee():
                """
                Handle update button click.
                
                This function:
                1. Validates inputs
                2. Gets values from form fields
                3. Calls EmployeeModel.update() to save changes
                4. Shows success/error message
                5. Reloads form with updated data
                """
                try:
                    # Validate and convert salary
                    salary_str = salary_entry.get().strip()
                    valid, _, salary = validate_salary(salary_str)
                    salary = salary if valid else 0.0
                    
                    # Get selected department ID
                    dept_selection = dept_var.get()
                    dept_id = None if not dept_selection or dept_selection == "None" else int(dept_selection.split(":")[0])
                    
                    # Validate required fields
                    if not first_name_entry.get().strip():
                        messagebox.showerror("Error", "First name is required")
                        return
                    if not last_name_entry.get().strip():
                        messagebox.showerror("Error", "Last name is required")
                        return
                    
                    # Validate email
                    email = email_entry.get().strip()
                    if not email:
                        messagebox.showerror("Error", "Email is required")
                        return
                    if not validate_email(email):
                        messagebox.showerror("Error", "Invalid email format")
                        return
                    
                    # Update employee in database
                    self.employee_model.update(
                        emp_id=self.selected_emp_id,
                        first_name=first_name_entry.get().strip(),
                        last_name=last_name_entry.get().strip(),
                        email=email,
                        phone=phone_entry.get().strip(),
                        position=position_entry.get().strip(),
                        salary=salary,
                        department_id=dept_id,
                        hire_date=hire_date_entry.get().strip()
                    )
                    
                    # Show success message
                    messagebox.showinfo("Success", "Employee updated successfully!")
                    
                    # Reload employee list and form
                    # This refreshes the dropdown and form with latest data
                    self.load_employees_for_selection()
                    self.load_employee_for_update(self.selected_emp_id)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update employee: {str(e)}")
            
            # Create button frame
            button_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
            button_frame.grid(row=9, column=0, columnspan=2, pady=20)
            
            # Create Update button
            ctk.CTkButton(
                button_frame, 
                text="Update Employee", 
                command=update_employee, 
                width=120
            ).pack(side="left", padx=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load employee: {str(e)}")
    
    def load_employees_for_delete_selection(self):
        """
        Load employees into delete selection dropdown.
        
        Similar to load_employees_for_selection() but for delete form.
        """
        try:
            employees = self.employee_model.get_all()
            emp_list = ["-- Select an Employee --"] + [
                f"{emp.get('id', '')}: {emp.get('first_name', '')} {emp.get('last_name', '')} ({emp.get('email', '')})"
                for emp in employees
            ]
            if hasattr(self, 'delete_emp_combo'):
                self.delete_emp_combo.configure(values=emp_list)
                if emp_list:
                    self.delete_emp_combo.set(emp_list[0])
        except Exception:
            pass
    
    def on_delete_employee_selected(self, choice=None):
        """
        Handle employee selection from delete dropdown.
        
        Called when user selects an employee to delete.
        Loads employee information and enables delete button.
        """
        if not hasattr(self, 'delete_emp_var'):
            return
        
        selection = self.delete_emp_var.get()
        if not selection or selection == "-- Select an Employee --":
            # Clear info and disable button
            self.delete_info_label.configure(text="")
            self.delete_button.configure(state="disabled")
            self.delete_emp_id = None
            return
        
        try:
            # Extract employee ID
            emp_id = int(selection.split(":")[0])
            # Load employee for deletion
            self.load_employee_for_delete(emp_id)
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Invalid selection")
    
    def load_employee_for_delete(self, emp_id):
        """
        Load employee information for deletion confirmation.
        
        This method displays employee details so user can confirm
        they're deleting the right person.
        
        Args:
            emp_id: Employee ID to load
        """
        try:
            # Get employee data
            employee = self.employee_model.get_by_id(emp_id)
            
            if not employee:
                messagebox.showerror("Error", "Employee not found")
                # Clear info and disable button
                self.delete_info_label.configure(text="")
                self.delete_button.configure(state="disabled")
                return
            
            # Format employee information for display
            info_text = (
                f"ID: {employee.get('id', 'N/A')}\n"
                f"Name: {employee.get('first_name', '')} {employee.get('last_name', '')}\n"
                f"Email: {employee.get('email', 'N/A')}\n"
                f"Position: {employee.get('position') or 'N/A'}\n"
                f"Department: {employee.get('department_name', 'N/A')}"
            )
            
            # Display employee info
            self.delete_info_label.configure(text=info_text)
            
            # Enable delete button (user can now delete)
            self.delete_button.configure(state="normal")
            
            # Store employee ID for deletion
            self.delete_emp_id = emp_id
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load employee: {str(e)}")
    
    def delete_employee(self):
        """
        Delete selected employee from database.
        
        This method:
        1. Confirms deletion with user
        2. Calls EmployeeModel.delete() to remove from database
        3. Shows success/error message
        4. Resets form
        """
        # Check if employee is selected
        if not hasattr(self, 'delete_emp_id') or self.delete_emp_id is None:
            return
        
        # Confirm deletion with user
        # askyesno() shows Yes/No dialog, returns True if Yes
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this employee?"):
            try:
                # Delete employee from database
                self.employee_model.delete(self.delete_emp_id)
                
                # Show success message
                messagebox.showinfo("Success", "Employee deleted successfully!")
                
                # Clear info label
                self.delete_info_label.configure(text="")
                
                # Disable delete button
                self.delete_button.configure(state="disabled")
                
                # Clear employee ID
                self.delete_emp_id = None
                
                # Reload employee list in dropdown
                self.load_employees_for_delete_selection()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete employee: {str(e)}")
    
    def load_employees(self):
        """
        Load all employees into the table view.
        
        This method:
        1. Queries database for all employees
        2. Clears existing table rows
        3. Adds each employee as a row in the table
        
        Used in "view" mode to display employee list.
        """
        try:
            # Check if tree widget exists
            if hasattr(self, 'tree'):
                # Clear existing rows
                # get_children() returns list of all row IDs
                for item in self.tree.get_children():
                    # delete() removes a row from table
                    self.tree.delete(item)
                
                # Get all employees from database
                employees = self.employee_model.get_all()
                
                # Add each employee as a row
                for emp in employees:
                    try:
                        # Extract employee data
                        emp_id = emp.get('id', 'N/A')
                        name = f"{emp.get('first_name', '')} {emp.get('last_name', '')}".strip()
                        email = emp.get('email', 'N/A')
                        phone = emp.get('phone') or "N/A"
                        position = emp.get('position') or "N/A"
                        
                        # Format salary with currency symbol
                        salary_val = emp.get('salary')
                        salary = f"${salary_val:.2f}" if salary_val is not None and salary_val != 0 else "N/A"
                        
                        dept = emp.get('department_name', 'N/A')
                        hire_date = emp.get('hire_date') or "N/A"
                        
                        # Insert row into table
                        # insert() adds a new row
                        # "" means root (top level)
                        # "end" means add at end
                        # values=() provides the data for each column
                        self.tree.insert(
                            "", 
                            "end", 
                            values=(emp_id, name, email, phone, position, salary, dept, hire_date)
                        )
                    except Exception:
                        # Skip this employee if error occurs (prevents crash)
                        continue
        except Exception:
            # Silently fail if error occurs
            pass
    
    def search_employees(self):
        """
        Search for employees and display results.
        
        This method:
        1. Gets search term from input field
        2. Validates search term is not empty
        3. Calls EmployeeModel.search() to find matching employees
        4. Displays results in table
        
        Search looks in: first name, last name, email, position
        """
        # Get search term from input field
        search_term = self.search_entry.get().strip()
        
        # Validate search term is not empty
        if not search_term:
            messagebox.showwarning("Warning", "Please enter a search term")
            return
        
        # Clear existing search results
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)
        
        # Search for employees
        # search() returns list of matching employees
        employees = self.employee_model.search(search_term)
        
        # Add each result as a row in table
        for emp in employees:
            try:
                # Extract and format employee data
                emp_id = emp.get('id', 'N/A')
                name = f"{emp.get('first_name', '')} {emp.get('last_name', '')}".strip()
                email = emp.get('email', 'N/A')
                phone = emp.get('phone') or "N/A"
                position = emp.get('position') or "N/A"
                
                # Format salary
                salary_val = emp.get('salary')
                salary = f"${salary_val:.2f}" if salary_val is not None and salary_val != 0 else "N/A"
                
                dept = emp.get('department_name', 'N/A')
                
                # Insert row into search results table
                self.search_tree.insert(
                    "", 
                    "end", 
                    values=(emp_id, name, email, phone, position, salary, dept)
                )
            except Exception:
                # Skip this employee if error occurs
                continue
