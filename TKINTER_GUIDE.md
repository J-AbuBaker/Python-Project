# Complete Tkinter & CustomTkinter Guide
## All Concepts Used in Smart Records System Project

This comprehensive guide explains every tkinter and CustomTkinter concept, widget, and pattern used throughout the Smart Records System project. It's designed for beginners to understand GUI programming with Python.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Basic Concepts](#basic-concepts)
3. [Layout Managers](#layout-managers)
4. [Widgets Reference](#widgets-reference)
5. [Event Handling](#event-handling)
6. [Common Patterns](#common-patterns)
7. [Project-Specific Examples](#project-specific-examples)
8. [Best Practices](#best-practices)

---

## Introduction

### What is Tkinter?
- **Tkinter** is Python's built-in GUI (Graphical User Interface) library
- It provides widgets (buttons, labels, text fields, etc.) to create desktop applications
- It's cross-platform (works on Windows, Mac, Linux)

### What is CustomTkinter?
- **CustomTkinter** is a modern, beautiful extension of tkinter
- Provides the same functionality as tkinter but with modern, customizable styling
- Supports dark/light themes automatically
- Better-looking widgets out of the box

### Why Both?
In this project, we use:
- **CustomTkinter** for most widgets (buttons, labels, entries, etc.)
- **Standard tkinter** for features CustomTkinter doesn't have (Menu bars, Treeview tables)

---

## Basic Concepts

### 1. Root Window
The main window of your application. Everything else is placed inside it.

```python
import customtkinter as ctk

# Create root window
root = ctk.CTk()  # CustomTkinter root window
root.title("My Application")
root.geometry("800x600")  # Width x Height

# Start the application
root.mainloop()  # Keeps window open and responsive
```

**In our project:**
- `main.py` creates the root window
- It's hidden initially (`root.withdraw()`)
- Shown after successful login (`root.deiconify()`)

### 2. Widgets
Widgets are the building blocks of GUI applications:
- **Buttons**: Clickable elements
- **Labels**: Text display
- **Entries**: Text input fields
- **Frames**: Containers for organizing widgets
- **Menus**: Menu bars and dropdowns

### 3. Widget Hierarchy
Widgets are organized in a parent-child relationship:
```
Root Window
  └── Frame
      ├── Label
      ├── Entry
      └── Button
```

---

## Layout Managers

Layout managers control **where** widgets appear in the window. There are three main layout managers:

### 1. `.pack()` - Sequential Layout

**Purpose**: Places widgets one after another (sequentially)

**Common Parameters:**
- `side`: Where to place widget (`"left"`, `"right"`, `"top"`, `"bottom"`)
- `padx`: Horizontal padding (left/right spacing)
- `pady`: Vertical padding (top/bottom spacing)
- `fill`: How to fill space (`"x"`, `"y"`, `"both"`)
- `expand`: Allow widget to grow (`True`/`False`)

**Example:**
```python
# Create buttons
button1 = ctk.CTkButton(frame, text="Button 1")
button2 = ctk.CTkButton(frame, text="Button 2")
button3 = ctk.CTkButton(frame, text="Button 3")

# Pack them horizontally (left to right)
button1.pack(side="left", padx=5)
button2.pack(side="left", padx=5)
button3.pack(side="left", padx=5)

# Result: [Button 1] [Button 2] [Button 3]
```

**Used in our project:**
- Button rows in forms (`gui/login_window.py`, `gui/department_form.py`)
- Status bar at bottom (`gui/main_window.py`)
- Welcome labels (`gui/main_window.py`)

### 2. `.grid()` - Grid Layout

**Purpose**: Places widgets in a grid (rows and columns) - like a spreadsheet

**Common Parameters:**
- `row`: Row number (starts at 0)
- `column`: Column number (starts at 0)
- `sticky`: Alignment within cell (`"w"`, `"e"`, `"n"`, `"s"`, or combinations)
- `padx`: Horizontal padding
- `pady`: Vertical padding
- `columnspan`: Number of columns to span
- `rowspan`: Number of rows to span

**Sticky Values Explained:**
- `sticky="w"` → Align to **west** (left)
- `sticky="e"` → Align to **east** (right)
- `sticky="n"` → Align to **north** (top)
- `sticky="s"` → Align to **south** (bottom)
- `sticky="nsew"` → Fill entire cell (all sides)
- `sticky="ew"` → Stretch horizontally (left and right)

**Example:**
```python
# Create form labels and entries
label = ctk.CTkLabel(frame, text="Name:")
entry = ctk.CTkEntry(frame, width=200)

# Place in grid
label.grid(row=0, column=0, sticky="w", padx=10, pady=5)  # Left column, left-aligned
entry.grid(row=0, column=1, padx=10, pady=5)              # Right column

# Result:
# Name:  [___________]
```

**Used extensively in our project:**
- All form layouts (`gui/employee_form.py`, `gui/department_form.py`)
- Login form (`gui/login_window.py`)
- Registration dialog (`gui/login_window.py`)

### 3. `.place()` - Absolute Positioning

**Purpose**: Places widgets at exact pixel coordinates (rarely used)

**Note**: Not used in this project. `.grid()` and `.pack()` are preferred.

---

## Widgets Reference

### CustomTkinter Widgets

#### 1. `CTkLabel` - Text Display

**Purpose**: Display text (labels, titles, instructions)

**Common Parameters:**
- `text`: Text to display
- `font`: Font settings (`ctk.CTkFont(size=16, weight="bold")`)
- `fg_color`: Foreground (text) color
- `bg_color`: Background color
- `anchor`: Text alignment (`"w"`, `"e"`, `"center"`)

**Example:**
```python
# Simple label
title = ctk.CTkLabel(root, text="Smart Records System")
title.pack(pady=20)

# Label with custom font
title = ctk.CTkLabel(
    root, 
    text="Smart Records System",
    font=ctk.CTkFont(size=18, weight="bold")
)
title.pack(pady=20)
```

**Used in our project:**
- Window titles (`gui/login_window.py`, `gui/main_window.py`)
- Form labels (`gui/employee_form.py`, `gui/department_form.py`)
- Status bar (`gui/main_window.py`)

#### 2. `CTkEntry` - Single-Line Text Input

**Purpose**: User types text in a single line (username, email, etc.)

**Common Parameters:**
- `width`: Width in pixels
- `show`: Character to show instead of text (for passwords: `show="*"`)
- `placeholder_text`: Hint text shown when empty
- `state`: `"normal"` (editable) or `"readonly"` (not editable)

**Methods:**
- `.get()`: Get the text entered by user
- `.insert(index, text)`: Insert text at position
- `.delete(start, end)`: Delete text from start to end
- `.focus()`: Set keyboard focus to this widget

**Example:**
```python
# Username entry
username_entry = ctk.CTkEntry(root, width=200)
username_entry.pack(pady=10)
username_entry.focus()  # Focus when window opens

# Password entry (masked)
password_entry = ctk.CTkEntry(root, width=200, show="*")
password_entry.pack(pady=10)

# Get user input
username = username_entry.get()
```

**Used in our project:**
- Login form (`gui/login_window.py`)
- All form inputs (`gui/employee_form.py`, `gui/department_form.py`)

#### 3. `CTkTextbox` - Multi-Line Text Input/Display

**Purpose**: User types multiple lines of text (descriptions, reports)

**Common Parameters:**
- `width`: Width in pixels
- `height`: Height in pixels
- `wrap`: Word wrapping (`"word"` or `"char"`)
- `state`: `"normal"` (editable) or `"disabled"` (read-only)

**Methods:**
- `.get(start, end)`: Get text from start to end
- `.insert(index, text)`: Insert text at position
- `.delete(start, end)`: Delete text
- `.configure(state="disabled")`: Make read-only

**Example:**
```python
# Description textbox
description_box = ctk.CTkTextbox(root, width=300, height=100)
description_box.pack(pady=10)

# Get all text
text = description_box.get("1.0", "end-1c")  # "1.0" = line 1, char 0

# Insert text
description_box.insert("1.0", "Enter description here...")
```

**Used in our project:**
- Department descriptions (`gui/department_form.py`)
- Report display (`gui/report_window.py`)

#### 4. `CTkButton` - Clickable Button

**Purpose**: User clicks to trigger an action

**Common Parameters:**
- `text`: Button label
- `command`: Function to call when clicked
- `width`: Width in pixels
- `height`: Height in pixels
- `fg_color`: Button color
- `hover_color`: Color when mouse hovers

**Example:**
```python
def handle_click():
    print("Button clicked!")

button = ctk.CTkButton(
    root,
    text="Click Me",
    command=handle_click,
    width=120
)
button.pack(pady=10)
```

**Used extensively in our project:**
- Login button (`gui/login_window.py`)
- Form submit buttons (`gui/employee_form.py`, `gui/department_form.py`)
- Export buttons (`gui/report_window.py`)

#### 5. `CTkComboBox` - Dropdown Selection

**Purpose**: User selects one option from a dropdown list

**Common Parameters:**
- `values`: List of options to choose from
- `variable`: `StringVar` to track selected value
- `width`: Width in pixels
- `state`: `"normal"` or `"readonly"` (prevents typing)
- `command`: Function called when selection changes

**Important**: Requires `StringVar` from tkinter

**Example:**
```python
import tkinter as tk

# Create variable to track selection
department_var = tk.StringVar()

# Create combobox
department_combo = ctk.CTkComboBox(
    root,
    variable=department_var,
    values=["HR", "IT", "Sales", "Marketing"],
    width=250,
    state="readonly"  # Can't type, only select
)
department_combo.pack(pady=10)

# Get selected value
selected = department_var.get()
```

**Used in our project:**
- Department selection (`gui/employee_form.py`)
- Employee selection for update/delete (`gui/employee_form.py`, `gui/department_form.py`)

#### 6. `CTkFrame` - Container Widget

**Purpose**: Groups widgets together visually and logically

**Common Parameters:**
- `fg_color`: Frame background color
- `bg_color`: Frame border color
- `corner_radius`: Rounded corners (0-20)

**Example:**
```python
# Create frame to group buttons
button_frame = ctk.CTkFrame(root)
button_frame.pack(pady=20)

# Add buttons to frame
button1 = ctk.CTkButton(button_frame, text="Button 1")
button2 = ctk.CTkButton(button_frame, text="Button 2")
button1.pack(side="left", padx=5)
button2.pack(side="left", padx=5)
```

**Used in our project:**
- Form containers (`gui/employee_form.py`, `gui/department_form.py`)
- Button groups (`gui/login_window.py`)
- Content area (`gui/main_window.py`)

#### 7. `CTkScrollableFrame` - Scrollable Container

**Purpose**: Frame that can scroll if content is larger than visible area

**Inheritance**: Our forms inherit from this class

**Example:**
```python
class MyForm(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(parent)  # Initialize parent class
        # Now this form can scroll!
        self.create_widgets()
```

**Used in our project:**
- `EmployeeForm` (`gui/employee_form.py`)
- `DepartmentForm` (`gui/department_form.py`)
- `ReportWindow` (`gui/report_window.py`)

#### 8. `CTkToplevel` - Popup Window

**Purpose**: Creates a separate window (popup/dialog)

**Common Parameters:**
- `parent`: Parent window
- `title`: Window title
- `geometry`: Window size (`"400x300"`)

**Important Methods:**
- `.grab_set()`: Makes window modal (blocks other windows)
- `.transient(parent)`: Keeps window on top of parent
- `.destroy()`: Close the window

**Example:**
```python
# Create popup window
popup = ctk.CTkToplevel(root)
popup.title("Registration")
popup.geometry("350x200")
popup.transient(root)  # Stay on top
popup.grab_set()       # Modal (blocks other windows)

# Add content
label = ctk.CTkLabel(popup, text="Register New User")
label.pack(pady=20)
```

**Used in our project:**
- Login window (`gui/login_window.py`)
- Registration dialog (`gui/login_window.py`)

### Standard Tkinter Widgets

#### 9. `tk.Menu` - Menu Bar

**Purpose**: Creates menu bars (File, Edit, etc.) at top of window

**Important Parameters:**
- `tearoff`: `0` = can't detach menu, `1` = can detach (we use `0`)

**Methods:**
- `.add_cascade()`: Add dropdown menu
- `.add_command()`: Add menu item
- `.add_separator()`: Add separator line

**Example:**
```python
import tkinter as tk

# Create menu bar
menubar = tk.Menu(root, tearoff=0)
root.config(menu=menubar)

# Create submenu
file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu)

# Add menu items
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_separator()  # Separator line
file_menu.add_command(label="Exit", command=exit_app)
```

**Used in our project:**
- Main menu bar (`gui/main_window.py`)
- Employees, Departments, Reports, Help menus

#### 10. `ttk.Treeview` - Data Table

**Purpose**: Display data in rows and columns (like a spreadsheet)

**Common Parameters:**
- `columns`: Column names (tuple)
- `show`: What to show (`"headings"` = column headers only, `"tree"` = tree view)
- `height`: Number of visible rows

**Methods:**
- `.insert(parent, index, values, text)`: Add row
- `.delete(item)`: Remove row
- `.get_children()`: Get all row IDs
- `.selection()`: Get selected row ID

**Example:**
```python
from tkinter import ttk

# Create table
tree = ttk.Treeview(
    root,
    columns=("Name", "Email", "Department"),
    show="headings",
    height=10
)

# Define column headers
tree.heading("Name", text="Name")
tree.heading("Email", text="Email")
tree.heading("Department", text="Department")

# Add rows
tree.insert("", "end", values=("John Doe", "john@email.com", "IT"))
tree.insert("", "end", values=("Jane Smith", "jane@email.com", "HR"))

tree.pack(pady=10)
```

**Used in our project:**
- Employee list (`gui/employee_form.py`)
- Department list (`gui/department_form.py`)
- Search results (`gui/employee_form.py`)

#### 11. `StringVar` - Text Variable

**Purpose**: Tracks text value and updates widgets automatically when changed

**Used with**: `CTkComboBox`, `CTkEntry` (sometimes)

**Methods:**
- `.get()`: Get current value
- `.set(value)`: Set value (updates widget automatically)

**Example:**
```python
import tkinter as tk

# Create variable
name_var = tk.StringVar()
name_var.set("Default Name")

# Use with widget
entry = ctk.CTkEntry(root, textvariable=name_var)
entry.pack()

# Get value
current_name = name_var.get()

# Set value (updates entry automatically)
name_var.set("New Name")
```

**Used in our project:**
- Department selection (`gui/employee_form.py`)
- Employee selection (`gui/employee_form.py`, `gui/department_form.py`)

---

## Event Handling

### 1. Button Clicks

**Method**: Use `command` parameter

```python
def handle_button_click():
    print("Button was clicked!")

button = ctk.CTkButton(root, text="Click Me", command=handle_button_click)
```

**Used in our project:**
- All buttons (`gui/login_window.py`, `gui/employee_form.py`, etc.)

### 2. Keyboard Events

**Method**: Use `.bind()` method

**Common Events:**
- `'<Return>'`: Enter key pressed
- `'<KeyPress>'`: Any key pressed
- `'<Button-1>'`: Mouse click

**Example:**
```python
# Bind Enter key to function
entry = ctk.CTkEntry(root)
entry.pack()

def on_enter(event):
    print("Enter key pressed!")
    handle_submit()

entry.bind('<Return>', on_enter)  # Call on_enter when Enter pressed
```

**Used in our project:**
- Login form (`gui/login_window.py`): Enter key submits login
- Registration form (`gui/login_window.py`): Enter key submits registration

### 3. Combobox Selection Change

**Method**: Use `command` parameter

```python
def on_selection_changed(choice):
    print(f"Selected: {choice}")

combo = ctk.CTkComboBox(
    root,
    values=["Option 1", "Option 2"],
    command=on_selection_changed
)
```

**Used in our project:**
- Employee selection (`gui/employee_form.py`): Loads employee data when selected
- Department selection (`gui/department_form.py`): Loads department data when selected

---

## Common Patterns

### Pattern 1: Form Layout with Grid

**Structure**: Labels in left column, entries in right column

```python
# Create frame
form_frame = ctk.CTkFrame(root)
form_frame.pack(padx=20, pady=20)

# Row 0: Name
ctk.CTkLabel(form_frame, text="Name:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
name_entry = ctk.CTkEntry(form_frame, width=250)
name_entry.grid(row=0, column=1, padx=10, pady=5)

# Row 1: Email
ctk.CTkLabel(form_frame, text="Email:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
email_entry = ctk.CTkEntry(form_frame, width=250)
email_entry.grid(row=1, column=1, padx=10, pady=5)
```

**Used in our project:**
- All forms (`gui/employee_form.py`, `gui/department_form.py`)

### Pattern 2: Button Row with Pack

**Structure**: Multiple buttons in a horizontal row

```python
# Create transparent frame for buttons
button_frame = ctk.CTkFrame(root, fg_color="transparent")
button_frame.pack(pady=20)

# Add buttons side by side
ctk.CTkButton(button_frame, text="Save", command=save, width=120).pack(side="left", padx=5)
ctk.CTkButton(button_frame, text="Cancel", command=cancel, width=120).pack(side="left", padx=5)
ctk.CTkButton(button_frame, text="Clear", command=clear, width=120).pack(side="left", padx=5)
```

**Used in our project:**
- All forms (`gui/employee_form.py`, `gui/department_form.py`, `gui/login_window.py`)

### Pattern 3: Modal Dialog Window

**Structure**: Popup window that blocks interaction until closed

```python
def show_dialog():
    # Create popup
    dialog = ctk.CTkToplevel(root)
    dialog.title("Dialog Title")
    dialog.geometry("400x300")
    dialog.transient(root)    # Stay on top
    dialog.grab_set()         # Block other windows
    
    # Center window
    dialog.update_idletasks()
    x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
    y = (dialog.winfo_screenheight() // 2) - (300 // 2)
    dialog.geometry(f"400x300+{x}+{y}")
    
    # Add content
    label = ctk.CTkLabel(dialog, text="Dialog Content")
    label.pack(pady=20)
    
    # Close button
    ctk.CTkButton(dialog, text="Close", command=dialog.destroy).pack(pady=10)
```

**Used in our project:**
- Registration dialog (`gui/login_window.py`)

### Pattern 4: Dynamic Content Clearing

**Structure**: Clear old widgets before showing new ones

```python
def clear_content(self):
    """Remove all widgets from content frame"""
    for widget in self.content_frame.winfo_children():
        widget.destroy()

def show_new_form(self):
    self.clear_content()  # Remove old widgets
    # Add new widgets
    new_form = MyForm(self.content_frame)
    new_form.pack(fill="both", expand=True)
```

**Used in our project:**
- Main window (`gui/main_window.py`): Clears content before showing new form

### Pattern 5: Scrollable Form

**Structure**: Form that inherits from `CTkScrollableFrame`

```python
class MyForm(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(parent)  # Initialize scrollable frame
        self.create_widgets()
    
    def create_widgets(self):
        # Add widgets - they'll scroll if too many
        label = ctk.CTkLabel(self, text="Form Title")
        label.pack(pady=10)
        # ... more widgets
```

**Used in our project:**
- `EmployeeForm` (`gui/employee_form.py`)
- `DepartmentForm` (`gui/department_form.py`)
- `ReportWindow` (`gui/report_window.py`)

---

## Project-Specific Examples

### Example 1: Login Window (`gui/login_window.py`)

**Key Concepts:**
- `CTkToplevel`: Separate window
- `CTkEntry`: Username/password input
- `show="*"`: Password masking
- `.bind('<Return>')`: Enter key handling
- `.grab_set()`: Modal window
- `.transient()`: Stay on top

**Code Structure:**
```python
class LoginWindow:
    def __init__(self, root, auth_manager, on_login_success):
        self.window = ctk.CTkToplevel(root)
        self.window.grab_set()  # Modal
        self.create_widgets()
    
    def create_widgets(self):
        # Username entry
        self.username_entry = ctk.CTkEntry(self.window, width=200)
        self.username_entry.pack()
        
        # Password entry (masked)
        self.password_entry = ctk.CTkEntry(self.window, width=200, show="*")
        self.password_entry.pack()
        self.password_entry.bind('<Return>', lambda e: self.handle_login())
        
        # Login button
        ctk.CTkButton(self.window, text="Login", command=self.handle_login).pack()
```

### Example 2: Employee Form (`gui/employee_form.py`)

**Key Concepts:**
- `CTkScrollableFrame`: Scrollable form
- `grid()`: Form layout
- `CTkComboBox`: Department selection
- `ttk.Treeview`: Employee table
- `StringVar`: Track selections

**Code Structure:**
```python
class EmployeeForm(ctk.CTkScrollableFrame):
    def create_add_form(self):
        # Name field
        ctk.CTkLabel(self, text="First Name *:").grid(row=1, column=0, sticky="w")
        self.first_name_entry = ctk.CTkEntry(self, width=250)
        self.first_name_entry.grid(row=1, column=1)
        
        # Department dropdown
        self.department_var = tk.StringVar()
        self.department_combo = ctk.CTkComboBox(
            self,
            variable=self.department_var,
            state="readonly"
        )
        self.department_combo.grid(row=7, column=1)
        self.load_departments()  # Populate dropdown
```

### Example 3: Main Menu (`gui/main_window.py`)

**Key Concepts:**
- `tk.Menu`: Menu bar
- `tearoff=0`: Prevent menu detachment
- `.add_cascade()`: Dropdown menus
- `.add_command()`: Menu items
- `.add_separator()`: Separator lines

**Code Structure:**
```python
def create_menu(self):
    menubar = tk.Menu(self.root, tearoff=0)
    self.root.config(menu=menubar)
    
    # Employees menu
    employees_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Employees", menu=employees_menu)
    employees_menu.add_command(label="Add Employee", command=self.add_employee)
    employees_menu.add_command(label="View All Employees", command=self.view_employees)
    employees_menu.add_separator()
    employees_menu.add_command(label="Delete Employee", command=self.delete_employee)
```

### Example 4: Data Table (`gui/employee_form.py`)

**Key Concepts:**
- `ttk.Treeview`: Table widget
- `.heading()`: Column headers
- `.insert()`: Add rows
- `.get_children()`: Get all rows
- `.delete()`: Remove rows

**Code Structure:**
```python
def create_view_list(self):
    # Create table
    self.tree = ttk.Treeview(
        self,
        columns=("ID", "Name", "Email", "Department", "Position"),
        show="headings",
        height=15
    )
    
    # Define headers
    self.tree.heading("ID", text="ID")
    self.tree.heading("Name", text="Name")
    # ... more headers
    
    # Add rows
    for employee in employees:
        self.tree.insert("", "end", values=(
            employee['id'],
            f"{employee['first_name']} {employee['last_name']}",
            employee['email'],
            # ... more values
        ))
```

---

## Best Practices

### 1. Use Grid for Forms, Pack for Simple Layouts
- **Grid**: Forms with labels and entries (organized rows/columns)
- **Pack**: Simple sequential layouts (buttons in a row, status bar)

### 2. Always Use `sticky="w"` for Labels
- Keeps labels left-aligned for consistent appearance

### 3. Set `tearoff=0` for Menus
- Modern applications don't need detachable menus

### 4. Use `state="readonly"` for ComboBoxes
- Prevents users from typing invalid values

### 5. Clear Content Before Showing New Forms
- Prevents widgets from piling up
- Use `clear_content()` method

### 6. Use `CTkScrollableFrame` for Long Forms
- Automatically handles scrolling
- Better user experience

### 7. Bind Enter Key for Forms
- Improves usability
- Users expect Enter to submit

### 8. Use `StringVar` with ComboBoxes
- Easier to track and update selections

### 9. Center Modal Windows
- Better user experience
- Use `update_idletasks()` before calculating position

### 10. Use `fg_color="transparent"` for Button Frames
- Cleaner appearance
- Buttons appear grouped without visible frame

---

## Quick Reference

### Layout Managers

| Method | Use Case | Example |
|-------|----------|---------|
| `.pack()` | Simple sequential layout | Buttons in a row |
| `.grid()` | Form layouts | Labels and entries |
| `.place()` | Rarely used | Not used in this project |

### Common Widgets

| Widget | Purpose | Key Method |
|--------|---------|------------|
| `CTkLabel` | Display text | `.configure(text="...")` |
| `CTkEntry` | Single-line input | `.get()` |
| `CTkTextbox` | Multi-line input | `.get("1.0", "end")` |
| `CTkButton` | Clickable button | `command=function` |
| `CTkComboBox` | Dropdown selection | `variable=StringVar` |
| `CTkFrame` | Container | Groups widgets |
| `CTkScrollableFrame` | Scrollable container | Inherit from this |
| `CTkToplevel` | Popup window | `.grab_set()` |

### Common Parameters

| Parameter | Values | Purpose |
|-----------|--------|---------|
| `sticky` | `"w"`, `"e"`, `"n"`, `"s"` | Alignment in grid |
| `side` | `"left"`, `"right"`, `"top"`, `"bottom"` | Position in pack |
| `padx` | Number | Horizontal padding |
| `pady` | Number | Vertical padding |
| `state` | `"normal"`, `"readonly"`, `"disabled"` | Widget state |
| `show` | String | Character to show (for passwords: `"*"`) |
| `tearoff` | `0` or `1` | Menu detachment (use `0`) |

---

## Conclusion

This guide covers all tkinter and CustomTkinter concepts used in the Smart Records System project. Each widget, layout manager, and pattern is explained with examples from the actual project code.

**Key Takeaways:**
1. Use CustomTkinter for modern, beautiful widgets
2. Use `grid()` for forms, `pack()` for simple layouts
3. Always clear content before showing new forms
4. Use `CTkScrollableFrame` for long forms
5. Bind Enter key for better UX
6. Use `StringVar` with ComboBoxes

For more details, refer to the actual code files in the `gui/` directory, which contain extensive line-by-line comments explaining every concept.

---

**Happy GUI Programming! 🎨**
