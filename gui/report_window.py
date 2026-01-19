"""Report viewing window."""

import customtkinter as ctk
from tkinter import messagebox
from reports.report_generator import ReportGenerator


class ReportWindow(ctk.CTkScrollableFrame):
    """Report viewing and display interface."""
    
    def __init__(self, parent, employee_model, department_model, db_manager):
        """Initialize report window."""
        super().__init__(parent)
        self.employee_model = employee_model
        self.department_model = department_model
        self.db_manager = db_manager
        self.report_generator = ReportGenerator(employee_model, department_model)
        
        self.create_widgets()
        self.generate_summary()
    
    def create_widgets(self):
        """Create report window widgets."""
        control_frame = ctk.CTkFrame(self, fg_color="transparent")
        control_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(control_frame, text="Refresh", command=self.generate_summary, width=120).pack(side="left", padx=5)
        ctk.CTkButton(control_frame, text="Export to PDF", command=self.export_pdf, width=120).pack(side="left", padx=5)
        ctk.CTkButton(control_frame, text="Export to TXT", command=self.export_txt, width=120).pack(side="left", padx=5)
        
        report_frame = ctk.CTkFrame(self)
        report_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(report_frame, text="Report Summary", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        self.report_text = ctk.CTkTextbox(
            report_frame,
            wrap="word",
            font=ctk.CTkFont(family="Courier", size=10),
            width=800,
            height=500
        )
        self.report_text.pack(fill="both", expand=True, padx=10, pady=10)
    
    def generate_summary(self):
        """Generate and display summary report."""
        try:
            stats = self.employee_model.get_statistics()
            employees = self.employee_model.get_all()
            departments = self.department_model.get_all()
            
            report = "=" * 80 + "\n"
            report += " " * 25 + "SMART RECORDS SYSTEM REPORT\n"
            report += "=" * 80 + "\n\n"
            
            report += "SUMMARY STATISTICS\n"
            report += "-" * 80 + "\n"
            report += f"Total Employees: {stats.get('total_employees', 0)}\n"
            report += f"Total Departments: {len(departments)}\n"
            
            if stats.get('total_employees', 0) > 0:
                avg_salary = stats.get('avg_salary', 0) or 0
                min_salary = stats.get('min_salary', 0) or 0
                max_salary = stats.get('max_salary', 0) or 0
                total_salary = stats.get('total_salary', 0) or 0
                
                report += f"Average Salary: ${avg_salary:,.2f}\n"
                report += f"Minimum Salary: ${min_salary:,.2f}\n"
                report += f"Maximum Salary: ${max_salary:,.2f}\n"
                report += f"Total Salary Budget: ${total_salary:,.2f}\n"
            
            report += "\n" + "=" * 80 + "\n\n"
            
            report += "DEPARTMENT-WISE EMPLOYEE COUNT\n"
            report += "-" * 80 + "\n"
            
            dept_employee_count = {}
            for emp in employees:
                dept_name = emp.get('department_name', 'No Department')
                dept_employee_count[dept_name] = dept_employee_count.get(dept_name, 0) + 1
            
            for dept_name, count in sorted(dept_employee_count.items()):
                report += f"{dept_name}: {count} employee(s)\n"
            
            report += "\n" + "=" * 80 + "\n\n"
            
            report += "EMPLOYEE LISTING\n"
            report += "-" * 80 + "\n"
            
            if employees:
                report += f"{'ID':<5} {'Name':<25} {'Email':<25} {'Position':<15} {'Salary':<12} {'Department':<15}\n"
                report += "-" * 80 + "\n"
                
                for emp in employees:
                    try:
                        name = f"{emp.get('first_name', '')} {emp.get('last_name', '')}".strip()
                        email = emp.get('email', 'N/A')
                        position = emp.get('position') or "N/A"
                        salary_val = emp.get('salary')
                        salary = f"${salary_val:.2f}" if salary_val is not None and salary_val != 0 else "N/A"
                        dept = emp.get('department_name', 'N/A')
                        emp_id = emp.get('id', 'N/A')
                        
                        report += f"{emp_id:<5} {name:<25} {email:<25} {position:<15} {salary:<12} {dept:<15}\n"
                    except Exception:
                        continue
            else:
                report += "No employees found.\n"
            
            report += "\n" + "=" * 80 + "\n\n"
            
            report += "DEPARTMENT LISTING\n"
            report += "-" * 80 + "\n"
            
            if departments:
                report += f"{'ID':<5} {'Name':<30} {'Description':<40}\n"
                report += "-" * 80 + "\n"
                
                for dept in departments:
                    try:
                        name = dept.get('name', 'N/A')
                        desc = (dept.get('description') or "N/A")[:40]
                        dept_id = dept.get('id', 'N/A')
                        report += f"{dept_id:<5} {name:<30} {desc:<40}\n"
                    except Exception:
                        continue
            else:
                report += "No departments found.\n"
            
            report += "\n" + "=" * 80 + "\n"
            report += f"Report generated on: {self.report_generator.get_current_date()}\n"
            report += "=" * 80 + "\n"
            
            self.report_text.delete("1.0", "end")
            self.report_text.insert("1.0", report)
            
        except Exception as e:
            self.report_text.delete("1.0", "end")
            self.report_text.insert("1.0", f"Error generating report: {str(e)}")
    
    def export_pdf(self):
        """Export report to PDF."""
        try:
            filename = self.report_generator.export_to_pdf()
            messagebox.showinfo("Success", f"Report exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export PDF: {str(e)}")
    
    def export_txt(self):
        """Export report to TXT."""
        try:
            filename = self.report_generator.export_to_txt()
            messagebox.showinfo("Success", f"Report exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export TXT: {str(e)}")

