"""
Main Application Window - Smart Records System

This module creates the main application window that appears after successful login.
It provides a menu bar for accessing all features and a content area that displays
different forms based on user selection.

The main window includes:
- Menu bar with Employees, Departments, Reports, Help menus
- Status bar showing current user and status messages
- Content area that displays forms (employee forms, department forms, reports)
- Welcome screen when first opened

GUI CONCEPTS EXPLAINED:
- Menu bar: Horizontal menu at top of window (File, Edit, etc.)
- Status bar: Information bar at bottom showing current status
- Content frame: Main area that displays different forms
- Menu items: Clickable menu options that trigger actions
- clear_content(): Removes old widgets before showing new ones
"""

# Import CustomTkinter for modern GUI widgets
import customtkinter as ctk

# Import tkinter for menu bar (CustomTkinter doesn't have native menu support)
# tk.Menu is used for creating menu bars
import tkinter as tk

# Import messagebox for showing popup dialogs
from tkinter import messagebox

# Import AuthManager for logout functionality
from auth.auth_manager import AuthManager

# Import form classes - these create the actual forms displayed in content area
from gui.employee_form import EmployeeForm
from gui.department_form import DepartmentForm
from gui.report_window import ReportWindow


class MainWindow:
    """
    Main Application Window Class
    
    This class creates and manages the main application window. It:
    - Creates menu bar with all features
    - Manages content area (shows different forms)
    - Displays status bar with user info
    - Coordinates between different parts of the application
    
    The window acts as a "container" - it doesn't do the actual work,
    but coordinates other components (forms, models, etc.).
    """
    
    def __init__(self, root, auth_manager, employee_model, department_model, db_manager):
        """
        Initialize the main application window.
        
        This method sets up the window, creates menu bar, and shows welcome screen.
        
        Args:
            root: The main window (CTk root window)
            auth_manager: AuthManager instance - for logout and user info
            employee_model: EmployeeModel instance - for employee operations
            department_model: DepartmentModel instance - for department operations
            db_manager: DatabaseManager instance - for database operations
        """
        # Store reference to root window
        # This is the main application window container
        self.root = root
        
        # Store references to managers and models
        # These are used by forms to perform operations
        self.auth_manager = auth_manager
        self.employee_model = employee_model
        self.department_model = department_model
        self.db_manager = db_manager
        
        # Set window title (appears in title bar)
        self.root.title("Smart Records System")
        
        # Set window size (1000 pixels wide, 700 pixels tall)
        # This is a good size for displaying forms and data tables
        self.root.geometry("1000x700")
        
        # Create menu bar (horizontal menu at top)
        # This must be created before other widgets
        self.create_menu()
        
        # Create main widgets (status bar, content area, welcome screen)
        self.create_widgets()
        
        # Get current logged-in user
        # get_current_user() returns dict with user info or None
        current_user = self.auth_manager.get_current_user()
        
        # If user is logged in, show welcome message
        if current_user:
            # Extract username from user dict
            # .get() safely gets 'username' key, uses 'User' as default if not found
            username = current_user.get('username', 'User')
            
            # Show welcome popup dialog
            # showinfo() displays an information dialog
            # \n\n creates blank lines for better formatting
            messagebox.showinfo(
                "Welcome", 
                f"Welcome, {username}!\n\nUse the menu bar to navigate through the system."
            )
    
    def create_menu(self):
        """
        Create the menu bar at the top of the window.
        
        The menu bar contains:
        - Employees menu (Add, View, Search, Update, Delete)
        - Departments menu (Add, View, Update, Delete)
        - Reports menu (Generate, Export PDF, Export TXT)
        - Help menu (About)
        - Logout button
        
        Menu bars use tkinter's Menu widget (not CustomTkinter).
        """
        # Create main menu bar
        # tk.Menu creates a menu bar widget
        # tearoff=0 prevents menu from being "torn off" (detached)
        menubar = tk.Menu(self.root, tearoff=0)
        
        # Attach menu bar to root window
        # config(menu=menubar) sets this as the window's menu bar
        self.root.config(menu=menubar)
        
        # ========== EMPLOYEES MENU ==========
        # Create Employees submenu
        # This will contain all employee-related actions
        employees_menu = tk.Menu(menubar, tearoff=0)
        
        # Add Employees menu to menu bar
        # add_cascade() creates a dropdown menu
        # label="Employees" is what appears in menu bar
        menubar.add_cascade(label="Employees", menu=employees_menu)
        
        # Add menu items to Employees menu
        # add_command() adds a clickable menu item
        # command=self.add_employee calls the method when clicked
        employees_menu.add_command(label="Add Employee", command=self.add_employee)
        employees_menu.add_command(label="View All Employees", command=self.view_employees)
        employees_menu.add_command(label="Search Employees", command=self.search_employees)
        
        # Add separator line (visual divider)
        # add_separator() draws a horizontal line in the menu
        employees_menu.add_separator()
        
        # Add update and delete options (separated from view/search)
        employees_menu.add_command(label="Update Employee", command=self.update_employee)
        employees_menu.add_command(label="Delete Employee", command=self.delete_employee)
        
        # ========== DEPARTMENTS MENU ==========
        # Create Departments submenu
        departments_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Departments", menu=departments_menu)
        
        # Add department menu items
        departments_menu.add_command(label="Add Department", command=self.add_department)
        departments_menu.add_command(label="View All Departments", command=self.view_departments)
        departments_menu.add_separator()
        departments_menu.add_command(label="Update Department", command=self.update_department)
        departments_menu.add_command(label="Delete Department", command=self.delete_department)
        
        # ========== REPORTS MENU ==========
        # Create Reports submenu
        reports_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Reports", menu=reports_menu)
        
        # Add report menu items
        reports_menu.add_command(label="Generate Reports", command=self.show_reports)
        reports_menu.add_command(label="Export to PDF", command=self.export_pdf)
        reports_menu.add_command(label="Export to TXT", command=self.export_txt)
        
        # ========== HELP MENU ==========
        # Create Help submenu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
        # ========== LOGOUT BUTTON ==========
        # Add logout as a direct menu item (not in submenu)
        # This makes it easily accessible
        menubar.add_command(label="Logout", command=self.logout)
    
    def create_widgets(self):
        """
        Create main window widgets.
        
        This method creates:
        - Status bar (at bottom, shows current user and status)
        - Content frame (main area that displays forms)
        - Welcome screen (initial content)
        """
        # Create status bar (information bar at bottom of window)
        # CTkLabel creates a text label widget
        # text="Ready" is the initial status message
        # anchor="w" aligns text to west (left side)
        # padx=10, pady=5 adds padding (space around text)
        # fg_color sets foreground color (background color of label)
        # ("gray75", "gray25") means light gray in light mode, dark gray in dark mode
        self.status_bar = ctk.CTkLabel(
            self.root, 
            text="Ready", 
            anchor="w", 
            padx=10, 
            pady=5, 
            fg_color=("gray75", "gray25")
        )
        
        # Pack status bar at bottom of window
        # side="bottom" places widget at bottom
        # fill="x" makes it fill entire width
        self.status_bar.pack(side="bottom", fill="x")
        
        # Update status bar with current user info
        # Get current logged-in user
        current_user = self.auth_manager.get_current_user()
        
        # If user is logged in, show username in status bar
        if current_user:
            # Extract username safely
            # Ternary operator: use username if current_user exists, else 'User'
            username = current_user.get('username', 'User') if current_user else 'User'
            
            # Update status bar text
            # configure() changes widget properties after creation
            self.status_bar.configure(text=f"Logged in as: {username} | Ready")
        
        # Create content frame (main area that displays forms)
        # This is where EmployeeForm, DepartmentForm, ReportWindow will be displayed
        self.content_frame = ctk.CTkFrame(self.root)
        
        # Pack content frame to fill available space
        # fill="both" fills horizontally and vertically
        # expand=True allows it to grow when window is resized
        # padx=20, pady=20 adds padding around frame
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create welcome label (shown when window first opens)
        # This is the initial content before user selects a menu item
        welcome_label = ctk.CTkLabel(
            self.content_frame,
            text="Smart Records System",
            font=ctk.CTkFont(size=24, weight="bold")  # Large, bold text
        )
        welcome_label.pack(pady=50)  # Add vertical spacing
        
        # Create info label (instructions for user)
        info_label = ctk.CTkLabel(
            self.content_frame,
            text="Use the menu bar to manage employees, departments, and generate reports.",
            font=ctk.CTkFont(size=12)  # Smaller, normal text
        )
        info_label.pack(pady=20)
    
    def clear_content(self):
        """
        Clear the main content area.
        
        This method removes all widgets from content_frame.
        It's called before displaying a new form to ensure old content is removed.
        
        This is important because we reuse the same content_frame for different forms.
        Without clearing, old widgets would remain visible.
        """
        # Loop through all child widgets in content_frame
        # winfo_children() returns a list of all widgets inside content_frame
        for widget in self.content_frame.winfo_children():
            # Destroy each widget (remove from screen and free memory)
            # destroy() removes widget and all its children
            widget.destroy()
    
    def add_employee(self):
        """
        Open the "Add Employee" form.
        
        This method is called when user clicks "Employees → Add Employee" menu.
        It clears the content area and displays EmployeeForm in "add" mode.
        """
        # Clear any existing content
        self.clear_content()
        
        # Create EmployeeForm in "add" mode
        # EmployeeForm is a scrollable form widget
        # mode="add" tells the form to show add employee interface
        form = EmployeeForm(
            self.content_frame,           # Parent widget (where form will be placed)
            self.employee_model,          # For saving employee data
            self.department_model,        # For loading department dropdown
            mode="add"                    # Form mode: add, view, update, delete, search
        )
        
        # Pack form to fill content area
        form.pack(fill="both", expand=True)
        
        # Update status bar to show current action
        self.status_bar.configure(text="Add Employee")
    
    def view_employees(self):
        """
        View all employees in a table.
        
        Called when user clicks "Employees → View All Employees".
        Displays EmployeeForm in "view" mode (shows table of all employees).
        """
        self.clear_content()
        
        # Create form in "view" mode (displays employee list)
        form = EmployeeForm(
            self.content_frame, 
            self.employee_model,
            self.department_model, 
            mode="view"
        )
        form.pack(fill="both", expand=True)
        self.status_bar.configure(text="View All Employees")
    
    def search_employees(self):
        """
        Open employee search interface.
        
        Called when user clicks "Employees → Search Employees".
        Displays EmployeeForm in "search" mode (shows search box and results).
        """
        self.clear_content()
        form = EmployeeForm(
            self.content_frame, 
            self.employee_model,
            self.department_model, 
            mode="search"
        )
        form.pack(fill="both", expand=True)
        self.status_bar.configure(text="Search Employees")
    
    def update_employee(self):
        """
        Open employee update form.
        
        Called when user clicks "Employees → Update Employee".
        Displays EmployeeForm in "update" mode (shows dropdown to select employee, then edit form).
        """
        self.clear_content()
        form = EmployeeForm(
            self.content_frame, 
            self.employee_model,
            self.department_model, 
            mode="update"
        )
        form.pack(fill="both", expand=True)
        self.status_bar.configure(text="Update Employee")
    
    def delete_employee(self):
        """
        Open employee deletion interface.
        
        Called when user clicks "Employees → Delete Employee".
        Displays EmployeeForm in "delete" mode (shows dropdown to select employee, then delete button).
        """
        self.clear_content()
        form = EmployeeForm(
            self.content_frame, 
            self.employee_model,
            self.department_model, 
            mode="delete"
        )
        form.pack(fill="both", expand=True)
        self.status_bar.configure(text="Delete Employee")
    
    def add_department(self):
        """
        Open the "Add Department" form.
        
        Called when user clicks "Departments → Add Department".
        Displays DepartmentForm in "add" mode.
        """
        self.clear_content()
        form = DepartmentForm(
            self.content_frame, 
            self.department_model, 
            mode="add"
        )
        form.pack(fill="both", expand=True)
        self.status_bar.configure(text="Add Department")
    
    def view_departments(self):
        """
        View all departments in a table.
        
        Called when user clicks "Departments → View All Departments".
        Displays DepartmentForm in "view" mode.
        """
        self.clear_content()
        form = DepartmentForm(
            self.content_frame, 
            self.department_model, 
            mode="view"
        )
        form.pack(fill="both", expand=True)
        self.status_bar.configure(text="View All Departments")
    
    def update_department(self):
        """
        Open department update form.
        
        Called when user clicks "Departments → Update Department".
        Displays DepartmentForm in "update" mode.
        """
        self.clear_content()
        form = DepartmentForm(
            self.content_frame, 
            self.department_model, 
            mode="update"
        )
        form.pack(fill="both", expand=True)
        self.status_bar.configure(text="Update Department")
    
    def delete_department(self):
        """
        Open department deletion interface.
        
        Called when user clicks "Departments → Delete Department".
        Displays DepartmentForm in "delete" mode.
        """
        self.clear_content()
        form = DepartmentForm(
            self.content_frame, 
            self.department_model, 
            mode="delete"
        )
        form.pack(fill="both", expand=True)
        self.status_bar.configure(text="Delete Department")
    
    def show_reports(self):
        """
        Show reports window with statistics and listings.
        
        Called when user clicks "Reports → Generate Reports".
        Displays ReportWindow which shows comprehensive report.
        """
        self.clear_content()
        
        # Create ReportWindow
        # ReportWindow displays formatted report with statistics
        report_window = ReportWindow(
            self.content_frame, 
            self.employee_model,
            self.department_model, 
            self.db_manager
        )
        report_window.pack(fill="both", expand=True)
        self.status_bar.configure(text="Generate Reports")
    
    def export_pdf(self):
        """
        Export report to PDF file.
        
        Called when user clicks "Reports → Export to PDF".
        Creates a PDF file in reports_output/ folder.
        
        This method:
        1. Creates ReportGenerator
        2. Calls export_to_pdf() to generate PDF
        3. Shows success/error message
        4. Updates status bar
        """
        # Import ReportGenerator (imported here to avoid circular imports)
        from reports.report_generator import ReportGenerator
        
        # Create report generator
        generator = ReportGenerator(self.employee_model, self.department_model)
        
        # Try to export PDF
        try:
            # Generate PDF file
            # export_to_pdf() returns the file path
            filename = generator.export_to_pdf()
            
            # Show success message with file path
            messagebox.showinfo("Success", f"Report exported to {filename}")
            
            # Update status bar
            self.status_bar.configure(text=f"Report exported to {filename}")
        except Exception as e:
            # If export fails, show error message
            # Common reasons: reportlab not installed, disk full, permission error
            messagebox.showerror("Error", f"Failed to export PDF: {str(e)}")
    
    def export_txt(self):
        """
        Export report to text file.
        
        Called when user clicks "Reports → Export to TXT".
        Creates a TXT file in reports_output/ folder.
        
        Similar to export_pdf() but creates text file instead.
        """
        from reports.report_generator import ReportGenerator
        generator = ReportGenerator(self.employee_model, self.department_model)
        
        try:
            # Generate TXT file
            filename = generator.export_to_txt()
            messagebox.showinfo("Success", f"Report exported to {filename}")
            self.status_bar.configure(text=f"Report exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export TXT: {str(e)}")
    
    def show_about(self):
        """
        Show "About" dialog with application information.
        
        Called when user clicks "Help → About".
        Displays a popup with app version and features.
        """
        # Show information dialog
        messagebox.showinfo(
            "About Smart Records System",  # Dialog title
            "Smart Records System v1.0\n\n"  # Dialog content
            "A GUI-based database application for managing\n"
            "employee and department records.\n\n"
            "Features:\n"
            "- User authentication\n"
            "- CRUD operations\n"
            "- Report generation\n"
            "- PDF and TXT export"
        )
    
    def logout(self):
        """
        Handle logout action.
        
        Called when user clicks "Logout" in menu bar.
        This method:
        1. Confirms logout with user
        2. Calls AuthManager.logout() to clear session
        3. Closes the application (quits main loop)
        
        After logout, user must login again to access the system.
        """
        # Ask user to confirm logout
        # askyesno() shows Yes/No dialog, returns True if Yes clicked
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            # User confirmed - logout
            # Clear current user session
            self.auth_manager.logout()
            
            # Quit the application
            # quit() stops the main event loop and closes all windows
            self.root.quit()
