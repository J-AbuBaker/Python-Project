"""Login and registration window."""

import customtkinter as ctk
from tkinter import messagebox
from auth.auth_manager import AuthManager


class LoginWindow:
    """Login and registration interface."""
    
    def __init__(self, root, auth_manager, on_login_success):
        """Initialize login window."""
        self.root = root
        self.auth_manager = auth_manager
        self.on_login_success = on_login_success
        
        self.window = ctk.CTkToplevel(root)
        self.window.title("Smart Records System - Login")
        self.window.geometry("400x300")
        self.window.resizable(False, False)
        self.window.transient(root)
        self.window.grab_set()
        
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.window.winfo_screenheight() // 2) - (300 // 2)
        self.window.geometry(f"400x300+{x}+{y}")
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create and layout widgets."""
        title_label = ctk.CTkLabel(self.window, text="Smart Records System", font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(pady=20)
        
        login_frame = ctk.CTkFrame(self.window)
        login_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(login_frame, text="Username:").grid(row=0, column=0, sticky="w", pady=5, padx=10)
        self.username_entry = ctk.CTkEntry(login_frame, width=200)
        self.username_entry.grid(row=0, column=1, pady=5, padx=10)
        self.username_entry.focus()
        
        ctk.CTkLabel(login_frame, text="Password:").grid(row=1, column=0, sticky="w", pady=5, padx=10)
        self.password_entry = ctk.CTkEntry(login_frame, width=200, show="*")
        self.password_entry.grid(row=1, column=1, pady=5, padx=10)
        self.password_entry.bind('<Return>', lambda e: self.handle_login())
        
        button_frame = ctk.CTkFrame(login_frame, fg_color="transparent")
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        ctk.CTkButton(button_frame, text="Login", command=self.handle_login, width=120).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Register", command=self.show_register, width=120).pack(side="left", padx=5)
    
    def handle_login(self):
        """Handle login button click."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        success, message = self.auth_manager.login(username, password)
        
        if success:
            self.window.destroy()
            self.on_login_success()
        else:
            messagebox.showerror("Login Failed", message)
    
    def show_register(self):
        """Show registration dialog."""
        register_window = ctk.CTkToplevel(self.window)
        register_window.title("Register New User")
        register_window.geometry("350x200")
        register_window.resizable(False, False)
        register_window.transient(self.window)
        register_window.grab_set()
        
        register_window.update_idletasks()
        x = (register_window.winfo_screenwidth() // 2) - (350 // 2)
        y = (register_window.winfo_screenheight() // 2) - (200 // 2)
        register_window.geometry(f"350x200+{x}+{y}")
        
        frame = ctk.CTkFrame(register_window)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(frame, text="Username:").grid(row=0, column=0, sticky="w", pady=5, padx=10)
        username_entry = ctk.CTkEntry(frame, width=200)
        username_entry.grid(row=0, column=1, pady=5, padx=10)
        username_entry.focus()
        
        ctk.CTkLabel(frame, text="Password:").grid(row=1, column=0, sticky="w", pady=5, padx=10)
        password_entry = ctk.CTkEntry(frame, width=200, show="*")
        password_entry.grid(row=1, column=1, pady=5, padx=10)
        
        ctk.CTkLabel(frame, text="Confirm:").grid(row=2, column=0, sticky="w", pady=5, padx=10)
        confirm_entry = ctk.CTkEntry(frame, width=200, show="*")
        confirm_entry.grid(row=2, column=1, pady=5, padx=10)
        
        def register():
            username = username_entry.get().strip()
            password = password_entry.get()
            confirm = confirm_entry.get()
            
            if not username:
                messagebox.showerror("Error", "Username is required")
                return
            
            if not password:
                messagebox.showerror("Error", "Password is required")
                return
            
            if password != confirm:
                messagebox.showerror("Error", "Passwords do not match")
                return
            
            success, message = self.auth_manager.register_user(username, password)
            
            if success:
                messagebox.showinfo("Success", message)
                register_window.destroy()
            else:
                messagebox.showerror("Registration Failed", message)
        
        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_frame.grid(row=3, column=0, columnspan=2, pady=15)
        
        ctk.CTkButton(button_frame, text="Register", command=register, width=100).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Cancel", command=register_window.destroy, width=100).pack(side="left", padx=5)
        
        confirm_entry.bind('<Return>', lambda e: register())

