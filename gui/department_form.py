"""
Department Management Forms - Smart Records System

This module creates forms for managing departments. It supports multiple "modes":
- add: Form to add new departments
- view: Table showing all departments
- update: Form to update existing departments
- delete: Interface to delete departments

Departments are simpler than employees - they only have:
- Name (required, must be unique)
- Description (optional)

GUI CONCEPTS EXPLAINED:
- CTkScrollableFrame: Frame that can scroll if content is too large
- CTkEntry: Single-line text input field
- CTkTextbox: Multi-line text input field (for descriptions)
- CTkComboBox: Dropdown selection box
- ttk.Treeview: Table widget for displaying data
- StringVar: Variable that tracks text value (used with widgets)
"""

# Import CustomTkinter for modern GUI widgets
import customtkinter as ctk

# Import tkinter for StringVar and Treeview
import tkinter as tk

# Import ttk (themed tkinter) for Treeview widget
# Import messagebox for popup dialogs
from tkinter import ttk, messagebox

# Import validation function
# validate_required checks if a field is not empty
from utils.validators import validate_required


class DepartmentForm(ctk.CTkScrollableFrame):
    """
    Department Form Class - Handles All Department Operations
    
    This class inherits from CTkScrollableFrame, which provides:
    - Scrollable content area
    - Container for other widgets
    
    The form works in different "modes":
    - "add": Show form to add new department
    - "view": Show table of all departments
    - "update": Show form to update existing department
    - "delete": Show interface to delete department
    """
    
    def __init__(self, parent, department_model, mode="view"):
        """
        Initialize department form.
        
        Args:
            parent: Parent widget (usually content_frame from MainWindow)
            department_model: DepartmentModel instance - handles department data operations
            mode: Form mode string - determines what interface to show
                 Options: 'add', 'view', 'update', 'delete'
        """
        # Call parent class constructor
        # super() refers to CTkScrollableFrame parent class
        super().__init__(parent)
        
        # Store reference to department model
        # This is used to save/load department data
        self.department_model = department_model
        
        # Store form mode
        self.mode = mode
        
        # Create widgets based on mode
        self.create_widgets()
        
        # If mode is "view", load departments immediately
        # This displays the department table right away
        if mode == "view":
            self.load_departments()
    
    def create_widgets(self):
        """
        Create form widgets based on current mode.
        
        This method acts as a router - it calls the appropriate method
        based on the form mode to create the correct interface.
        """
        # Check mode and call appropriate method
        if self.mode == "add":
            # Create form for adding new departments
            self.create_add_form()
        elif self.mode == "update":
            # Create form for updating existing departments
            self.create_update_form()
        elif self.mode == "delete":
            # Create interface for deleting departments
            self.create_delete_form()
        elif self.mode == "view":
            # Create table view of all departments
            self.create_view_list()
    
    def create_add_form(self):
        """
        Create form for adding new departments.
        
        This method creates:
        - Input field for department name (required)
        - Text area for description (optional)
        - Add and Clear buttons
        
        The form uses grid() layout manager for organized rows and columns.
        """
        # Create frame to contain the form
        form_frame = ctk.CTkFrame(self)
        
        # Pack frame to fill available space
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create title label
        # columnspan=2 makes it span both columns (full width)
        ctk.CTkLabel(
            form_frame, 
            text="Add New Department", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=10)
        
        # ========== DEPARTMENT NAME FIELD ==========
        # Create label for department name
        # * indicates required field
        ctk.CTkLabel(form_frame, text="Department Name *:").grid(
            row=1, column=0, sticky="w", pady=5, padx=10
        )
        
        # Create input field for department name
        # width=300 sets field width to 300 pixels
        self.name_entry = ctk.CTkEntry(form_frame, width=300)
        self.name_entry.grid(row=1, column=1, pady=5, padx=10)
        
        # Set focus to name field (cursor appears here automatically)
        # This improves user experience - user can start typing immediately
        self.name_entry.focus()
        
        # ========== DESCRIPTION FIELD ==========
        # Create label for description
        ctk.CTkLabel(form_frame, text="Description:").grid(
            row=2, column=0, sticky="w", pady=5, padx=10
        )
        
        # Create text area for description
        # CTkTextbox creates a multi-line text input field
        # width=300, height=100 sets dimensions
        # This allows longer descriptions than a single-line entry
        self.description_text = ctk.CTkTextbox(form_frame, width=300, height=100)
        self.description_text.grid(row=2, column=1, pady=5, padx=10)
        
        # ========== BUTTONS ==========
        # Create frame for buttons (transparent background)
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Create "Add Department" button
        # command=self.save_department calls save_department() when clicked
        add_button = ctk.CTkButton(
            button_frame, 
            text="Add Department", 
            command=self.save_department, 
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
        Create form for updating existing departments.
        
        This form has two parts:
        1. Dropdown to select which department to update
        2. Form fields (shown after selection) to edit department data
        
        The form is dynamic - it changes when user selects a department.
        """
        # Create frame for department selection dropdown
        select_frame = ctk.CTkFrame(self)
        # fill="x" makes it fill horizontally (full width)
        select_frame.pack(fill="x", padx=20, pady=10)
        
        # Create label for selection section
        ctk.CTkLabel(
            select_frame, 
            text="Select Department to Update", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=5)
        
        # Create frame for dropdown and label (transparent)
        selection_input_frame = ctk.CTkFrame(select_frame, fg_color="transparent")
        selection_input_frame.pack(pady=5)
        
        # Create label for dropdown
        ctk.CTkLabel(selection_input_frame, text="Department:").pack(side="left", padx=5)
        
        # Create StringVar to track selected department
        self.dept_select_var = tk.StringVar()
        
        # Create dropdown for department selection
        # command=self.on_department_selected is called when selection changes
        # This automatically loads the department form when user selects one
        self.dept_select_combo = ctk.CTkComboBox(
            selection_input_frame, 
            variable=self.dept_select_var, 
            width=300, 
            state="readonly", 
            command=self.on_department_selected
        )
        self.dept_select_combo.pack(side="left", padx=5)
        
        # Load departments into dropdown
        self.load_departments_for_selection()
        
        # Create frame for the actual update form
        # This will be populated when user selects a department
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Initialize selected department ID to None
        self.selected_dept_id = None
    
    def create_delete_form(self):
        """
        Create interface for deleting departments.
        
        This interface:
        1. Shows dropdown to select department
        2. Displays department information when selected
        3. Shows warning if department has employees
        4. Shows delete button (enabled only after selection)
        5. Confirms deletion before actually deleting
        """
        # Create frame for delete interface
        delete_frame = ctk.CTkFrame(self)
        delete_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create title label
        ctk.CTkLabel(
            delete_frame, 
            text="Delete Department", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Create label for dropdown
        ctk.CTkLabel(delete_frame, text="Select Department:").grid(
            row=1, column=0, sticky="w", pady=5, padx=10
        )
        
        # Create StringVar for department selection
        self.delete_dept_var = tk.StringVar()
        
        # Create dropdown for department selection
        # command=self.on_delete_department_selected is called on selection
        self.delete_dept_combo = ctk.CTkComboBox(
            delete_frame, 
            variable=self.delete_dept_var, 
            width=350, 
            state="readonly", 
            command=self.on_delete_department_selected
        )
        # sticky="ew" makes it expand horizontally
        self.delete_dept_combo.grid(row=1, column=1, pady=5, padx=10, sticky="ew")
        
        # Configure column to expand (allows dropdown to grow)
        delete_frame.grid_columnconfigure(1, weight=1)
        
        # Load departments into dropdown
        self.load_departments_for_delete_selection()
        
        # Create label to display department information
        # This will show department details when selected
        self.delete_info_label = ctk.CTkLabel(
            delete_frame, 
            text="", 
            font=ctk.CTkFont(size=12)
        )
        self.delete_info_label.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Create delete button (disabled initially)
        # state="disabled" means button is grayed out and can't be clicked
        # It will be enabled when user selects a department
        self.delete_button = ctk.CTkButton(
            delete_frame, 
            text="Delete Department", 
            command=self.delete_department, 
            state="disabled", 
            width=200
        )
        self.delete_button.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Initialize delete department ID to None
        self.delete_dept_id = None
    
    def create_view_list(self):
        """
        Create table view showing all departments.
        
        This method creates a Treeview widget (table) that displays:
        - Department ID
        - Name
        - Description
        - Created At (timestamp)
        
        The table includes a scrollbar for long lists.
        """
        # Create frame to contain the table
        list_frame = ctk.CTkFrame(self)
        list_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create title label
        ctk.CTkLabel(
            list_frame, 
            text="All Departments", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        # Create container for table and scrollbar
        tree_container = ctk.CTkFrame(list_frame)
        tree_container.pack(fill="both", expand=True, pady=10)
        
        # Create scrollbar for table
        scrollbar = ttk.Scrollbar(tree_container)
        scrollbar.pack(side="right", fill="y")
        
        # Create Treeview widget (table)
        # columns=() defines column names
        # show="headings" shows column headers but not tree column
        # yscrollcommand=scrollbar.set connects scrollbar to table
        self.tree = ttk.Treeview(
            tree_container, 
            columns=("ID", "Name", "Description", "Created"),
            show="headings", 
            yscrollcommand=scrollbar.set
        )
        
        # Connect scrollbar to table
        scrollbar.config(command=self.tree.yview)
        
        # Set column headings (header text)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Created", text="Created At")
        
        # Set column widths (in pixels)
        self.tree.column("ID", width=80)
        self.tree.column("Name", width=200)
        self.tree.column("Description", width=300)
        self.tree.column("Created", width=150)
        
        # Pack table to fill container
        self.tree.pack(fill="both", expand=True)
    
    def validate_form(self):
        """
        Validate form inputs before saving.
        
        This method checks:
        - Department name is not empty (required field)
        
        Returns:
            tuple: (is_valid: bool, error_message: str)
        """
        # Validate department name (required)
        # validate_required() returns (is_valid, error_message)
        valid, msg = validate_required(self.name_entry.get(), "Department name")
        if not valid:
            return False, msg
        
        # All validations passed
        return True, ""
    
    def save_department(self):
        """
        Save new department to database.
        
        This method:
        1. Validates form inputs
        2. Gets description from text area
        3. Calls DepartmentModel.create() to save to database
        4. Shows success/error message
        5. Clears form if successful
        """
        # Validate form inputs
        valid, error_msg = self.validate_form()
        if not valid:
            # Show error dialog if validation fails
            messagebox.showerror("Validation Error", error_msg)
            return  # Exit early if validation fails
        
        # Try to save department
        try:
            # Get description from text area
            # get("1.0", "end-1c") gets all text from text area
            # "1.0" means line 1, character 0 (start)
            # "end-1c" means end minus 1 character (removes trailing newline)
            # .strip() removes leading/trailing whitespace
            description = self.description_text.get("1.0", "end-1c").strip()
            
            # Create department in database
            # department_model.create() saves to database and returns department ID
            self.department_model.create(
                name=self.name_entry.get().strip(),
                description=description
            )
            
            # Show success message
            messagebox.showinfo("Success", "Department added successfully!")
            
            # Clear form so user can add another department
            self.clear_form()
        except Exception as e:
            # If error occurs (database error, duplicate name, etc.), show error
            messagebox.showerror("Error", f"Failed to add department: {str(e)}")
    
    def clear_form(self):
        """
        Clear all input fields in the form.
        
        This method resets all entry fields to empty, allowing user to
        start fresh when adding a new department.
        """
        # Clear name field
        # delete(0, "end") removes all text from field
        self.name_entry.delete(0, "end")
        
        # Clear description text area
        # delete("1.0", "end") removes all text from text area
        self.description_text.delete("1.0", "end")
    
    def load_departments_for_selection(self):
        """
        Load departments into update/delete selection dropdowns.
        
        This method queries database and formats departments as:
        "ID: Name"
        
        Used for update and delete forms.
        """
        try:
            # Get all departments from database
            departments = self.department_model.get_all()
            
            # Create list of department strings for dropdown
            # Format: "ID: Name" (e.g., "1: IT Department")
            dept_list = ["-- Select a Department --"] + [
                f"{dept.get('id', '')}: {dept.get('name', '')}"
                for dept in departments
            ]
            
            # Check if combo box exists (it might not in all modes)
            if hasattr(self, 'dept_select_combo'):
                # Configure dropdown with department list
                self.dept_select_combo.configure(values=dept_list)
                # Set default to first item (the "-- Select --" option)
                if dept_list:
                    self.dept_select_combo.set(dept_list[0])
        except Exception:
            # Silently fail if error occurs
            pass
    
    def on_department_selected(self, choice=None):
        """
        Handle department selection from update dropdown.
        
        This method is called automatically when user selects a department
        from the dropdown in update mode. It loads the department's data
        into the form fields.
        
        Args:
            choice: Selected value (optional, can also get from StringVar)
        """
        # Check if selection variable exists
        if not hasattr(self, 'dept_select_var'):
            return
        
        # Get selected value
        selection = self.dept_select_var.get()
        
        # If no selection or default option, clear form
        if not selection or selection == "-- Select a Department --":
            # Remove all widgets from form frame
            for widget in self.form_frame.winfo_children():
                widget.destroy()
            # Clear selected department ID
            self.selected_dept_id = None
            return
        
        try:
            # Extract department ID from selection string
            # "1: IT Department".split(":")[0] = "1"
            dept_id = int(selection.split(":")[0])
            
            # Load department data into form
            self.load_department_for_update(dept_id)
        except (ValueError, IndexError):
            # If parsing fails, show error
            messagebox.showerror("Error", "Invalid selection")
    
    def load_department_for_update(self, dept_id=None):
        """
        Load department data into update form fields.
        
        This method:
        1. Queries database for department data
        2. Clears existing form widgets
        3. Creates new form fields with department data pre-filled
        4. Creates update button that saves changes
        
        Args:
            dept_id: Department ID to load (if None, uses self.selected_dept_id)
        """
        try:
            # Get department ID (use parameter or stored value)
            if dept_id is None:
                # If no ID provided, check if we have stored ID
                if not hasattr(self, 'selected_dept_id') or self.selected_dept_id is None:
                    return  # No department selected, exit
                dept_id = self.selected_dept_id
            else:
                # Store ID for later use
                self.selected_dept_id = dept_id
            
            # Get department data from database
            department = self.department_model.get_by_id(dept_id)
            
            # Check if department exists
            if not department:
                messagebox.showerror("Error", "Department not found")
                return
            
            # Clear existing form widgets
            for widget in self.form_frame.winfo_children():
                widget.destroy()
            
            # Create title label
            ctk.CTkLabel(
                self.form_frame, 
                text="Update Department", 
                font=ctk.CTkFont(size=16, weight="bold")
            ).grid(row=0, column=0, columnspan=2, pady=10)
            
            # ========== CREATE FORM FIELDS WITH PRE-FILLED DATA ==========
            
            # Department Name field
            ctk.CTkLabel(self.form_frame, text="Department Name *:").grid(
                row=1, column=0, sticky="w", pady=5, padx=10
            )
            name_entry = ctk.CTkEntry(self.form_frame, width=300)
            # insert(0, value) adds text at position 0 (beginning)
            name_entry.insert(0, department.get('name', ''))
            name_entry.grid(row=1, column=1, pady=5, padx=10)
            
            # Description field
            ctk.CTkLabel(self.form_frame, text="Description:").grid(
                row=2, column=0, sticky="w", pady=5, padx=10
            )
            description_text = ctk.CTkTextbox(self.form_frame, width=300, height=100)
            # insert("1.0", value) adds text at line 1, character 0
            description_text.insert("1.0", department.get('description') or "")
            description_text.grid(row=2, column=1, pady=5, padx=10)
            
            # Define update function (nested function)
            # This function is called when user clicks "Update Department" button
            def update_department():
                """
                Handle update button click.
                
                This function:
                1. Validates inputs
                2. Gets values from form fields
                3. Calls DepartmentModel.update() to save changes
                4. Shows success/error message
                5. Reloads form with updated data
                """
                try:
                    # Validate department name is not empty
                    if not name_entry.get().strip():
                        messagebox.showerror("Error", "Department name is required")
                        return
                    
                    # Get description from text area
                    description = description_text.get("1.0", "end-1c").strip()
                    
                    # Update department in database
                    self.department_model.update(
                        dept_id=self.selected_dept_id,
                        name=name_entry.get().strip(),
                        description=description
                    )
                    
                    # Show success message
                    messagebox.showinfo("Success", "Department updated successfully!")
                    
                    # Reload department list and form
                    # This refreshes the dropdown and form with latest data
                    self.load_departments_for_selection()
                    self.load_department_for_update(self.selected_dept_id)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update department: {str(e)}")
            
            # Create button frame
            button_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
            button_frame.grid(row=3, column=0, columnspan=2, pady=20)
            
            # Create Update button
            ctk.CTkButton(
                button_frame, 
                text="Update Department", 
                command=update_department, 
                width=120
            ).pack(side="left", padx=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load department: {str(e)}")
    
    def load_departments_for_delete_selection(self):
        """
        Load departments into delete selection dropdown.
        
        Similar to load_departments_for_selection() but for delete form.
        """
        try:
            departments = self.department_model.get_all()
            dept_list = ["-- Select a Department --"] + [
                f"{dept.get('id', '')}: {dept.get('name', '')}"
                for dept in departments
            ]
            if hasattr(self, 'delete_dept_combo'):
                self.delete_dept_combo.configure(values=dept_list)
                if dept_list:
                    self.delete_dept_combo.set(dept_list[0])
        except Exception:
            pass
    
    def on_delete_department_selected(self, choice=None):
        """
        Handle department selection from delete dropdown.
        
        Called when user selects a department to delete.
        Loads department information and enables delete button.
        """
        if not hasattr(self, 'delete_dept_var'):
            return
        
        selection = self.delete_dept_var.get()
        if not selection or selection == "-- Select a Department --":
            # Clear info and disable button
            self.delete_info_label.configure(text="")
            self.delete_button.configure(state="disabled")
            self.delete_dept_id = None
            return
        
        try:
            # Extract department ID
            dept_id = int(selection.split(":")[0])
            # Load department for deletion
            self.load_department_for_delete(dept_id)
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Invalid selection")
    
    def load_department_for_delete(self, dept_id):
        """
        Load department information for deletion confirmation.
        
        This method displays department details so user can confirm
        they're deleting the right department. It also checks if the
        department has employees and shows a warning.
        
        Args:
            dept_id: Department ID to load
        """
        try:
            # Get department data
            department = self.department_model.get_by_id(dept_id)
            
            if not department:
                messagebox.showerror("Error", "Department not found")
                # Clear info and disable button
                self.delete_info_label.configure(text="")
                self.delete_button.configure(state="disabled")
                return
            
            # Check if department has employees
            # has_employees() returns True if any employees belong to this department
            has_employees = self.department_model.has_employees(dept_id)
            
            # Create warning text if department has employees
            # This warns user that deleting will affect employees
            warning_text = "\n⚠ Warning: This department has employees assigned to it!" if has_employees else ""
            
            # Format department information for display
            info_text = (
                f"ID: {department.get('id', 'N/A')}\n"
                f"Name: {department.get('name', 'N/A')}\n"
                f"Description: {department.get('description') or 'N/A'}{warning_text}"
            )
            
            # Display department info
            self.delete_info_label.configure(text=info_text)
            
            # Enable delete button (user can now delete)
            self.delete_button.configure(state="normal")
            
            # Store department ID for deletion
            self.delete_dept_id = dept_id
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load department: {str(e)}")
    
    def delete_department(self):
        """
        Delete selected department from database.
        
        This method:
        1. Checks if department has employees (shows warning)
        2. Confirms deletion with user
        3. Calls DepartmentModel.delete() to remove from database
        4. Shows success/error message
        5. Resets form
        
        Note: If department has employees, their department_id will be set to NULL
        (due to foreign key constraint ON DELETE SET NULL).
        """
        # Check if department is selected
        if not hasattr(self, 'delete_dept_id') or self.delete_dept_id is None:
            return
        
        # Check if department has employees
        has_employees = self.department_model.has_employees(self.delete_dept_id)
        
        # Create warning message if department has employees
        warning = ""
        if has_employees:
            warning = "\n\nThis department has employees. Their department will be set to NULL."
        
        # Confirm deletion with user
        # askyesno() shows Yes/No dialog, returns True if Yes
        if messagebox.askyesno(
            "Confirm Delete", 
            f"Are you sure you want to delete this department?{warning}"
        ):
            try:
                # Delete department from database
                self.department_model.delete(self.delete_dept_id)
                
                # Show success message
                messagebox.showinfo("Success", "Department deleted successfully!")
                
                # Clear info label
                self.delete_info_label.configure(text="")
                
                # Disable delete button
                self.delete_button.configure(state="disabled")
                
                # Clear department ID
                self.delete_dept_id = None
                
                # Reload department list in dropdown
                self.load_departments_for_delete_selection()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete department: {str(e)}")
    
    def load_departments(self):
        """
        Load all departments into the table view.
        
        This method:
        1. Queries database for all departments
        2. Clears existing table rows
        3. Adds each department as a row in the table
        
        Used in "view" mode to display department list.
        """
        try:
            # Check if tree widget exists
            if hasattr(self, 'tree'):
                # Clear existing rows
                # get_children() returns list of all row IDs
                for item in self.tree.get_children():
                    # delete() removes a row from table
                    self.tree.delete(item)
                
                # Get all departments from database
                departments = self.department_model.get_all()
                
                # Add each department as a row
                for dept in departments:
                    try:
                        # Extract department data
                        dept_id = dept.get('id', 'N/A')
                        name = dept.get('name', 'N/A')
                        desc = dept.get('description') or "N/A"
                        created = dept.get('created_at') or "N/A"
                        
                        # Insert row into table
                        # insert() adds a new row
                        # "" means root (top level)
                        # "end" means add at end
                        # values=() provides the data for each column
                        self.tree.insert(
                            "", 
                            "end", 
                            values=(dept_id, name, desc, created)
                        )
                    except Exception:
                        # Skip this department if error occurs (prevents crash)
                        continue
        except Exception:
            # Silently fail if error occurs
            pass
