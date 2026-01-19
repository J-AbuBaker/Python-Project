"""Report generation and export functionality."""

from datetime import datetime
import os


class ReportGenerator:
    """Generates and exports reports in various formats."""
    
    def __init__(self, employee_model, department_model):
        """Initialize report generator."""
        self.employee_model = employee_model
        self.department_model = department_model
    
    def get_current_date(self):
        """Get current date as formatted string."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def generate_report_text(self):
        """Generate report text content."""
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
        report += f"Report generated on: {self.get_current_date()}\n"
        report += "=" * 80 + "\n"
        
        return report
    
    def export_to_txt(self) -> str:
        """
        Export report to text file.
        
        Returns:
            Path to exported file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{timestamp}.txt"
        
        output_dir = "reports_output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.generate_report_text())
        
        return filepath
    
    def export_to_pdf(self):
        """
        Export report to PDF file.
        
        Returns:
            Path to exported file
        """
        try:
            from reportlab.lib.pagesizes import letter  # type: ignore
            from reportlab.lib import colors  # type: ignore
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle  # type: ignore
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle  # type: ignore
            from reportlab.lib.units import inch  # type: ignore
        except ImportError:
            raise ImportError("reportlab library is required for PDF export. Install it using: pip install reportlab")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{timestamp}.pdf"
        
        output_dir = "reports_output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        filepath = os.path.join(output_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'],
            fontSize=18, textAlignment=1, spaceAfter=30)
        
        heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'],
            fontSize=14, spaceAfter=12)
        
        story.append(Paragraph("Smart Records System Report", title_style))
        story.append(Spacer(1, 0.2 * inch))
        
        stats = self.employee_model.get_statistics()
        employees = self.employee_model.get_all()
        departments = self.department_model.get_all()
        
        story.append(Paragraph("Summary Statistics", heading_style))
        summary_data = [
            ['Metric', 'Value'],
            ['Total Employees', str(stats.get('total_employees', 0))],
            ['Total Departments', str(len(departments))]
        ]
        
        if stats.get('total_employees', 0) > 0:
            avg_salary = stats.get('avg_salary', 0) or 0
            min_salary = stats.get('min_salary', 0) or 0
            max_salary = stats.get('max_salary', 0) or 0
            total_salary = stats.get('total_salary', 0) or 0
            
            summary_data.extend([
                ['Average Salary', f"${avg_salary:,.2f}"],
                ['Minimum Salary', f"${min_salary:,.2f}"],
                ['Maximum Salary', f"${max_salary:,.2f}"],
                ['Total Salary Budget', f"${total_salary:,.2f}"]
            ])
        
        summary_table = Table(summary_data, colWidths=[3 * inch, 3 * inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 0.3 * inch))
        
        story.append(Paragraph("Department-wise Employee Count", heading_style))
        # Aggregate employee count by department for PDF table
        dept_employee_count = {}
        for emp in employees:
            dept_name = emp.get('department_name', 'No Department')
            dept_employee_count[dept_name] = dept_employee_count.get(dept_name, 0) + 1
        
        dept_data = [['Department', 'Employee Count']]
        for dept_name, count in sorted(dept_employee_count.items()):
            dept_data.append([dept_name, str(count)])
        
        dept_table = Table(dept_data, colWidths=[4 * inch, 2 * inch])
        dept_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(dept_table)
        story.append(Spacer(1, 0.3 * inch))
        
        story.append(Paragraph("Employee Listing", heading_style))
        if employees:
            emp_data = [['ID', 'Name', 'Email', 'Position', 'Salary', 'Department']]
            # Limit to 50 employees per PDF to avoid memory issues with large datasets
            # Limit to 50 employees per PDF to avoid memory issues with large datasets
            for emp in employees[:50]:
                try:
                    name = f"{emp.get('first_name', '')} {emp.get('last_name', '')}".strip()
                    email = emp.get('email', 'N/A')
                    position = emp.get('position') or "N/A"
                    # Format salary with currency symbol, or show N/A if zero/None
                    salary_val = emp.get('salary')
                    salary = f"${salary_val:.2f}" if salary_val is not None and salary_val != 0 else "N/A"
                    dept = emp.get('department_name', 'N/A')
                    emp_id = str(emp.get('id', 'N/A'))
                    emp_data.append([emp_id, name, email, position, salary, dept])
                except Exception:
                    continue
            
            if len(employees) > 50:
                emp_data.append(['...', f'... and {len(employees) - 50} more employees', '', '', '', ''])
            
            emp_table = Table(emp_data, colWidths=[0.5 * inch, 1.5 * inch, 1.8 * inch, 1.2 * inch, 1 * inch, 1 * inch])
            emp_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
            ]))
            story.append(emp_table)
        else:
            story.append(Paragraph("No employees found.", styles['Normal']))
        
        story.append(Spacer(1, 0.3 * inch))
        
        story.append(Spacer(1, 0.2 * inch))
        story.append(Paragraph(f"Report generated on: {self.get_current_date()}", styles['Normal']))
        
        doc.build(story)
        return filepath

