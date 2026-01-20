"""
Report Generation and Export - Smart Records System

This module handles generation and export of reports in multiple formats:
- Text format (.txt) - Plain text file
- PDF format (.pdf) - Formatted PDF document

The reports include:
- Summary statistics (total employees, average salary, etc.)
- Department-wise employee count
- Complete employee listing
- Complete department listing

CONCEPTS EXPLAINED:
- String formatting: Using f-strings and format specifiers to create formatted text
- File operations: Creating, writing, and saving files
- PDF generation: Using reportlab library to create PDF documents
- Table formatting: Creating aligned tables using string spacing
- Timestamp generation: Creating unique filenames with dates/times
"""

# Import datetime for generating timestamps
from datetime import datetime

# Import os for file and directory operations
import os


class ReportGenerator:
    """
    Report Generator Class
    
    This class generates comprehensive reports about employees and departments.
    It can export reports in both text and PDF formats.
    
    The generator:
    1. Queries database for data
    2. Formats data into readable report
    3. Exports to file (TXT or PDF)
    """
    
    def __init__(self, employee_model, department_model):
        """
        Initialize report generator.
        
        Args:
            employee_model: EmployeeModel instance - for getting employee data
            department_model: DepartmentModel instance - for getting department data
        """
        # Store references to models
        # These are used to query data for reports
        self.employee_model = employee_model
        self.department_model = department_model
    
    def get_current_date(self):
        """
        Get current date and time as formatted string.
        
        Returns:
            str: Formatted date/time string (e.g., "2024-01-15 14:30:22")
        """
        # datetime.now() gets current date and time
        # strftime() formats it as a string
        # "%Y-%m-%d %H:%M:%S" format: Year-Month-Day Hour:Minute:Second
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def generate_report_text(self):
        """
        Generate formatted text report.
        
        This method creates a comprehensive text report including:
        - Summary statistics
        - Department-wise employee counts
        - Employee listing (table format)
        - Department listing (table format)
        
        Returns:
            str: Complete report as formatted text string
        """
        # Get data from database
        # get_statistics() returns dict with employee statistics
        stats = self.employee_model.get_statistics()
        
        # get_all() returns list of all employees
        employees = self.employee_model.get_all()
        
        # get_all() returns list of all departments
        departments = self.department_model.get_all()
        
        # ========== BUILD REPORT HEADER ==========
        # Start building report string
        # "=" * 80 creates a line of 80 equal signs (decorative separator)
        report = "=" * 80 + "\n"
        
        # Add report title (centered)
        # " " * 25 adds 25 spaces before title (centers it approximately)
        report += " " * 25 + "SMART RECORDS SYSTEM REPORT\n"
        report += "=" * 80 + "\n\n"
        
        # ========== SUMMARY STATISTICS SECTION ==========
        report += "SUMMARY STATISTICS\n"
        report += "-" * 80 + "\n"  # Separator line (80 dashes)
        
        # Add total employees count
        # .get() safely gets value from dict, uses 0 as default if not found
        report += f"Total Employees: {stats.get('total_employees', 0)}\n"
        
        # Add total departments count
        # len() gets number of items in list
        report += f"Total Departments: {len(departments)}\n"
        
        # Add salary statistics (only if there are employees)
        # This prevents division by zero errors
        if stats.get('total_employees', 0) > 0:
            # Get salary values (use 0 as default if None)
            # The "or 0" handles None values (None or 0 evaluates to 0)
            avg_salary = stats.get('avg_salary', 0) or 0
            min_salary = stats.get('min_salary', 0) or 0
            max_salary = stats.get('max_salary', 0) or 0
            total_salary = stats.get('total_salary', 0) or 0
            
            # Format salary with currency symbol and commas
            # :,.2f formats number with:
            #   - Commas as thousand separators (50,000)
            #   - 2 decimal places (.00)
            # Example: 50000 becomes "50,000.00"
            report += f"Average Salary: ${avg_salary:,.2f}\n"
            report += f"Minimum Salary: ${min_salary:,.2f}\n"
            report += f"Maximum Salary: ${max_salary:,.2f}\n"
            report += f"Total Salary Budget: ${total_salary:,.2f}\n"
        
        # Add separator between sections
        report += "\n" + "=" * 80 + "\n\n"
        
        # ========== DEPARTMENT-WISE EMPLOYEE COUNT SECTION ==========
        report += "DEPARTMENT-WISE EMPLOYEE COUNT\n"
        report += "-" * 80 + "\n"
        
        # Count employees per department
        # Create dictionary to store counts
        # Key: department name, Value: employee count
        dept_employee_count = {}
        
        # Loop through all employees
        for emp in employees:
            # Get department name (or "No Department" if None)
            # .get() safely gets value, uses default if not found
            dept_name = emp.get('department_name', 'No Department')
            
            # Increment count for this department
            # .get(dept_name, 0) gets current count (0 if department not in dict yet)
            # Then add 1 to increment
            dept_employee_count[dept_name] = dept_employee_count.get(dept_name, 0) + 1
        
        # Add department counts to report (sorted alphabetically)
        # sorted() sorts dictionary items by key (department name)
        # .items() returns (key, value) pairs
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
            # Format: column names with spacing for alignment
            # <5 means left-align, width 5 characters
            # <25 means left-align, width 25 characters
            # This creates aligned columns
            report += f"{'ID':<5} {'Name':<25} {'Email':<25} {'Position':<15} {'Salary':<12} {'Department':<15}\n"
            report += "-" * 80 + "\n"  # Separator line under header
            
            # Add each employee as a row
            for emp in employees:
                try:
                    # Extract and format employee data
                    # Combine first and last name
                    name = f"{emp.get('first_name', '')} {emp.get('last_name', '')}".strip()
                    
                    # Get email (use "N/A" if not found)
                    email = emp.get('email', 'N/A')
                    
                    # Get position (use "N/A" if None or empty)
                    # "or" operator: if position is None/empty, use "N/A"
                    position = emp.get('position') or "N/A"
                    
                    # Format salary with currency symbol
                    salary_val = emp.get('salary')
                    # If salary exists and is not 0, format it; otherwise show "N/A"
                    # f"${salary_val:.2f}" formats as currency with 2 decimals
                    salary = f"${salary_val:.2f}" if salary_val is not None and salary_val != 0 else "N/A"
                    
                    # Get department name
                    dept = emp.get('department_name', 'N/A')
                    
                    # Get employee ID
                    emp_id = emp.get('id', 'N/A')
                    
                    # Add employee row to report
                    # Format aligns columns using spacing (<5, <25, etc.)
                    report += f"{emp_id:<5} {name:<25} {email:<25} {position:<15} {salary:<12} {dept:<15}\n"
                except Exception:
                    # Skip this employee if error occurs (prevents crash)
                    # This handles corrupted data gracefully
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
                    
                    # Get description (limit to 40 characters for table alignment)
                    # [:40] slices string to first 40 characters
                    # This prevents long descriptions from breaking table layout
                    desc = (dept.get('description') or "N/A")[:40]
                    
                    # Get department ID
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
        report += f"Report generated on: {self.get_current_date()}\n"
        report += "=" * 80 + "\n"
        
        # Return complete report string
        return report
    
    def export_to_txt(self) -> str:
        """
        Export report to text file.
        
        This method:
        1. Generates timestamp for unique filename
        2. Creates reports_output directory if it doesn't exist
        3. Writes report text to file
        4. Returns file path
        
        Returns:
            str: Path to exported text file
            
        Example:
            Returns: "reports_output/report_20240115_143022.txt"
        """
        # Generate timestamp for filename
        # strftime() formats datetime as string
        # "%Y%m%d_%H%M%S" format: YearMonthDay_HourMinuteSecond
        # Example: "20240115_143022" (January 15, 2024 at 14:30:22)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create filename with timestamp
        # f"report_{timestamp}.txt" creates: "report_20240115_143022.txt"
        filename = f"report_{timestamp}.txt"
        
        # Set output directory name
        output_dir = "reports_output"
        
        # Create directory if it doesn't exist
        # os.path.exists() checks if directory exists
        if not os.path.exists(output_dir):
            # os.makedirs() creates directory (and parent directories if needed)
            os.makedirs(output_dir)
        
        # Create full file path
        # os.path.join() combines directory and filename (handles OS differences)
        # Windows: "reports_output\\report_20240115_143022.txt"
        # Linux/Mac: "reports_output/report_20240115_143022.txt"
        filepath = os.path.join(output_dir, filename)
        
        # Write report to file
        # "with open()" automatically closes file when done (even if error occurs)
        # 'w' mode opens file for writing (overwrites if exists)
        # encoding='utf-8' ensures proper character encoding (handles special characters)
        with open(filepath, 'w', encoding='utf-8') as f:
            # Write report text to file
            # generate_report_text() returns formatted report string
            f.write(self.generate_report_text())
        
        # Return file path so caller knows where file was saved
        return filepath
    
    def export_to_pdf(self):
        """
        Export report to PDF file.
        
        This method uses the reportlab library to create a formatted PDF document.
        The PDF includes:
        - Formatted tables with styling
        - Headers and sections
        - Professional layout
        
        Returns:
            str: Path to exported PDF file
            
        Raises:
            ImportError: If reportlab library is not installed
        """
        # Try to import reportlab library
        # This is imported here (not at top) to avoid errors if library not installed
        try:
            # Import reportlab components
            # letter: Standard US letter page size (8.5 x 11 inches)
            from reportlab.lib.pagesizes import letter  # type: ignore
            
            # colors: Color definitions for styling
            from reportlab.lib import colors  # type: ignore
            
            # Styles: Pre-defined text styles and custom style creation
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle  # type: ignore
            
            # Platypus: ReportLab's page layout system
            # SimpleDocTemplate: Creates PDF document
            # Paragraph: Formatted text paragraphs
            # Spacer: Empty space
            # Table: Data tables
            # TableStyle: Table styling
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle  # type: ignore
            
            # inch: Unit conversion (1 inch = 72 points)
            from reportlab.lib.units import inch  # type: ignore
        except ImportError:
            # If reportlab is not installed, raise helpful error
            raise ImportError(
                "reportlab library is required for PDF export. "
                "Install it using: pip install reportlab"
            )
        
        # Generate timestamp for filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create PDF filename
        filename = f"report_{timestamp}.pdf"
        
        # Set output directory
        output_dir = "reports_output"
        
        # Create directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Create full file path
        filepath = os.path.join(output_dir, filename)
        
        # Create PDF document template
        # SimpleDocTemplate creates a PDF document
        # pagesize=letter sets page size to US letter (8.5 x 11 inches)
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        
        # Create story list (contains all PDF elements)
        # "Story" is ReportLab's term for a list of elements to add to PDF
        # Elements are added in order (top to bottom)
        story = []
        
        # Get default styles
        # getSampleStyleSheet() returns pre-defined styles (Heading1, Normal, etc.)
        styles = getSampleStyleSheet()
        
        # Create custom title style
        # ParagraphStyle creates a custom text style
        # parent=styles['Heading1'] inherits from Heading1 style
        # fontSize=18 sets text size to 18 points
        # textAlignment=1 means center alignment (0=left, 1=center, 2=right)
        # spaceAfter=30 adds 30 points of space after title
        title_style = ParagraphStyle(
            'CustomTitle', 
            parent=styles['Heading1'],
            fontSize=18, 
            textAlignment=1, 
            spaceAfter=30
        )
        
        # Create custom heading style
        # fontSize=14 sets text size to 14 points
        # spaceAfter=12 adds 12 points of space after heading
        heading_style = ParagraphStyle(
            'CustomHeading', 
            parent=styles['Heading2'],
            fontSize=14, 
            spaceAfter=12
        )
        
        # Add title to PDF
        # Paragraph creates formatted text paragraph
        story.append(Paragraph("Smart Records System Report", title_style))
        
        # Add spacer (empty space)
        # Spacer(1, 0.2 * inch) creates vertical space
        # 1 means width (not used for vertical spacer)
        # 0.2 * inch means 0.2 inches of height
        story.append(Spacer(1, 0.2 * inch))
        
        # Get data from database
        stats = self.employee_model.get_statistics()
        employees = self.employee_model.get_all()
        departments = self.department_model.get_all()
        
        # ========== SUMMARY STATISTICS TABLE ==========
        # Add heading
        story.append(Paragraph("Summary Statistics", heading_style))
        
        # Create table data (list of rows, each row is a list)
        # First row is header row
        summary_data = [
            ['Metric', 'Value'],  # Header row
            ['Total Employees', str(stats.get('total_employees', 0))],
            ['Total Departments', str(len(departments))]
        ]
        
        # Add salary statistics if there are employees
        if stats.get('total_employees', 0) > 0:
            # Get salary values
            avg_salary = stats.get('avg_salary', 0) or 0
            min_salary = stats.get('min_salary', 0) or 0
            max_salary = stats.get('max_salary', 0) or 0
            total_salary = stats.get('total_salary', 0) or 0
            
            # extend() adds multiple items to list
            summary_data.extend([
                ['Average Salary', f"${avg_salary:,.2f}"],
                ['Minimum Salary', f"${min_salary:,.2f}"],
                ['Maximum Salary', f"${max_salary:,.2f}"],
                ['Total Salary Budget', f"${total_salary:,.2f}"]
            ])
        
        # Create table from data
        # Table() creates a table widget
        # colWidths=[3 * inch, 3 * inch] sets column widths to 3 inches each
        summary_table = Table(summary_data, colWidths=[3 * inch, 3 * inch])
        
        # Apply table styling
        # TableStyle() creates styling rules for table
        # Rules are applied in order
        summary_table.setStyle(TableStyle([
            # Style header row (row 0)
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Gray background
            # (0, 0) means column 0, row 0 (top-left)
            # (-1, 0) means last column, row 0 (top-right)
            # This styles the entire header row
            
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # White text
            
            # Style all cells
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Left-align all cells
            # (-1, -1) means last column, last row (bottom-right)
            
            # Style header row font
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold font
            ('FONTSIZE', (0, 0), (-1, 0), 12),  # 12pt font
            
            # Add padding to header
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # 12 points padding
            
            # Style data rows (row 1 onwards)
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Beige background
            
            # Add grid lines
            ('GRID', (0, 0), (-1, -1), 1, colors.black)  # Black grid lines, 1pt width
        ]))
        
        # Add table to PDF story
        story.append(summary_table)
        
        # Add spacer after table
        story.append(Spacer(1, 0.3 * inch))
        
        # ========== DEPARTMENT-WISE EMPLOYEE COUNT TABLE ==========
        story.append(Paragraph("Department-wise Employee Count", heading_style))
        
        # Count employees per department
        dept_employee_count = {}
        for emp in employees:
            dept_name = emp.get('department_name', 'No Department')
            dept_employee_count[dept_name] = dept_employee_count.get(dept_name, 0) + 1
        
        # Create table data
        dept_data = [['Department', 'Employee Count']]  # Header row
        for dept_name, count in sorted(dept_employee_count.items()):
            dept_data.append([dept_name, str(count)])  # Data rows
        
        # Create table
        dept_table = Table(dept_data, colWidths=[4 * inch, 2 * inch])
        
        # Apply same styling as summary table
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
        
        # ========== EMPLOYEE LISTING TABLE ==========
        story.append(Paragraph("Employee Listing", heading_style))
        
        if employees:
            # Create table data
            emp_data = [['ID', 'Name', 'Email', 'Position', 'Salary', 'Department']]  # Header
            
            # Limit to 50 employees per PDF to avoid memory issues
            # [:50] slices list to first 50 items
            # Large tables can cause memory problems in PDF generation
            for emp in employees[:50]:
                try:
                    # Extract and format employee data
                    name = f"{emp.get('first_name', '')} {emp.get('last_name', '')}".strip()
                    email = emp.get('email', 'N/A')
                    position = emp.get('position') or "N/A"
                    
                    # Format salary
                    salary_val = emp.get('salary')
                    salary = f"${salary_val:.2f}" if salary_val is not None and salary_val != 0 else "N/A"
                    
                    dept = emp.get('department_name', 'N/A')
                    emp_id = str(emp.get('id', 'N/A'))
                    
                    # Add employee row
                    emp_data.append([emp_id, name, email, position, salary, dept])
                except Exception:
                    continue
            
            # If more than 50 employees, add note
            if len(employees) > 50:
                # Add row indicating more employees exist
                emp_data.append(['...', f'... and {len(employees) - 50} more employees', '', '', '', ''])
            
            # Create table with specific column widths
            # Column widths in inches: ID, Name, Email, Position, Salary, Department
            emp_table = Table(
                emp_data, 
                colWidths=[0.5 * inch, 1.5 * inch, 1.8 * inch, 1.2 * inch, 1 * inch, 1 * inch]
            )
            
            # Apply table styling
            emp_table.setStyle(TableStyle([
                # Header row styling
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),  # Smaller font for header (9pt)
                
                # Data row styling
                ('FONTSIZE', (0, 1), (-1, -1), 8),  # Even smaller for data (8pt)
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                
                # Alternating row colors
                # ROWBACKGROUNDS alternates between white and light gray
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
            ]))
            
            story.append(emp_table)
        else:
            # No employees - add message
            story.append(Paragraph("No employees found.", styles['Normal']))
        
        # Add spacer
        story.append(Spacer(1, 0.3 * inch))
        
        # ========== REPORT FOOTER ==========
        # Add more spacer
        story.append(Spacer(1, 0.2 * inch))
        
        # Add generation timestamp
        story.append(Paragraph(f"Report generated on: {self.get_current_date()}", styles['Normal']))
        
        # Build PDF document
        # build() takes the story list and creates the PDF file
        # This writes all elements to the file
        doc.build(story)
        
        # Return file path
        return filepath
