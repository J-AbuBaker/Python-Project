"""
Main Application Entry Point - Smart Records System

This file is the starting point of the entire application. When you run this program,
it initializes all components (database, authentication, GUI) and starts the application.

Think of this file as the "conductor" of an orchestra - it coordinates all the different
parts of the system to work together.
"""

# Import the customtkinter library - this provides modern, beautiful GUI components
# CustomTkinter is built on top of tkinter but with a modern look
import customtkinter as ctk

# Import messagebox from tkinter - this shows popup messages to users
# (like error messages, success messages, etc.)
from tkinter import messagebox

# Import sys - provides system-specific functions (like exiting the program)
import sys

# Import os - provides operating system interface functions (like checking if files exist)
import os

# Import DatabaseManager - this class handles all database connections and operations
# It's like a "translator" between Python and MySQL database
from database.db_manager import DatabaseManager

# Import EmployeeModel and DepartmentModel - these classes handle business logic
# for employees and departments. They use the DatabaseManager to save/load data
from database.models import EmployeeModel, DepartmentModel

# Import AuthManager - handles user authentication (login, registration, password checking)
from auth.auth_manager import AuthManager

# Import LoginWindow - the GUI window that shows the login screen
from gui.login_window import LoginWindow

# Import MainWindow - the main GUI window that appears after successful login
from gui.main_window import MainWindow


def load_db_config():
    """
    Load MySQL database configuration from db_config.py file.
    
    This function reads the database connection settings (host, username, password, etc.)
    from a configuration file. This is safer than hardcoding credentials in the code.
    
    Returns:
        dict: A dictionary containing MySQL connection settings
        Exits the program if configuration file is missing or invalid
    """
    # Check if the db_config.py file exists in the current directory
    # os.path.exists() returns True if file exists, False otherwise
    if os.path.exists('db_config.py'):
        # Try to import and read the configuration
        try:
            # Import the db_config module (this loads db_config.py file)
            # The comment tells the type checker to ignore missing import warnings
            import db_config  # pyright: ignore[reportMissingImports]
            
            # Get the MYSQL_CONFIG dictionary from the db_config module
            # getattr() safely gets an attribute, returns {} if it doesn't exist
            mysql_config = getattr(db_config, 'MYSQL_CONFIG', {})
            
            # Return the configuration dictionary so it can be used to connect to database
            return mysql_config
        except Exception:
            # If anything goes wrong (file corrupted, syntax error, etc.), just pass
            # and show error message below
            pass
    
    # If we get here, the config file doesn't exist or couldn't be loaded
    # Show an error message to the user explaining what's wrong
    messagebox.showerror(
        "Configuration Error",  # Title of the error window
        "db_config.py not found or invalid.\n\n"  # Error message text
        "Please create db_config.py with MySQL configuration.\n"
        "See db_config.py.example for reference."
    )
    # Exit the program with error code 1 (indicates failure)
    sys.exit(1)


