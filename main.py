"""Main application entry point."""

import customtkinter as ctk
from tkinter import messagebox
import sys
import os

from database.db_manager import DatabaseManager
from database.models import EmployeeModel, DepartmentModel
from auth.auth_manager import AuthManager
from gui.login_window import LoginWindow
from gui.main_window import MainWindow


def load_db_config():
    """Load MySQL database configuration from db_config.py."""
    if os.path.exists('db_config.py'):
        try:
            import db_config  # pyright: ignore[reportMissingImports]
            mysql_config = getattr(db_config, 'MYSQL_CONFIG', {})
            return mysql_config
        except Exception:
            pass
    
    messagebox.showerror(
        "Configuration Error",
        "db_config.py not found or invalid.\n\n"
        "Please create db_config.py with MySQL configuration.\n"
        "See db_config.py.example for reference."
    )
    sys.exit(1)


class SmartRecordsApp:
    """Main application class."""
    
    def __init__(self):
        """Initialize the application."""
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.withdraw()
        
        mysql_config = load_db_config()
        
        try:
            self.db_manager = DatabaseManager(mysql_config=mysql_config)
            self.db_manager.initialize_database()
        except Exception as e:
            messagebox.showerror(
                "Database Error",
                f"Failed to initialize database:\n{str(e)}\n\n"
                "Make sure MySQL is running and check your configuration in db_config.py.\n\n"
                "Application will exit."
            )
            sys.exit(1)
        
        self.employee_model = EmployeeModel(self.db_manager)
        self.department_model = DepartmentModel(self.db_manager)
        self.auth_manager = AuthManager(self.db_manager)
        self.show_login()
    
    def show_login(self):
        """Show login window."""
        LoginWindow(self.root, self.auth_manager, self.on_login_success)
    
    def on_login_success(self):
        """Handle successful login."""
        self.main_window = MainWindow(
            self.root, self.auth_manager, self.employee_model,
            self.department_model, self.db_manager
        )
        self.root.deiconify()
    
    def run(self):
        """Run the application."""
        self.root.mainloop()
        if hasattr(self, 'db_manager'):
            self.db_manager.close()


def main():
    """Application entry point."""
    SmartRecordsApp().run()


if __name__ == "__main__":
    main()

