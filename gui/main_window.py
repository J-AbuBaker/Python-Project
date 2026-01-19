"""Main application window."""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from auth.auth_manager import AuthManager
from gui.employee_form import EmployeeForm
from gui.department_form import DepartmentForm
from gui.report_window import ReportWindow


class MainWindow:
    """Main application window with menu system."""
    
    def __init__(self, root, auth_manager, employee_model, department_model, db_manager):
        """Initialize main window."""
        self.root = root
        self.auth_manager = auth_manager
        self.employee_model = employee_model
        self.department_model = department_model
        self.db_manager = db_manager
        
        self.root.title("Smart Records System")
        self.root.geometry("1000x700")
        
        self.create_menu()
        self.create_widgets()
        
        current_user = self.auth_manager.get_current_user()
        if current_user:
            username = current_user.get('username', 'User')
            messagebox.showinfo("Welcome", f"Welcome, {username}!\n\nUse the menu bar to navigate through the system.")
    
    def create_menu(self):
        """Create menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        employees_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Employees", menu=employees_menu)
        employees_menu.add_command(label="Add Employee", command=self.add_employee)
        employees_menu.add_command(label="View All Employees", command=self.view_employees)
        employees_menu.add_command(label="Search Employees", command=self.search_employees)
        employees_menu.add_separator()
        employees_menu.add_command(label="Update Employee", command=self.update_employee)
        employees_menu.add_command(label="Delete Employee", command=self.delete_employee)
        
        departments_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Departments", menu=departments_menu)
        departments_menu.add_command(label="Add Department", command=self.add_department)
        departments_menu.add_command(label="View All Departments", command=self.view_departments)
        departments_menu.add_separator()
        departments_menu.add_command(label="Update Department", command=self.update_department)
        departments_menu.add_command(label="Delete Department", command=self.delete_department)
        
        reports_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Reports", menu=reports_menu)
        reports_menu.add_command(label="Generate Reports", command=self.show_reports)
        reports_menu.add_command(label="Export to PDF", command=self.export_pdf)
        reports_menu.add_command(label="Export to TXT", command=self.export_txt)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
        menubar.add_command(label="Logout", command=self.logout)
    
    def create_widgets(self):
        """Create main window widgets."""
        self.status_bar = ctk.CTkLabel(self.root, text="Ready", anchor="w", padx=10, pady=5, fg_color=("gray75", "gray25"))
        self.status_bar.pack(side="bottom", fill="x")
        
        current_user = self.auth_manager.get_current_user()
        if current_user:
            username = current_user.get('username', 'User') if current_user else 'User'
            self.status_bar.configure(text=f"Logged in as: {username} | Ready")
        
        self.content_frame = ctk.CTkFrame(self.root)
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        welcome_label = ctk.CTkLabel(
            self.content_frame,
            text="Smart Records System",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        welcome_label.pack(pady=50)
        
        info_label = ctk.CTkLabel(
            self.content_frame,
            text="Use the menu bar to manage employees, departments, and generate reports.",
            font=ctk.CTkFont(size=12)
        )
        info_label.pack(pady=20)
    
    def clear_content(self):
        """Clear the main content area."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def add_employee(self):
        """Open add employee form."""
        self.clear_content()
        form = EmployeeForm(self.content_frame, self.employee_model, 
                          self.department_model, mode="add")
        form.pack(fill="both", expand=True)
        self.status_bar.configure(text="Add Employee")
    
    def view_employees(self):
        """View all employees."""
        self.clear_content()
        form = EmployeeForm(self.content_frame, self.employee_model,
                          self.department_model, mode="view")
        form.pack(fill="both", expand=True)
        self.status_bar.configure(text="View All Employees")
    
    def search_employees(self):
        """Search employees."""
        self.clear_content()
        form = EmployeeForm(self.content_frame, self.employee_model,
                          self.department_model, mode="search")
        form.pack(fill="both", expand=True)
        self.status_bar.configure(text="Search Employees")
    
    def update_employee(self):
        """Update employee."""
        self.clear_content()
        form = EmployeeForm(self.content_frame, self.employee_model,
                          self.department_model, mode="update")
        form.pack(fill="both", expand=True)
        self.status_bar.configure(text="Update Employee")
    
    def delete_employee(self):
        """Delete employee."""
        self.clear_content()
        form = EmployeeForm(self.content_frame, self.employee_model,
                          self.department_model, mode="delete")
        form.pack(fill="both", expand=True)
        self.status_bar.configure(text="Delete Employee")
    
    def add_department(self):
        """Open add department form."""
        self.clear_content()
        form = DepartmentForm(self.content_frame, self.department_model, mode="add")
        form.pack(fill="both", expand=True)
        self.status_bar.configure(text="Add Department")
    
    def view_departments(self):
        """View all departments."""
        self.clear_content()
        form = DepartmentForm(self.content_frame, self.department_model, mode="view")
        form.pack(fill="both", expand=True)
        self.status_bar.configure(text="View All Departments")
    
    def update_department(self):
        """Update department."""
        self.clear_content()
        form = DepartmentForm(self.content_frame, self.department_model, mode="update")
        form.pack(fill="both", expand=True)
        self.status_bar.configure(text="Update Department")
    
    def delete_department(self):
        """Delete department."""
        self.clear_content()
        form = DepartmentForm(self.content_frame, self.department_model, mode="delete")
        form.pack(fill="both", expand=True)
        self.status_bar.configure(text="Delete Department")
    
    def show_reports(self):
        """Show reports window."""
        self.clear_content()
        report_window = ReportWindow(self.content_frame, self.employee_model,
                                    self.department_model, self.db_manager)
        report_window.pack(fill="both", expand=True)
        self.status_bar.configure(text="Generate Reports")
    
    def export_pdf(self):
        """Export reports to PDF."""
        from reports.report_generator import ReportGenerator
        generator = ReportGenerator(self.employee_model, self.department_model)
        
        try:
            filename = generator.export_to_pdf()
            messagebox.showinfo("Success", f"Report exported to {filename}")
            self.status_bar.configure(text=f"Report exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export PDF: {str(e)}")
    
    def export_txt(self):
        """Export reports to TXT."""
        from reports.report_generator import ReportGenerator
        generator = ReportGenerator(self.employee_model, self.department_model)
        
        try:
            filename = generator.export_to_txt()
            messagebox.showinfo("Success", f"Report exported to {filename}")
            self.status_bar.configure(text=f"Report exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export TXT: {str(e)}")
    
    def show_about(self):
        """Show about dialog."""
        messagebox.showinfo(
            "About Smart Records System",
            "Smart Records System v1.0\n\n"
            "A GUI-based database application for managing\n"
            "employee and department records.\n\n"
            "Features:\n"
            "- User authentication\n"
            "- CRUD operations\n"
            "- Report generation\n"
            "- PDF and TXT export"
        )
    
    def logout(self):
        """Handle logout."""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.auth_manager.logout()
            self.root.quit()