class SmartRecordsApp:
    """
    Main Application Class - The Core of the Application
    
    This class represents the entire application. It creates and manages all the
    major components: database connection, authentication system, and GUI windows.
    
    Think of this class as the "brain" of the application - it coordinates everything.
    """
    
    def __init__(self):
        """
        Initialize the application - This is called when the app starts.
        
        This method sets up:
        1. GUI appearance settings
        2. Database connection
        3. Data models (Employee, Department)
        4. Authentication system
        5. Shows the login window
        """
        # Set the appearance mode to "System" - this makes the app match your OS theme
        # (dark mode on Windows 10/11 if you have dark mode enabled)
        ctk.set_appearance_mode("System")
        
        # Set the default color theme to "blue" - this gives buttons and widgets a blue color
        ctk.set_default_color_theme("blue")
        
        # Create the main window (root window) - this is the base window for the app
        # CTk() creates a CustomTkinter window object
        self.root = ctk.CTk()
        
        # Hide the main window initially - we'll show it after login
        # withdraw() hides the window without destroying it
        self.root.withdraw()
        
        # Load database configuration from db_config.py file
        # This gets the connection settings (host, username, password, database name)
        mysql_config = load_db_config()
        
        # Try to connect to the database and initialize it
        try:
            # Create a DatabaseManager object - this handles all database operations
            # We pass the mysql_config dictionary so it knows how to connect
            self.db_manager = DatabaseManager(mysql_config=mysql_config)
            
            # Initialize the database - this creates all necessary tables if they don't exist
            # Also creates default admin user and sample data if database is empty
            self.db_manager.initialize_database()
        except Exception as e:
            # If database connection fails, show an error message
            # str(e) converts the exception to a readable error message
            messagebox.showerror(
                "Database Error",  # Error window title
                f"Failed to initialize database:\n{str(e)}\n\n"  # Error message with details
                "Make sure MySQL is running and check your configuration in db_config.py.\n\n"
                "Application will exit."
            )
            # Exit the program since we can't work without a database
            sys.exit(1)
        
        # Create EmployeeModel - this handles all employee-related operations
        # (adding, updating, deleting, searching employees)
        # We pass db_manager so it can use it to save/load data
        self.employee_model = EmployeeModel(self.db_manager)
        
        # Create DepartmentModel - this handles all department-related operations
        # (adding, updating, deleting departments)
        self.department_model = DepartmentModel(self.db_manager)
        
        # Create AuthManager - this handles user authentication
        # (login, registration, password checking)
        self.auth_manager = AuthManager(self.db_manager)
        
        # Show the login window - user must login before accessing the main app
        self.show_login()
    
    def show_login(self):
        """
        Show the login window to the user.
        
        This creates a login window where users can enter their username and password.
        After successful login, the main window will be shown.
        """
        # Create and show the LoginWindow
        # Parameters:
        #   - self.root: The main window (parent window)
        #   - self.auth_manager: The authentication manager (handles login logic)
        #   - self.on_login_success: Function to call when login succeeds
        LoginWindow(self.root, self.auth_manager, self.on_login_success)
    
    def on_login_success(self):
        """
        Handle successful login - Called after user successfully logs in.
        
        This method creates and shows the main application window with all features:
        employee management, department management, reports, etc.
        """
        # Create the main window with all the application features
        # Parameters:
        #   - self.root: The main window container
        #   - self.auth_manager: For logout functionality
        #   - self.employee_model: For employee operations
        #   - self.department_model: For department operations
        #   - self.db_manager: For database operations
        self.main_window = MainWindow(
            self.root, self.auth_manager, self.employee_model,
            self.department_model, self.db_manager
        )
        
        # Show the main window (it was hidden earlier)
        # deiconify() makes a hidden window visible again
        self.root.deiconify()
    
    def run(self):
        """
        Run the application - Start the main event loop.
        
        This method starts the GUI event loop, which waits for user interactions
        (button clicks, menu selections, etc.) and responds to them.
        
        The loop continues until the user closes the window or logs out.
        """
        # Start the main event loop - this keeps the application running
        # The loop waits for events (button clicks, keyboard input, etc.) and processes them
        # This is a blocking call - the program stays here until the window is closed
        self.root.mainloop()
        
        # After the window is closed, check if we have a database connection
        # hasattr() checks if an object has a specific attribute
        if hasattr(self, 'db_manager'):
            # Close the database connection to free up resources
            # This is good practice - always close database connections when done
            self.db_manager.close()


def main():
    """
    Application Entry Point - This is where the program starts.
    
    When you run this Python file, Python calls this function first.
    This function creates the application and starts it running.
    """
    # Create a SmartRecordsApp object - this initializes everything
    # Then call run() to start the GUI event loop
    SmartRecordsApp().run()


# This special check ensures code only runs when the file is executed directly
# (not when it's imported as a module by another file)
# This is a Python convention - allows the file to be both runnable and importable
if __name__ == "__main__":
    # Call the main function to start the application
    main()
