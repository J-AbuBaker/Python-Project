"""Department management forms."""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from utils.validators import validate_required


class DepartmentForm(ctk.CTkScrollableFrame):
    """Department CRUD form."""
    
    def __init__(self, parent, department_model, mode="view"):
        """
        Initialize department form.
        
        Args:
            parent: Parent widget
            department_model: DepartmentModel instance
            mode: Form mode ('add', 'view', 'update', 'delete')
        """
        super().__init__(parent)
        self.department_model = department_model
        self.mode = mode
        
        self.create_widgets()
        
        if mode == "view":
            self.load_departments()
    
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
    
    def create_add_form(self):
        """Create add department form."""
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(form_frame, text="Add New Department", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        ctk.CTkLabel(form_frame, text="Department Name *:").grid(row=1, column=0, sticky="w", pady=5, padx=10)
        self.name_entry = ctk.CTkEntry(form_frame, width=300)
        self.name_entry.grid(row=1, column=1, pady=5, padx=10)
        self.name_entry.focus()
        
        ctk.CTkLabel(form_frame, text="Description:").grid(row=2, column=0, sticky="w", pady=5, padx=10)
        self.description_text = ctk.CTkTextbox(form_frame, width=300, height=100)
        self.description_text.grid(row=2, column=1, pady=5, padx=10)
        
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ctk.CTkButton(button_frame, text="Add Department", command=self.save_department, width=120).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Clear", command=self.clear_form, width=120).pack(side="left", padx=5)
    
    def create_update_form(self):
        """Create update department form."""
        select_frame = ctk.CTkFrame(self)
        select_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(select_frame, text="Select Department to Update", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
        
        selection_input_frame = ctk.CTkFrame(select_frame, fg_color="transparent")
        selection_input_frame.pack(pady=5)
        
        ctk.CTkLabel(selection_input_frame, text="Department:").pack(side="left", padx=5)
        self.dept_select_var = tk.StringVar()
        self.dept_select_combo = ctk.CTkComboBox(selection_input_frame, variable=self.dept_select_var, 
                                                 width=300, state="readonly", command=self.on_department_selected)
        self.dept_select_combo.pack(side="left", padx=5)
        
        self.load_departments_for_selection()
        
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.selected_dept_id = None
    
    def create_delete_form(self):
        """Create delete department form."""
        delete_frame = ctk.CTkFrame(self)
        delete_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(delete_frame, text="Delete Department", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        ctk.CTkLabel(delete_frame, text="Select Department:").grid(row=1, column=0, sticky="w", pady=5, padx=10)
        self.delete_dept_var = tk.StringVar()
        self.delete_dept_combo = ctk.CTkComboBox(delete_frame, variable=self.delete_dept_var, 
                                                 width=350, state="readonly", command=self.on_delete_department_selected)
        self.delete_dept_combo.grid(row=1, column=1, pady=5, padx=10, sticky="ew")
        delete_frame.grid_columnconfigure(1, weight=1)
        
        self.load_departments_for_delete_selection()
        
        self.delete_info_label = ctk.CTkLabel(delete_frame, text="", font=ctk.CTkFont(size=12))
        self.delete_info_label.grid(row=2, column=0, columnspan=2, pady=20)
        
        self.delete_button = ctk.CTkButton(delete_frame, text="Delete Department", 
                                        command=self.delete_department, state="disabled", width=200)
        self.delete_button.grid(row=3, column=0, columnspan=2, pady=10)
        self.delete_dept_id = None
    
    def create_view_list(self):
        """Create department list view."""
        list_frame = ctk.CTkFrame(self)
        list_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(list_frame, text="All Departments", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        tree_container = ctk.CTkFrame(list_frame)
        tree_container.pack(fill="both", expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_container)
        scrollbar.pack(side="right", fill="y")
        
        self.tree = ttk.Treeview(tree_container, columns=("ID", "Name", "Description", "Created"),
                                show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Created", text="Created At")
        
        self.tree.column("ID", width=80)
        self.tree.column("Name", width=200)
        self.tree.column("Description", width=300)
        self.tree.column("Created", width=150)
        
        self.tree.pack(fill="both", expand=True)
    
    def validate_form(self):
        """Validate form inputs."""
        valid, msg = validate_required(self.name_entry.get(), "Department name")
        if not valid:
            return False, msg
        return True, ""
    
    def save_department(self):
        """Save new department."""
        valid, error_msg = self.validate_form()
        if not valid:
            messagebox.showerror("Validation Error", error_msg)
            return
        
        try:
            description = self.description_text.get("1.0", "end-1c").strip()
            self.department_model.create(
                name=self.name_entry.get().strip(),
                description=description
            )
            messagebox.showinfo("Success", "Department added successfully!")
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add department: {str(e)}")
    
    def clear_form(self):
        """Clear form fields."""
        self.name_entry.delete(0, "end")
        self.description_text.delete("1.0", "end")
    
    def load_departments_for_selection(self):
        """Load departments into selection dropdown."""
        try:
            departments = self.department_model.get_all()
            dept_list = ["-- Select a Department --"] + [
                f"{dept.get('id', '')}: {dept.get('name', '')}"
                for dept in departments
            ]
            if hasattr(self, 'dept_select_combo'):
                self.dept_select_combo.configure(values=dept_list)
                if dept_list:
                    self.dept_select_combo.set(dept_list[0])
        except Exception:
            pass
    
    def on_department_selected(self, choice=None):
        """Handle department selection from dropdown."""
        if not hasattr(self, 'dept_select_var'):
            return
        
        selection = self.dept_select_var.get()
        if not selection or selection == "-- Select a Department --":
            for widget in self.form_frame.winfo_children():
                widget.destroy()
            self.selected_dept_id = None
            return
        
        try:
            dept_id = int(selection.split(":")[0])
            self.load_department_for_update(dept_id)
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Invalid selection")
    
    def load_department_for_update(self, dept_id=None):
        """Load department data for updating."""
        try:
            if dept_id is None:
                if not hasattr(self, 'selected_dept_id') or self.selected_dept_id is None:
                    return
                dept_id = self.selected_dept_id
            else:
                self.selected_dept_id = dept_id
            
            department = self.department_model.get_by_id(dept_id)
            
            if not department:
                messagebox.showerror("Error", "Department not found")
                return
            
            for widget in self.form_frame.winfo_children():
                widget.destroy()
            
            ctk.CTkLabel(self.form_frame, text="Update Department", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=2, pady=10)
            
            ctk.CTkLabel(self.form_frame, text="Department Name *:").grid(row=1, column=0, sticky="w", pady=5, padx=10)
            name_entry = ctk.CTkEntry(self.form_frame, width=300)
            name_entry.insert(0, department.get('name', ''))
            name_entry.grid(row=1, column=1, pady=5, padx=10)
            
            ctk.CTkLabel(self.form_frame, text="Description:").grid(row=2, column=0, sticky="w", pady=5, padx=10)
            description_text = ctk.CTkTextbox(self.form_frame, width=300, height=100)
            description_text.insert("1.0", department.get('description') or "")
            description_text.grid(row=2, column=1, pady=5, padx=10)
            
            def update_department():
                try:
                    if not name_entry.get().strip():
                        messagebox.showerror("Error", "Department name is required")
                        return
                    
                    description = description_text.get("1.0", "end-1c").strip()
                    self.department_model.update(
                        dept_id=self.selected_dept_id,
                        name=name_entry.get().strip(),
                        description=description
                    )
                    messagebox.showinfo("Success", "Department updated successfully!")
                    self.load_departments_for_selection()
                    self.load_department_for_update(self.selected_dept_id)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update department: {str(e)}")
            
            button_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
            button_frame.grid(row=3, column=0, columnspan=2, pady=20)
            ctk.CTkButton(button_frame, text="Update Department", command=update_department, width=120).pack(side="left", padx=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load department: {str(e)}")
    
    def load_departments_for_delete_selection(self):
        """Load departments into delete selection dropdown."""
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
        """Handle department selection for deletion."""
        if not hasattr(self, 'delete_dept_var'):
            return
        
        selection = self.delete_dept_var.get()
        if not selection or selection == "-- Select a Department --":
            self.delete_info_label.configure(text="")
            self.delete_button.configure(state="disabled")
            self.delete_dept_id = None
            return
        
        try:
            dept_id = int(selection.split(":")[0])
            self.load_department_for_delete(dept_id)
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Invalid selection")
    
    def load_department_for_delete(self, dept_id):
        """Load department for deletion."""
        try:
            department = self.department_model.get_by_id(dept_id)
            
            if not department:
                messagebox.showerror("Error", "Department not found")
                self.delete_info_label.configure(text="")
                self.delete_button.configure(state="disabled")
                return
            
            has_employees = self.department_model.has_employees(dept_id)
            warning_text = "\n⚠ Warning: This department has employees assigned to it!" if has_employees else ""
            
            info_text = (f"ID: {department.get('id', 'N/A')}\n"
                        f"Name: {department.get('name', 'N/A')}\n"
                        f"Description: {department.get('description') or 'N/A'}{warning_text}")
            
            self.delete_info_label.configure(text=info_text)
            self.delete_button.configure(state="normal")
            self.delete_dept_id = dept_id
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load department: {str(e)}")
    
    def delete_department(self):
        """Delete department."""
        if not hasattr(self, 'delete_dept_id') or self.delete_dept_id is None:
            return
        
        has_employees = self.department_model.has_employees(self.delete_dept_id)
        warning = ""
        if has_employees:
            warning = "\n\nThis department has employees. Their department will be set to NULL."
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete this department?{warning}"):
            try:
                self.department_model.delete(self.delete_dept_id)
                messagebox.showinfo("Success", "Department deleted successfully!")
                self.delete_info_label.configure(text="")
                self.delete_button.configure(state="disabled")
                self.delete_dept_id = None
                self.load_departments_for_delete_selection()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete department: {str(e)}")
    
    def load_departments(self):
        """Load all departments into treeview."""
        try:
            if hasattr(self, 'tree'):
                for item in self.tree.get_children():
                    self.tree.delete(item)
                
                departments = self.department_model.get_all()
                for dept in departments:
                    try:
                        dept_id = dept.get('id', 'N/A')
                        name = dept.get('name', 'N/A')
                        desc = dept.get('description') or "N/A"
                        created = dept.get('created_at') or "N/A"
                        
                        self.tree.insert("", "end", values=(dept_id, name, desc, created))
                    except Exception:
                        continue
        except Exception:
            pass

