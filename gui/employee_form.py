"""Employee management forms."""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from utils.validators import validate_email, validate_phone, validate_required, validate_salary, validate_date


class EmployeeForm(ctk.CTkScrollableFrame):
    """Employee CRUD form."""
    
    def __init__(self, parent, employee_model, department_model, mode="view"):
        """
        Initialize employee form.
        
        Args:
            parent: Parent widget
            employee_model: EmployeeModel instance
            department_model: DepartmentModel instance
            mode: Form mode ('add', 'view', 'update', 'delete', 'search')
        """
        super().__init__(parent)
        self.employee_model = employee_model
        self.department_model = department_model
        self.mode = mode
        
        self.create_widgets()
        
        if mode == "view":
            self.load_employees()
        elif mode == "search":
            self.show_search_interface()
    
    def create_widgets(self):
        """Create form widgets."""
        if self.mode == "add":
            self.create_add_form()
        elif self.mode == "update":
            self.create_update_form()
        elif self.mode == "delete":
            self.create_delete_form()
        elif self.mode == "view":
            self.create_view_list()
        elif self.mode == "search":
            pass
    
    def create_add_form(self):
        """Create add employee form."""
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(form_frame, text="Add New Employee", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        ctk.CTkLabel(form_frame, text="First Name *:").grid(row=1, column=0, sticky="w", pady=5, padx=10)
        self.first_name_entry = ctk.CTkEntry(form_frame, width=250)
        self.first_name_entry.grid(row=1, column=1, pady=5, padx=10)
        
        ctk.CTkLabel(form_frame, text="Last Name *:").grid(row=2, column=0, sticky="w", pady=5, padx=10)
        self.last_name_entry = ctk.CTkEntry(form_frame, width=250)
        self.last_name_entry.grid(row=2, column=1, pady=5, padx=10)
        
        ctk.CTkLabel(form_frame, text="Email *:").grid(row=3, column=0, sticky="w", pady=5, padx=10)
        self.email_entry = ctk.CTkEntry(form_frame, width=250)
        self.email_entry.grid(row=3, column=1, pady=5, padx=10)
        
        ctk.CTkLabel(form_frame, text="Phone:").grid(row=4, column=0, sticky="w", pady=5, padx=10)
        self.phone_entry = ctk.CTkEntry(form_frame, width=250)
        self.phone_entry.grid(row=4, column=1, pady=5, padx=10)
        
        ctk.CTkLabel(form_frame, text="Position:").grid(row=5, column=0, sticky="w", pady=5, padx=10)
        self.position_entry = ctk.CTkEntry(form_frame, width=250)
        self.position_entry.grid(row=5, column=1, pady=5, padx=10)
        
        ctk.CTkLabel(form_frame, text="Salary:").grid(row=6, column=0, sticky="w", pady=5, padx=10)
        self.salary_entry = ctk.CTkEntry(form_frame, width=250)
        self.salary_entry.grid(row=6, column=1, pady=5, padx=10)
        
        ctk.CTkLabel(form_frame, text="Department:").grid(row=7, column=0, sticky="w", pady=5, padx=10)
        self.department_var = tk.StringVar()
        self.department_combo = ctk.CTkComboBox(form_frame, variable=self.department_var, width=250, state="readonly")
        self.department_combo.grid(row=7, column=1, pady=5, padx=10)
        self.load_departments()
        
        ctk.CTkLabel(form_frame, text="Hire Date (YYYY-MM-DD):").grid(row=8, column=0, sticky="w", pady=5, padx=10)
        self.hire_date_entry = ctk.CTkEntry(form_frame, width=250)
        self.hire_date_entry.grid(row=8, column=1, pady=5, padx=10)
        
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=9, column=0, columnspan=2, pady=20)
        
        ctk.CTkButton(button_frame, text="Add Employee", command=self.save_employee, width=120).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Clear", command=self.clear_form, width=120).pack(side="left", padx=5)
    
    def create_update_form(self):
        """Create update employee form."""
        select_frame = ctk.CTkFrame(self)
        select_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(select_frame, text="Select Employee to Update", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
        
        selection_input_frame = ctk.CTkFrame(select_frame, fg_color="transparent")
        selection_input_frame.pack(pady=5)
        
        ctk.CTkLabel(selection_input_frame, text="Employee:").pack(side="left", padx=5)
        self.emp_select_var = tk.StringVar()
        self.emp_select_combo = ctk.CTkComboBox(selection_input_frame, variable=self.emp_select_var, 
                                                width=300, state="readonly", command=self.on_employee_selected)
        self.emp_select_combo.pack(side="left", padx=5)
        
        self.load_employees_for_selection()
        
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.selected_emp_id = None
    
    def create_delete_form(self):
        """Create delete employee form."""
        delete_frame = ctk.CTkFrame(self)
        delete_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(delete_frame, text="Delete Employee", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        ctk.CTkLabel(delete_frame, text="Select Employee:").grid(row=1, column=0, sticky="w", pady=5, padx=10)
        self.delete_emp_var = tk.StringVar()
        self.delete_emp_combo = ctk.CTkComboBox(delete_frame, variable=self.delete_emp_var, 
                                              width=350, state="readonly", command=self.on_delete_employee_selected)
        self.delete_emp_combo.grid(row=1, column=1, pady=5, padx=10, sticky="ew")
        delete_frame.grid_columnconfigure(1, weight=1)
        
        self.load_employees_for_delete_selection()
        
        self.delete_info_label = ctk.CTkLabel(delete_frame, text="", font=ctk.CTkFont(size=12))
        self.delete_info_label.grid(row=2, column=0, columnspan=2, pady=20)
        
        self.delete_button = ctk.CTkButton(delete_frame, text="Delete Employee", 
                                       command=self.delete_employee, state="disabled", width=200)
        self.delete_button.grid(row=3, column=0, columnspan=2, pady=10)
        self.delete_emp_id = None
    
    def create_view_list(self):
        """Create employee list view."""
        list_frame = ctk.CTkFrame(self)
        list_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(list_frame, text="All Employees", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        tree_container = ctk.CTkFrame(list_frame)
        tree_container.pack(fill="both", expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_container)
        scrollbar.pack(side="right", fill="y")
        
        self.tree = ttk.Treeview(tree_container, columns=("ID", "Name", "Email", "Phone", "Position", "Salary", "Department", "Hire Date"),
                                show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Position", text="Position")
        self.tree.heading("Salary", text="Salary")
        self.tree.heading("Department", text="Department")
        self.tree.heading("Hire Date", text="Hire Date")
        
        self.tree.column("ID", width=50)
        self.tree.column("Name", width=150)
        self.tree.column("Email", width=150)
        self.tree.column("Phone", width=100)
        self.tree.column("Position", width=100)
        self.tree.column("Salary", width=100)
        self.tree.column("Department", width=120)
        self.tree.column("Hire Date", width=100)
        
        self.tree.pack(fill="both", expand=True)
    
    def show_search_interface(self):
        """Show search interface."""
        search_frame = ctk.CTkFrame(self)
        search_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(search_frame, text="Search Employees", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
        
        search_input_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
        search_input_frame.pack(pady=5)
        
        ctk.CTkLabel(search_input_frame, text="Search:").pack(side="left", padx=5)
        self.search_entry = ctk.CTkEntry(search_input_frame, width=250)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind('<Return>', lambda e: self.search_employees())
        ctk.CTkButton(search_input_frame, text="Search", command=self.search_employees, width=100).pack(side="left", padx=5)
        
        results_frame = ctk.CTkFrame(self)
        results_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(results_frame, text="Search Results", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
        
        tree_container = ctk.CTkFrame(results_frame)
        tree_container.pack(fill="both", expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_container)
        scrollbar.pack(side="right", fill="y")
        
        self.search_tree = ttk.Treeview(tree_container, columns=("ID", "Name", "Email", "Phone", "Position", "Salary", "Department"),
                                       show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.search_tree.yview)
        
        for col in ("ID", "Name", "Email", "Phone", "Position", "Salary", "Department"):
            self.search_tree.heading(col, text=col)
            self.search_tree.column(col, width=120)
        
        self.search_tree.pack(fill="both", expand=True)
    
    def load_departments(self):
        """Load departments into combobox."""
        try:
            departments = self.department_model.get_all()
            dept_list = ["None"] + [f"{d.get('id', '')}: {d.get('name', '')}" for d in departments]
            if hasattr(self, 'department_combo'):
                self.department_combo.configure(values=dept_list)
                if dept_list:
                    self.department_combo.set("None")
        except Exception:
            pass
    
    def get_selected_department_id(self):
        """Get selected department ID from combobox."""
        selection = self.department_var.get()
        if not selection or selection == "None":
            return None
        try:
            return int(selection.split(":")[0])
        except (ValueError, IndexError, AttributeError):
            return None
    
    def validate_form(self):
        """Validate form inputs."""
        valid, msg = validate_required(self.first_name_entry.get(), "First name")
        if not valid:
            return False, msg
        
        valid, msg = validate_required(self.last_name_entry.get(), "Last name")
        if not valid:
            return False, msg
        
        email = self.email_entry.get().strip()
        valid, msg = validate_required(email, "Email")
        if not valid:
            return False, msg
        
        if not validate_email(email):
            return False, "Invalid email format"
        
        phone = self.phone_entry.get().strip()
        if phone and not validate_phone(phone):
            return False, "Invalid phone number format"
        
        salary_str = self.salary_entry.get().strip()
        if salary_str:
            valid, msg, _ = validate_salary(salary_str)
            if not valid:
                return False, msg
        
        hire_date = self.hire_date_entry.get().strip()
        if hire_date:
            valid, msg = validate_date(hire_date)
            if not valid:
                return False, msg
        
        return True, ""
    
    def save_employee(self):
        """Save new employee."""
        valid, error_msg = self.validate_form()
        if not valid:
            messagebox.showerror("Validation Error", error_msg)
            return
        
        try:
            salary_str = self.salary_entry.get().strip()
            valid, _, salary = validate_salary(salary_str)
            salary = salary if valid else 0.0
            
            dept_id = self.get_selected_department_id()
            hire_date = self.hire_date_entry.get().strip()
            
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
            
            messagebox.showinfo("Success", "Employee added successfully!")
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add employee: {str(e)}")
    
    def clear_form(self):
        """Clear form fields."""
        self.first_name_entry.delete(0, "end")
        self.last_name_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.phone_entry.delete(0, "end")
        self.position_entry.delete(0, "end")
        self.salary_entry.delete(0, "end")
        self.hire_date_entry.delete(0, "end")
        if hasattr(self, 'department_combo'):
            self.department_combo.set("None")
    
    def load_employees_for_selection(self):
        """Load employees into selection dropdown."""
        try:
            employees = self.employee_model.get_all()
            emp_list = ["-- Select an Employee --"] + [
                f"{emp.get('id', '')}: {emp.get('first_name', '')} {emp.get('last_name', '')} ({emp.get('email', '')})"
                for emp in employees
            ]
            if hasattr(self, 'emp_select_combo'):
                self.emp_select_combo.configure(values=emp_list)
                if emp_list:
                    self.emp_select_combo.set(emp_list[0])
        except Exception:
            pass
    
    def on_employee_selected(self, choice=None):
        """Handle employee selection from dropdown."""
        if not hasattr(self, 'emp_select_var'):
            return
        
        selection = self.emp_select_var.get()
        if not selection or selection == "-- Select an Employee --":
            for widget in self.form_frame.winfo_children():
                widget.destroy()
            self.selected_emp_id = None
            return
        
        try:
            emp_id = int(selection.split(":")[0])
            self.load_employee_for_update(emp_id)
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Invalid selection")
    
    def load_employee_for_update(self, emp_id=None):
        """Load employee data for updating."""
        try:
            if emp_id is None:
                if not hasattr(self, 'selected_emp_id') or self.selected_emp_id is None:
                    return
                emp_id = self.selected_emp_id
            else:
                self.selected_emp_id = emp_id
            
            employee = self.employee_model.get_by_id(emp_id)
            
            if not employee:
                messagebox.showerror("Error", "Employee not found")
                return
            
            # Clear existing form widgets and rebuild with selected employee data
            for widget in self.form_frame.winfo_children():
                widget.destroy()
            
            ctk.CTkLabel(self.form_frame, text="Update Employee", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=2, pady=10)
            
            ctk.CTkLabel(self.form_frame, text="First Name *:").grid(row=1, column=0, sticky="w", pady=5, padx=10)
            first_name_entry = ctk.CTkEntry(self.form_frame, width=250)
            first_name_entry.insert(0, employee.get('first_name', ''))
            first_name_entry.grid(row=1, column=1, pady=5, padx=10)
            
            ctk.CTkLabel(self.form_frame, text="Last Name *:").grid(row=2, column=0, sticky="w", pady=5, padx=10)
            last_name_entry = ctk.CTkEntry(self.form_frame, width=250)
            last_name_entry.insert(0, employee.get('last_name', ''))
            last_name_entry.grid(row=2, column=1, pady=5, padx=10)
            
            ctk.CTkLabel(self.form_frame, text="Email *:").grid(row=3, column=0, sticky="w", pady=5, padx=10)
            email_entry = ctk.CTkEntry(self.form_frame, width=250)
            email_entry.insert(0, employee.get('email', ''))
            email_entry.grid(row=3, column=1, pady=5, padx=10)
            
            ctk.CTkLabel(self.form_frame, text="Phone:").grid(row=4, column=0, sticky="w", pady=5, padx=10)
            phone_entry = ctk.CTkEntry(self.form_frame, width=250)
            phone_entry.insert(0, employee.get('phone') or "")
            phone_entry.grid(row=4, column=1, pady=5, padx=10)
            
            ctk.CTkLabel(self.form_frame, text="Position:").grid(row=5, column=0, sticky="w", pady=5, padx=10)
            position_entry = ctk.CTkEntry(self.form_frame, width=250)
            position_entry.insert(0, employee.get('position') or "")
            position_entry.grid(row=5, column=1, pady=5, padx=10)
            
            ctk.CTkLabel(self.form_frame, text="Salary:").grid(row=6, column=0, sticky="w", pady=5, padx=10)
            salary_entry = ctk.CTkEntry(self.form_frame, width=250)
            salary_entry.insert(0, str(employee.get('salary') or 0))
            salary_entry.grid(row=6, column=1, pady=5, padx=10)
            
            ctk.CTkLabel(self.form_frame, text="Department:").grid(row=7, column=0, sticky="w", pady=5, padx=10)
            dept_var = tk.StringVar()
            dept_combo = ctk.CTkComboBox(self.form_frame, variable=dept_var, width=250, state="readonly")
            departments = self.department_model.get_all()
            dept_list = ["None"] + [f"{d.get('id', '')}: {d.get('name', '')}" for d in departments]
            dept_combo.configure(values=dept_list)
            # Match employee's current department in dropdown (enumerate starts at 1 to skip "None")
            dept_id = employee.get('department_id')
            if dept_id:
                for i, d in enumerate(departments, 1):
                    if d.get('id') == dept_id:
                        dept_combo.set(dept_list[i])
                        break
                else:
                    dept_combo.set("None")
            else:
                dept_combo.set("None")
            dept_combo.grid(row=7, column=1, pady=5, padx=10)
            
            ctk.CTkLabel(self.form_frame, text="Hire Date (YYYY-MM-DD):").grid(row=8, column=0, sticky="w", pady=5, padx=10)
            hire_date_entry = ctk.CTkEntry(self.form_frame, width=250)
            hire_date_entry.insert(0, employee.get('hire_date') or "")
            hire_date_entry.grid(row=8, column=1, pady=5, padx=10)
            
            def update_employee():
                try:
                    salary_str = salary_entry.get().strip()
                    valid, _, salary = validate_salary(salary_str)
                    salary = salary if valid else 0.0
                    
                    dept_selection = dept_var.get()
                    dept_id = None if not dept_selection or dept_selection == "None" else int(dept_selection.split(":")[0])
                    
                    if not first_name_entry.get().strip():
                        messagebox.showerror("Error", "First name is required")
                        return
                    if not last_name_entry.get().strip():
                        messagebox.showerror("Error", "Last name is required")
                        return
                    email = email_entry.get().strip()
                    if not email:
                        messagebox.showerror("Error", "Email is required")
                        return
                    if not validate_email(email):
                        messagebox.showerror("Error", "Invalid email format")
                        return
                    
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
                    messagebox.showinfo("Success", "Employee updated successfully!")
                    self.load_employees_for_selection()
                    self.load_employee_for_update(self.selected_emp_id)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update employee: {str(e)}")
            
            button_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
            button_frame.grid(row=9, column=0, columnspan=2, pady=20)
            ctk.CTkButton(button_frame, text="Update Employee", command=update_employee, width=120).pack(side="left", padx=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load employee: {str(e)}")
    
    def load_employees_for_delete_selection(self):
        """Load employees into delete selection dropdown."""
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
        """Handle employee selection for deletion."""
        if not hasattr(self, 'delete_emp_var'):
            return
        
        selection = self.delete_emp_var.get()
        if not selection or selection == "-- Select an Employee --":
            self.delete_info_label.configure(text="")
            self.delete_button.configure(state="disabled")
            self.delete_emp_id = None
            return
        
        try:
            emp_id = int(selection.split(":")[0])
            self.load_employee_for_delete(emp_id)
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Invalid selection")
    
    def load_employee_for_delete(self, emp_id):
        """Load employee for deletion."""
        try:
            employee = self.employee_model.get_by_id(emp_id)
            
            if not employee:
                messagebox.showerror("Error", "Employee not found")
                self.delete_info_label.configure(text="")
                self.delete_button.configure(state="disabled")
                return
            
            info_text = (f"ID: {employee.get('id', 'N/A')}\n"
                        f"Name: {employee.get('first_name', '')} {employee.get('last_name', '')}\n"
                        f"Email: {employee.get('email', 'N/A')}\n"
                        f"Position: {employee.get('position') or 'N/A'}\n"
                        f"Department: {employee.get('department_name', 'N/A')}")
            
            self.delete_info_label.configure(text=info_text)
            self.delete_button.configure(state="normal")
            self.delete_emp_id = emp_id
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load employee: {str(e)}")
    
    def delete_employee(self):
        """Delete employee."""
        if not hasattr(self, 'delete_emp_id') or self.delete_emp_id is None:
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this employee?"):
            try:
                self.employee_model.delete(self.delete_emp_id)
                messagebox.showinfo("Success", "Employee deleted successfully!")
                self.delete_info_label.configure(text="")
                self.delete_button.configure(state="disabled")
                self.delete_emp_id = None
                self.load_employees_for_delete_selection()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete employee: {str(e)}")
    
    def load_employees(self):
        """Load all employees into treeview."""
        try:
            if hasattr(self, 'tree'):
                for item in self.tree.get_children():
                    self.tree.delete(item)
                
                employees = self.employee_model.get_all()
                for emp in employees:
                    try:
                        emp_id = emp.get('id', 'N/A')
                        name = f"{emp.get('first_name', '')} {emp.get('last_name', '')}".strip()
                        email = emp.get('email', 'N/A')
                        phone = emp.get('phone') or "N/A"
                        position = emp.get('position') or "N/A"
                        salary_val = emp.get('salary')
                        salary = f"${salary_val:.2f}" if salary_val is not None and salary_val != 0 else "N/A"
                        dept = emp.get('department_name', 'N/A')
                        hire_date = emp.get('hire_date') or "N/A"
                        
                        self.tree.insert("", "end", values=(emp_id, name, email, phone, position, salary, dept, hire_date))
                    except Exception:
                        continue
        except Exception:
            pass
    
    def search_employees(self):
        """Search employees."""
        search_term = self.search_entry.get().strip()
        if not search_term:
            messagebox.showwarning("Warning", "Please enter a search term")
            return
        
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)
        
        employees = self.employee_model.search(search_term)
        for emp in employees:
            try:
                emp_id = emp.get('id', 'N/A')
                name = f"{emp.get('first_name', '')} {emp.get('last_name', '')}".strip()
                email = emp.get('email', 'N/A')
                phone = emp.get('phone') or "N/A"
                position = emp.get('position') or "N/A"
                # Format salary with currency symbol, or show N/A if zero/None
                salary_val = emp.get('salary')
                salary = f"${salary_val:.2f}" if salary_val is not None and salary_val != 0 else "N/A"
                dept = emp.get('department_name', 'N/A')
                
                self.search_tree.insert("", "end", values=(
                    emp_id, name, email, phone, position, salary, dept
                ))
            except Exception:
                continue

