"""
Report generator module for Email Automation System
Handles generating CSV reports and statistics
"""

import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from .logger import logger
from .config import Config

class ReportGenerator:
    """Handles report generation and statistics"""
    
    def __init__(self):
        self.report_data = []
        self.stats = {}
    
    def add_email_record(self, email_to: str, subject: str, status: str, 
                        template_name: str, error_message: str = None, 
                        timestamp: datetime = None):
        """Add an email record to the report"""
        if timestamp is None:
            timestamp = datetime.now()
        
        record = {
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'to_email': email_to,
            'subject': subject,
            'status': status,
            'template_name': template_name,
            'error_message': error_message or '',
            'date': timestamp.strftime('%Y-%m-%d'),
            'time': timestamp.strftime('%H:%M:%S')
        }
        
        self.report_data.append(record)
        logger.log_info(f"Added email record: {email_to} - {status}")
    
    def generate_csv_report(self, filename: str = None) -> str:
        """Generate CSV report of all email activities"""
        try:
            if filename is None:
                filename = f"email_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            output_path = Path(Config.OUTPUTS_DIR) / filename
            
            # Create DataFrame from report data
            df = pd.DataFrame(self.report_data)
            
            # Save to CSV
            df.to_csv(output_path, index=False)
            
            logger.log_info(f"CSV report generated: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.log_error(f"Error generating CSV report: {str(e)}")
            raise
    
    def generate_summary_report(self) -> Dict:
        """Generate summary statistics"""
        try:
            if not self.report_data:
                return {
                    'total_emails': 0,
                    'successful_emails': 0,
                    'failed_emails': 0,
                    'success_rate': 0.0,
                    'templates_used': [],
                    'unique_recipients': 0
                }
            
            df = pd.DataFrame(self.report_data)
            
            # Basic statistics
            total_emails = len(df)
            successful_emails = len(df[df['status'] == 'sent'])
            failed_emails = len(df[df['status'] == 'failed'])
            success_rate = (successful_emails / total_emails * 100) if total_emails > 0 else 0
            
            # Templates used
            templates_used = df['template_name'].unique().tolist()
            
            # Unique recipients
            unique_recipients = df['to_email'].nunique()
            
            # Errors by type
            error_counts = df[df['error_message'] != '']['error_message'].value_counts().to_dict()
            
            # Emails by date
            emails_by_date = df.groupby('date').size().to_dict()
            
            # Templates by usage
            template_usage = df['template_name'].value_counts().to_dict()
            
            summary = {
                'total_emails': total_emails,
                'successful_emails': successful_emails,
                'failed_emails': failed_emails,
                'success_rate': round(success_rate, 2),
                'templates_used': templates_used,
                'unique_recipients': unique_recipients,
                'error_counts': error_counts,
                'emails_by_date': emails_by_date,
                'template_usage': template_usage,
                'first_email': df['timestamp'].min() if not df.empty else None,
                'last_email': df['timestamp'].max() if not df.empty else None
            }
            
            self.stats = summary
            return summary
            
        except Exception as e:
            logger.log_error(f"Error generating summary report: {str(e)}")
            return {}
    
    def generate_text_summary(self) -> str:
        """Generate formatted text summary"""
        summary = self.generate_summary_report()
        
        if not summary:
            return "No data available for summary."
        
        text_summary = f"""
Email Automation System - Summary Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

=== OVERVIEW ===
Total Emails Sent: {summary['total_emails']}
Successful Emails: {summary['successful_emails']}
Failed Emails: {summary['failed_emails']}
Success Rate: {summary['success_rate']}%
Unique Recipients: {summary['unique_recipients']}

=== TEMPLATES USED ===
"""
        
        for template, count in summary.get('template_usage', {}).items():
            text_summary += f"- {template}: {count} emails\n"
        
        text_summary += f"""
=== EMAILS BY DATE ===
"""
        
        for date, count in summary.get('emails_by_date', {}).items():
            text_summary += f"- {date}: {count} emails\n"
        
        if summary.get('error_counts'):
            text_summary += f"""
=== ERRORS ===
"""
            for error, count in summary.get('error_counts', {}).items():
                text_summary += f"- {error}: {count} times\n"
        
        if summary.get('first_email') and summary.get('last_email'):
            text_summary += f"""
=== TIME RANGE ===
First Email: {summary['first_email']}
Last Email: {summary['last_email']}
"""
        
        return text_summary.strip()
    
    def save_summary_to_file(self, filename: str = None) -> str:
        """Save summary report to text file"""
        try:
            if filename is None:
                filename = f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            output_path = Path(Config.OUTPUTS_DIR) / filename
            summary_text = self.generate_text_summary()
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(summary_text)
            
            logger.log_info(f"Summary report saved: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.log_error(f"Error saving summary report: {str(e)}")
            raise
    
    def get_failed_emails(self) -> List[Dict]:
        """Get list of failed email attempts"""
        return [record for record in self.report_data if record['status'] == 'failed']
    
    def get_successful_emails(self) -> List[Dict]:
        """Get list of successful email attempts"""
        return [record for record in self.report_data if record['status'] == 'sent']
    
    def get_emails_by_template(self, template_name: str) -> List[Dict]:
        """Get emails sent using a specific template"""
        return [record for record in self.report_data if record['template_name'] == template_name]
    
    def get_emails_by_date(self, date: str) -> List[Dict]:
        """Get emails sent on a specific date (YYYY-MM-DD format)"""
        return [record for record in self.report_data if record['date'] == date]
    
    def clear_data(self):
        """Clear all report data"""
        self.report_data = []
        self.stats = {}
        logger.log_info("Report data cleared")
    
    def load_data_from_logs(self) -> bool:
        """Load report data from log files"""
        try:
            # This would parse log files to recreate report data
            # Implementation depends on log format
            logger.log_info("Loading data from log files (not implemented yet)")
            return False
            
        except Exception as e:
            logger.log_error(f"Error loading data from logs: {str(e)}")
            return False
    
    def export_to_excel(self, filename: str = None) -> str:
        """Export report to Excel format (requires openpyxl)"""
        try:
            import openpyxl
            from openpyxl.styles import Font, PatternFill
            
            if filename is None:
                filename = f"email_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            output_path = Path(Config.OUTPUTS_DIR) / filename
            
            # Create DataFrame
            df = pd.DataFrame(self.report_data)
            
            # Create Excel writer
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Email Report', index=False)
                
                # Get workbook and worksheet
                workbook = writer.book
                worksheet = writer.sheets['Email Report']
                
                # Format header row
                header_font = Font(bold=True)
                header_fill = PatternFill(start_color="CCCCCC", end_color="CCCCCC", fill_type="solid")
                
                for cell in worksheet[1]:
                    cell.font = header_font
                    cell.fill = header_fill
                
                # Auto-adjust column widths
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            logger.log_info(f"Excel report generated: {output_path}")
            return str(output_path)
            
        except ImportError:
            logger.log_warning("openpyxl not available for Excel export")
            return self.generate_csv_report(filename.replace('.xlsx', '.csv'))
        except Exception as e:
            logger.log_error(f"Error generating Excel report: {str(e)}")
            return self.generate_csv_report(filename.replace('.xlsx', '.csv'))
