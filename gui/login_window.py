"""
Login and Registration Window - Smart Records System

This module creates the login window that appears when the application starts.
Users must authenticate before accessing the main application.

The window includes:
- Login form (username and password fields)
- Registration dialog (for creating new user accounts)
- Password masking (passwords are hidden with asterisks)
- Keyboard shortcuts (Enter key to submit)

GUI CONCEPTS EXPLAINED:
- CTkToplevel: Creates a popup window (separate from main window)
- CTkEntry: Text input field where users type
- CTkButton: Clickable button that triggers actions
- CTkLabel: Text display (labels, titles, etc.)
- grid() and pack(): Layout managers that position widgets
- bind(): Connects keyboard events (like Enter key) to functions
"""

# Import CustomTkinter - modern GUI framework with beautiful widgets
import customtkinter as ctk

# Import messagebox from tkinter - shows popup messages (errors, success, etc.)
from tkinter import messagebox

# Import AuthManager - handles authentication logic (login, registration)
from auth.auth_manager import AuthManager


class LoginWindow:
    """
    Login and Registration Window Class
    
    This class creates and manages the login window. It handles:
    - Displaying login form
    - Processing login attempts
    - Showing registration dialog
    - Validating user input
    
    The window is modal (blocks interaction with other windows until closed).
    """
    
    def __init__(self, root, auth_manager, on_login_success):
        """
        Initialize the login window.
        
        This method creates the window, sets its properties, and creates all widgets.
        
        Args:
            root: The main application window (parent window)
            auth_manager: AuthManager instance - handles authentication logic
            on_login_success: Callback function - called when login succeeds
                            This function will show the main application window
        """
        # Store reference to parent window (main application window)
        # We need this to position the login window relative to the main window
        self.root = root
        
        # Store reference to authentication manager
        # This handles checking username/password and creating new users
        self.auth_manager = auth_manager
        
        # Store callback function - called when user successfully logs in
        # This allows the login window to notify the main app that login succeeded
        self.on_login_success = on_login_success
        
        # Create a new top-level window (popup window)
        # CTkToplevel creates a window that appears on top of the parent window
        # This is different from CTk() which creates the main window
        self.window = ctk.CTkToplevel(root)
        
        # Set window title (appears in window title bar)
        self.window.title("Smart Records System - Login")
        
        # Set window size (width x height in pixels)
        # 400 pixels wide, 300 pixels tall
        self.window.geometry("400x300")
        
        # Prevent window resizing
        # resizable(False, False) means user cannot resize the window
        # This keeps the login window at a fixed size
        self.window.resizable(False, False)
        
        # Make window transient (appears on top of parent, closes when parent closes)
        # transient() makes the window "belong" to the parent window
        self.window.transient(root)
        
        # Make window modal (blocks interaction with other windows)
        # grab_set() makes this window capture all mouse/keyboard events
        # User must interact with this window before accessing other windows
        self.window.grab_set()
        
        # Update window to calculate its actual size
        # update_idletasks() forces window to calculate its dimensions
        # This is needed before we can center it on screen
        self.window.update_idletasks()
        
        # Calculate center position on screen
        # winfo_screenwidth() gets screen width in pixels
        # winfo_screenheight() gets screen height in pixels
        # We subtract half the window size to center it
        x = (self.window.winfo_screenwidth() // 2) - (400 // 2)  # Center horizontally
        y = (self.window.winfo_screenheight() // 2) - (300 // 2)  # Center vertically
        
        # Set window position (geometry format: "widthxheight+x+y")
        # The +x+y positions the window at calculated coordinates
        self.window.geometry(f"400x300+{x}+{y}")
        
        # Create all widgets (labels, input fields, buttons)
        # This method builds the visual interface
        self.create_widgets()
    
    def create_widgets(self):
        """
        Create and layout all widgets in the login window.
        
        This method creates:
        - Title label
        - Username input field
        - Password input field
        - Login button
        - Register button
        
        Layout uses grid() manager for organized rows and columns.
        """
        # Create title label - displays "Smart Records System" at top
        # CTkLabel creates a text label widget
        # font parameter sets text size and weight (bold)
        title_label = ctk.CTkLabel(
            self.window, 
            text="Smart Records System", 
            font=ctk.CTkFont(size=18, weight="bold")  # 18pt font, bold weight
        )
        # pack() places widget in window (simpler than grid for single items)
        # pady=20 adds 20 pixels of vertical padding (space above and below)
        title_label.pack(pady=20)
        
        # Create frame to contain login form
        # CTkFrame creates a container/widget group
        # Frames help organize widgets into logical groups
        login_frame = ctk.CTkFrame(self.window)
        
        # Pack frame to fill available space
        # fill="both" means fill horizontally and vertically
        # expand=True allows frame to grow if window is resized
        # padx=20, pady=20 adds 20 pixels padding on all sides
        login_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create username label
        # grid() positions widget in a grid (rows and columns)
        # row=0, column=0 means first row, first column
        # sticky="w" means align text to west (left side)
        # pady=5 adds vertical padding, padx=10 adds horizontal padding
        ctk.CTkLabel(login_frame, text="Username:").grid(
            row=0, column=0, sticky="w", pady=5, padx=10
        )
        
        # Create username input field
        # CTkEntry creates a text input box
        # width=200 sets field width to 200 pixels
        self.username_entry = ctk.CTkEntry(login_frame, width=200)
        
        # Position username field next to label
        # row=0, column=1 means first row, second column (next to label)
        self.username_entry.grid(row=0, column=1, pady=5, padx=10)
        
        # Set focus to username field (cursor appears here automatically)
        # focus() makes this widget receive keyboard input when window opens
        # This improves user experience - user can start typing immediately
        self.username_entry.focus()
        
        # Create password label
        # row=1 means second row (below username)
        ctk.CTkLabel(login_frame, text="Password:").grid(
            row=1, column=0, sticky="w", pady=5, padx=10
        )
        
        # Create password input field
        # show="*" hides password characters (shows asterisks instead)
        # This is a security feature - prevents others from seeing the password
        self.password_entry = ctk.CTkEntry(login_frame, width=200, show="*")
        self.password_entry.grid(row=1, column=1, pady=5, padx=10)
        
        # Bind Enter key to login function
        # bind() connects keyboard events to functions
        # '<Return>' is the Enter key event
        # lambda e: creates an anonymous function (e is the event object)
        # When user presses Enter in password field, it calls handle_login()
        self.password_entry.bind('<Return>', lambda e: self.handle_login())
        
        # Create button frame (container for buttons)
        # fg_color="transparent" makes frame invisible (no background)
        # This is just for organizing buttons, not displaying anything
        button_frame = ctk.CTkFrame(login_frame, fg_color="transparent")
        
        # Position button frame below form fields
        # columnspan=2 means it spans both columns (full width)
        # pady=20 adds vertical spacing
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Create Login button
        # text="Login" sets button label
        # command=self.handle_login sets function to call when clicked
        # width=120 sets button width to 120 pixels
        login_button = ctk.CTkButton(
            button_frame, 
            text="Login", 
            command=self.handle_login, 
            width=120
        )
        # pack() places button in frame
        # side="left" aligns button to left side
        # padx=5 adds horizontal spacing between buttons
        login_button.pack(side="left", padx=5)
        
        # Create Register button
        # command=self.show_register calls registration dialog when clicked
        register_button = ctk.CTkButton(
            button_frame, 
            text="Register", 
            command=self.show_register, 
            width=120
        )
        register_button.pack(side="left", padx=5)
    
    def handle_login(self):
        """
        Handle login button click or Enter key press.
        
        This method:
        1. Gets username and password from input fields
        2. Calls AuthManager to validate credentials
        3. If successful, closes login window and calls on_login_success callback
        4. If failed, shows error message
        
        This is called when:
        - User clicks "Login" button
        - User presses Enter key in password field
        """
        # Get username from input field
        # .get() retrieves text from the entry widget
        # .strip() removes leading/trailing whitespace
        username = self.username_entry.get().strip()
        
        # Get password from input field
        # Note: We don't strip password (spaces might be intentional)
        password = self.password_entry.get()
        
        # Call AuthManager to authenticate user
        # login() returns a tuple: (success: bool, message: str)
        # success is True if login succeeded, False otherwise
        # message contains success/error message
        success, message = self.auth_manager.login(username, password)
        
        # Check if login was successful
        if success:
            # Login successful!
            # Close the login window
            # destroy() removes the window from screen and frees memory
            self.window.destroy()
            
            # Call the callback function to notify main app
            # This will show the main application window
            self.on_login_success()
        else:
            # Login failed - show error message
            # showerror() displays a popup error dialog
            # First parameter is window title, second is error message
            messagebox.showerror("Login Failed", message)
    
    def show_register(self):
        """
        Show registration dialog window.
        
        This method creates a new popup window where users can create new accounts.
        The registration form includes:
        - Username field
        - Password field
        - Confirm password field (to prevent typos)
        - Register and Cancel buttons
        
        The dialog is modal (blocks interaction until closed).
        """
        # Create registration window (popup dialog)
        # CTkToplevel creates a new window on top of login window
        register_window = ctk.CTkToplevel(self.window)
        
        # Set window title
        register_window.title("Register New User")
        
        # Set window size (350 pixels wide, 200 pixels tall)
        register_window.geometry("350x200")
        
        # Prevent resizing
        register_window.resizable(False, False)
        
        # Make window transient to login window
        # This ensures registration window stays on top of login window
        register_window.transient(self.window)
        
        # Make window modal (blocks interaction with other windows)
        register_window.grab_set()
        
        # Calculate center position
        register_window.update_idletasks()
        x = (register_window.winfo_screenwidth() // 2) - (350 // 2)
        y = (register_window.winfo_screenheight() // 2) - (200 // 2)
        register_window.geometry(f"350x200+{x}+{y}")
        
        # Create frame to contain registration form
        frame = ctk.CTkFrame(register_window)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create username label
        ctk.CTkLabel(frame, text="Username:").grid(
            row=0, column=0, sticky="w", pady=5, padx=10
        )
        
        # Create username input field
        # This is a local variable (not self.username_entry)
        # It's only used within this registration dialog
        username_entry = ctk.CTkEntry(frame, width=200)
        username_entry.grid(row=0, column=1, pady=5, padx=10)
        
        # Set focus to username field
        username_entry.focus()
        
        # Create password label
        ctk.CTkLabel(frame, text="Password:").grid(
            row=1, column=0, sticky="w", pady=5, padx=10
        )
        
        # Create password input field (hidden with asterisks)
        password_entry = ctk.CTkEntry(frame, width=200, show="*")
        password_entry.grid(row=1, column=1, pady=5, padx=10)
        
        # Create confirm password label
        ctk.CTkLabel(frame, text="Confirm:").grid(
            row=2, column=0, sticky="w", pady=5, padx=10
        )
        
        # Create confirm password input field
        # User must type password twice to prevent typos
        confirm_entry = ctk.CTkEntry(frame, width=200, show="*")
        confirm_entry.grid(row=2, column=1, pady=5, padx=10)
        
        # Define registration function (nested function)
        # This function is called when user clicks "Register" button
        def register():
            """
            Handle registration button click.
            
            This function:
            1. Validates input (username, password, password match)
            2. Calls AuthManager to create new user
            3. Shows success/error message
            4. Closes registration window if successful
            """
            # Get values from input fields
            username = username_entry.get().strip()
            password = password_entry.get()
            confirm = confirm_entry.get()
            
            # Validate username is not empty
            if not username:
                messagebox.showerror("Error", "Username is required")
                return  # Exit function early if validation fails
            
            # Validate password is not empty
            if not password:
                messagebox.showerror("Error", "Password is required")
                return
            
            # Validate passwords match
            # This prevents typos - if passwords don't match, user made a mistake
            if password != confirm:
                messagebox.showerror("Error", "Passwords do not match")
                return
            
            # Call AuthManager to register new user
            # register_user() validates username availability and password requirements
            # Returns (success: bool, message: str)
            success, message = self.auth_manager.register_user(username, password)
            
            # Check if registration was successful
            if success:
                # Registration successful!
                # Show success message
                messagebox.showinfo("Success", message)
                
                # Close registration window
                # User can now login with new credentials
                register_window.destroy()
            else:
                # Registration failed - show error message
                # Common reasons: username already exists, password too short
                messagebox.showerror("Registration Failed", message)
        
        # Create button frame for Register and Cancel buttons
        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_frame.grid(row=3, column=0, columnspan=2, pady=15)
        
        # Create Register button
        # command=register calls the register() function when clicked
        register_button = ctk.CTkButton(
            button_frame, 
            text="Register", 
            command=register, 
            width=100
        )
        register_button.pack(side="left", padx=5)
        
        # Create Cancel button
        # command=register_window.destroy closes the registration window
        # destroy() removes the window without registering
        cancel_button = ctk.CTkButton(
            button_frame, 
            text="Cancel", 
            command=register_window.destroy, 
            width=100
        )
        cancel_button.pack(side="left", padx=5)
        
        # Bind Enter key in confirm field to registration function
        # When user presses Enter after typing confirm password, it registers
        # This improves user experience - no need to click button
        confirm_entry.bind('<Return>', lambda e: register())
