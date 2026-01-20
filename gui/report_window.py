"""
Report Viewing Window - Smart Records System

This module creates a window for viewing and exporting reports. It displays:
- Summary statistics (total employees, average salary, etc.)
- Department-wise employee count
- Complete employee listing
- Complete department listing

The window includes buttons to:
- Refresh the report (reload data)
- Export to PDF
- Export to TXT

GUI CONCEPTS EXPLAINED:
- CTkScrollableFrame: Frame that can scroll if content is too large
- CTkTextbox: Multi-line text display widget (read-only for reports)
- CTkButton: Clickable button that triggers actions
- Report formatting: Uses string formatting to create formatted text reports
"""

# Import CustomTkinter for modern GUI widgets
import customtkinter as ctk

# Import messagebox for popup dialogs
from tkinter import messagebox

# Import ReportGenerator for generating and exporting reports
from reports.report_generator import ReportGenerator


class ReportWindow(ctk.CTkScrollableFrame):
    """
    Report Viewing Window Class
    
    This class creates a window that displays comprehensive reports about
    employees and departments. It shows statistics, listings, and allows
    exporting reports to PDF or TXT files.
    
    The window inherits from CTkScrollableFrame, which provides scrolling
    capability if the report is longer than the visible area.
    """
    
    def __init__(self, parent, employee_model, department_model, db_manager):
        """
        Initialize report window.
        
        Args:
            parent: Parent widget (usually content_frame from MainWindow)
            employee_model: EmployeeModel instance - for getting employee data
            department_model: DepartmentModel instance - for getting department data
            db_manager: DatabaseManager instance - for database operations (not used directly here)
        """
        # Call parent class constructor
        # super() refers to CTkScrollableFrame parent class
        super().__init__(parent)
        
        # Store references to models
        # These are used to query data for the report
        self.employee_model = employee_model
        self.department_model = department_model
        self.db_manager = db_manager
        
        # Create ReportGenerator instance
        # This handles report generation and export functionality
        self.report_generator = ReportGenerator(employee_model, department_model)
        
        # Create widgets (buttons, text area, etc.)
        self.create_widgets()
        
        # Generate and display initial report
        # This shows the report immediately when window opens
        self.generate_summary()
    
    def create_widgets(self):
        """
        Create report window widgets.
        
        This method creates:
        - Control buttons (Refresh, Export PDF, Export TXT)
        - Report text area (displays formatted report)
        """
        # Create frame for control buttons
        # fg_color="transparent" makes frame invisible (no background)
        control_frame = ctk.CTkFrame(self, fg_color="transparent")
        # fill="x" makes it fill horizontally (full width)
        control_frame.pack(fill="x", padx=10, pady=10)
        
        # Create Refresh button
        # command=self.generate_summary reloads the report with latest data
        refresh_button = ctk.CTkButton(
            control_frame, 
            text="Refresh", 
            command=self.generate_summary, 
            width=120
        )
        refresh_button.pack(side="left", padx=5)
        
        # Create Export to PDF button
        # command=self.export_pdf exports report as PDF file
        pdf_button = ctk.CTkButton(
            control_frame, 
            text="Export to PDF", 
            command=self.export_pdf, 
            width=120
        )
        pdf_button.pack(side="left", padx=5)
        
        # Create Export to TXT button
        # command=self.export_txt exports report as text file
        txt_button = ctk.CTkButton(
            control_frame, 
            text="Export to TXT", 
            command=self.export_txt, 
            width=120
        )
        txt_button.pack(side="left", padx=5)
        
        # Create frame for report display
        report_frame = ctk.CTkFrame(self)
        report_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create label for report section
        ctk.CTkLabel(
            report_frame, 
            text="Report Summary", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        # Create text area for displaying report
        # CTkTextbox creates a multi-line text display widget
        # wrap="word" wraps text at word boundaries (not mid-word)
        # font sets font family and size (Courier is monospace, good for reports)
        # width and height set initial dimensions
        self.report_text = ctk.CTkTextbox(
            report_frame,
            wrap="word",  # Wrap text at word boundaries
            font=ctk.CTkFont(family="Courier", size=10),  # Monospace font for alignment
            width=800,    # Initial width in pixels
            height=500    # Initial height in pixels
        )
        # Pack text area to fill available space
        self.report_text.pack(fill="both", expand=True, padx=10, pady=10)
    
    def generate_summary(self):
        """
        Generate and display summary report.
        
        This method:
        1. Queries database for statistics and data
        2. Formats data into a readable report
        3. Displays report in the text area
        
        The report includes:
        - Summary statistics (total employees, average salary, etc.)
        - Department-wise employee count
        - Complete employee listing
        - Complete department listing
        """
        try:
            # Get employee statistics from database
            # get_statistics() returns dict with: total_employees, avg_salary, min_salary, max_salary, total_salary
            stats = self.employee_model.get_statistics()
            
            # Get all employees from database
            # get_all() returns list of employee dictionaries
            employees = self.employee_model.get_all()
            
            # Get all departments from database
            # get_all() returns list of department dictionaries
            departments = self.department_model.get_all()
            
            # ========== BUILD REPORT TEXT ==========
            # Start building report string
            # "=" * 80 creates a line of 80 equal signs (decorative separator)
            report = "=" * 80 + "\n"
            
            # Add report title (centered)
            # " " * 25 adds 25 spaces before title (centers it)
            report += " " * 25 + "SMART RECORDS SYSTEM REPORT\n"
            report += "=" * 80 + "\n\n"
            
            # ========== SUMMARY STATISTICS SECTION ==========
            report += "SUMMARY STATISTICS\n"
            report += "-" * 80 + "\n"  # Separator line
            
            # Add total employees count
            # .get() safely gets value, uses 0 as default if not found
            report += f"Total Employees: {stats.get('total_employees', 0)}\n"
            
            # Add total departments count
            # len() gets number of items in list
            report += f"Total Departments: {len(departments)}\n"
            
            # Add salary statistics (only if there are employees)
            if stats.get('total_employees', 0) > 0:
                # Get salary values (use 0 as default if None)
                avg_salary = stats.get('avg_salary', 0) or 0
                min_salary = stats.get('min_salary', 0) or 0
                max_salary = stats.get('max_salary', 0) or 0
                total_salary = stats.get('total_salary', 0) or 0
                
                # Format salary with currency symbol and commas
                # :,.2f formats number with commas and 2 decimal places
                # Example: 50000 becomes "50,000.00"
                report += f"Average Salary: ${avg_salary:,.2f}\n"
                report += f"Minimum Salary: ${min_salary:,.2f}\n"
                report += f"Maximum Salary: ${max_salary:,.2f}\n"
                report += f"Total Salary Budget: ${total_salary:,.2f}\n"
            
            # Add separator
            report += "\n" + "=" * 80 + "\n\n"
            
            # ========== DEPARTMENT-WISE EMPLOYEE COUNT SECTION ==========
            report += "DEPARTMENT-WISE EMPLOYEE COUNT\n"
            report += "-" * 80 + "\n"
            
            # Count employees per department
            # Create dictionary to store counts
            dept_employee_count = {}
            
            # Loop through all employees
            for emp in employees:
                # Get department name (or "No Department" if None)
                dept_name = emp.get('department_name', 'No Department')
                
                # Increment count for this department
                # .get() gets current count (0 if department not in dict yet)
                # Then add 1
                dept_employee_count[dept_name] = dept_employee_count.get(dept_name, 0) + 1
            
            # Add department counts to report (sorted alphabetically)
            # sorted() sorts dictionary items by key (department name)
            for dept_name, count in sorted(dept_employee_count.items()):
                report += f"{dept_name}: {count} employee(s)\n"
            
            # Add separator
            report += "\n" + "=" * 80 + "\n\n"
            
            # ========== EMPLOYEE LISTING SECTION ==========
            report += "EMPLOYEE LISTING\n"
            report += "-" * 80 + "\n"
            
            # Check if there are employees
            if employees:
                # Create table header
                # Format: column names with spacing
                # <5 means left-align, width 5 characters
                # <25 means left-align, width 25 characters
                report += f"{'ID':<5} {'Name':<25} {'Email':<25} {'Position':<15} {'Salary':<12} {'Department':<15}\n"
                report += "-" * 80 + "\n"  # Separator line
                
                # Add each employee as a row
                for emp in employees:
                    try:
                        # Extract and format employee data
                        # Combine first and last name
                        name = f"{emp.get('first_name', '')} {emp.get('last_name', '')}".strip()
                        
                        email = emp.get('email', 'N/A')
                        
                        # Use "N/A" if position is None or empty
                        position = emp.get('position') or "N/A"
                        
                        # Format salary with currency symbol
                        salary_val = emp.get('salary')
                        # If salary exists and is not 0, format it; otherwise show "N/A"
                        salary = f"${salary_val:.2f}" if salary_val is not None and salary_val != 0 else "N/A"
                        
                        dept = emp.get('department_name', 'N/A')
                        emp_id = emp.get('id', 'N/A')
                        
                        # Add employee row to report
                        # Format aligns columns using spacing
                        report += f"{emp_id:<5} {name:<25} {email:<25} {position:<15} {salary:<12} {dept:<15}\n"
                    except Exception:
                        # Skip this employee if error occurs (prevents crash)
                        continue
            else:
                # No employees found
                report += "No employees found.\n"
            
            # Add separator
            report += "\n" + "=" * 80 + "\n\n"
            
            # ========== DEPARTMENT LISTING SECTION ==========
            report += "DEPARTMENT LISTING\n"
            report += "-" * 80 + "\n"
            
            # Check if there are departments
            if departments:
                # Create table header
                report += f"{'ID':<5} {'Name':<30} {'Description':<40}\n"
                report += "-" * 80 + "\n"
                
                # Add each department as a row
                for dept in departments:
                    try:
                        # Extract department data
                        name = dept.get('name', 'N/A')
                        
                        # Get description (limit to 40 characters)
                        # [:40] slices string to first 40 characters
                        desc = (dept.get('description') or "N/A")[:40]
                        
                        dept_id = dept.get('id', 'N/A')
                        
                        # Add department row to report
                        report += f"{dept_id:<5} {name:<30} {desc:<40}\n"
                    except Exception:
                        # Skip this department if error occurs
                        continue
            else:
                # No departments found
                report += "No departments found.\n"
            
            # ========== REPORT FOOTER ==========
            report += "\n" + "=" * 80 + "\n"
            
            # Add generation timestamp
            # get_current_date() returns formatted date/time string
            report += f"Report generated on: {self.report_generator.get_current_date()}\n"
            report += "=" * 80 + "\n"
            
            # Display report in text area
            # delete("1.0", "end") clears existing text
            # "1.0" means line 1, character 0 (start)
            # "end" means end of text
            self.report_text.delete("1.0", "end")
            
            # insert("1.0", report) adds report text at beginning
            self.report_text.insert("1.0", report)
            
        except Exception as e:
            # If error occurs, display error message
            self.report_text.delete("1.0", "end")
            self.report_text.insert("1.0", f"Error generating report: {str(e)}")
    
    def export_pdf(self):
        """
        Export report to PDF file.
        
        This method:
        1. Calls ReportGenerator.export_to_pdf() to create PDF
        2. Shows success message with file path
        3. Shows error message if export fails
        
        The PDF file is saved in reports_output/ folder with timestamp.
        """
        try:
            # Generate PDF file
            # export_to_pdf() creates PDF and returns file path
            filename = self.report_generator.export_to_pdf()
            
            # Show success message
            messagebox.showinfo("Success", f"Report exported to {filename}")
        except Exception as e:
            # Show error message if export fails
            # Common reasons: reportlab not installed, disk full, permission error
            messagebox.showerror("Error", f"Failed to export PDF: {str(e)}")
    
    def export_txt(self):
        """
        Export report to text file.
        
        This method:
        1. Calls ReportGenerator.export_to_txt() to create TXT file
        2. Shows success message with file path
        3. Shows error message if export fails
        
        The TXT file is saved in reports_output/ folder with timestamp.
        """
        try:
            # Generate TXT file
            # export_to_txt() creates text file and returns file path
            filename = self.report_generator.export_to_txt()
            
            # Show success message
            messagebox.showinfo("Success", f"Report exported to {filename}")
        except Exception as e:
            # Show error message if export fails
            messagebox.showerror("Error", f"Failed to export TXT: {str(e)}")
