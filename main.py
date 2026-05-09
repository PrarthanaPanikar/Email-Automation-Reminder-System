#!/usr/bin/env python3
"""
Email Automation & Reminder System
Main entry point for the email automation application

Usage:
    python main.py [--dry-run] [--send] [--test] [--preview-template TEMPLATE_NAME]
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.config import Config
from src.logger import logger
from src.data_loader import DataLoader
from src.template_engine import TemplateEngine
from src.email_sender import EmailSender
from src.report_generator import ReportGenerator

class EmailAutomationSystem:
    """Main email automation system class"""
    
    def __init__(self):
        self.data_loader = DataLoader()
        self.template_engine = TemplateEngine()
        self.email_sender = EmailSender()
        self.report_generator = ReportGenerator()
        
        # Validate configuration
        self.validate_system()
    
    def validate_system(self):
        """Validate system configuration and requirements"""
        try:
            errors = Config.validate_config()
            if errors:
                logger.log_error("Configuration validation failed:")
                for error in errors:
                    logger.log_error(f"  - {error}")
                print("❌ Configuration validation failed:")
                for error in errors:
                    print(f"  - {error}")
                sys.exit(1)
            
            logger.log_info("System validation passed")
            print("✅ System validation passed")
            
        except Exception as e:
            logger.log_error(f"System validation error: {str(e)}")
            print(f"❌ System validation error: {str(e)}")
            sys.exit(1)
    
    def run_dry_run(self):
        """Run the system in dry-run mode (no actual emails sent)"""
        try:
            print("\n🔍 Running Email Automation System in DRY RUN mode")
            print("=" * 60)
            
            # Load data
            print("\n📊 Loading data...")
            self.data_loader.load_contacts()
            self.data_loader.load_reminders()
            merged_data = self.data_loader.merge_data()
            
            if merged_data.empty:
                print("⚠️  No data found or no matching contacts/reminders")
                return
            
            print(f"✅ Loaded {len(merged_data)} email records")
            
            # Get data summary
            summary = self.data_loader.get_data_summary()
            print(f"📈 Data Summary:")
            print(f"   - Total Contacts: {summary.get('total_contacts', 0)}")
            print(f"   - Total Reminders: {summary.get('total_reminders', 0)}")
            print(f"   - Merged Records: {summary.get('merged_records', 0)}")
            
            # Process each email
            print(f"\n📧 Processing {len(merged_data)} emails...")
            
            for idx, row in merged_data.iterrows():
                try:
                    # Create context
                    contact_data = {
                        'name': row['name'],
                        'email': row['contact_email'],
                        'phone': row.get('phone', ''),
                        'department': row.get('department', '')
                    }
                    
                    reminder_data = {
                        'reminder_title': row['reminder_title'],
                        'reminder_date': row['reminder_date'],
                        'template_name': row['template_name']
                    }
                    
                    context = self.template_engine.create_context_from_data(contact_data, reminder_data)
                    
                    # Render template
                    subject, body = self.template_engine.render_template(row['template_name'], context)
                    
                    # Simulate email sending (dry run)
                    success, message = self.email_sender.send_email(
                        row['contact_email'],
                        subject,
                        body
                    )
                    
                    # Record in report
                    self.report_generator.add_email_record(
                        row['contact_email'],
                        subject,
                        'sent' if success else 'failed',
                        row['template_name'],
                        message if not success else None
                    )
                    
                    print(f"   ✅ {idx+1}/{len(merged_data)} - {row['contact_email']} - {row['template_name']}")
                    
                except Exception as e:
                    logger.log_error(f"Error processing email {idx+1}: {str(e)}")
                    print(f"   ❌ {idx+1}/{len(merged_data)} - Error: {str(e)}")
            
            # Generate reports
            print(f"\n📋 Generating reports...")
            csv_report = self.report_generator.generate_csv_report()
            summary_report = self.report_generator.generate_text_summary()
            
            print(f"✅ CSV Report: {csv_report}")
            print(f"\n📊 Summary Report:")
            print(summary_report)
            
            print(f"\n🎉 Dry run completed successfully!")
            
        except Exception as e:
            logger.log_error(f"Dry run error: {str(e)}")
            print(f"❌ Dry run error: {str(e)}")
            sys.exit(1)
    
    def run_send_emails(self):
        """Run the system and actually send emails"""
        try:
            print("\n📧 Running Email Automation System - SENDING EMAILS")
            print("=" * 60)
            
            if Config.DRY_RUN:
                print("⚠️  WARNING: DRY_RUN is still enabled in .env file")
                print("   Emails will NOT be sent. Set DRY_RUN=False to send real emails")
                return
            
            # Test SMTP connection first
            print("\n🔌 Testing SMTP connection...")
            if not self.email_sender.test_connection():
                print("❌ SMTP connection test failed")
                sys.exit(1)
            print("✅ SMTP connection test passed")
            
            # Load and process data
            print("\n📊 Loading and processing data...")
            self.data_loader.load_contacts()
            self.data_loader.load_reminders()
            merged_data = self.data_loader.merge_data()
            
            if merged_data.empty:
                print("⚠️  No data found or no matching contacts/reminders")
                return
            
            print(f"✅ Processing {len(merged_data)} emails...")
            
            # Connect to SMTP
            with self.email_sender:
                for idx, row in merged_data.iterrows():
                    try:
                        # Create context and render template
                        contact_data = {
                            'name': row['name'],
                            'email': row['contact_email'],
                            'phone': row.get('phone', ''),
                            'department': row.get('department', '')
                        }
                        
                        reminder_data = {
                            'reminder_title': row['reminder_title'],
                            'reminder_date': row['reminder_date'],
                            'template_name': row['template_name']
                        }
                        
                        context = self.template_engine.create_context_from_data(contact_data, reminder_data)
                        subject, body = self.template_engine.render_template(row['template_name'], context)
                        
                        # Send email
                        success, message = self.email_sender.send_email_with_retry(
                            row['contact_email'],
                            subject,
                            body
                        )
                        
                        # Record in report
                        self.report_generator.add_email_record(
                            row['contact_email'],
                            subject,
                            'sent' if success else 'failed',
                            row['template_name'],
                            message if not success else None
                        )
                        
                        status_icon = "✅" if success else "❌"
                        print(f"   {status_icon} {idx+1}/{len(merged_data)} - {row['contact_email']} - {row['template_name']}")
                        
                    except Exception as e:
                        logger.log_error(f"Error processing email {idx+1}: {str(e)}")
                        print(f"   ❌ {idx+1}/{len(merged_data)} - Error: {str(e)}")
            
            # Generate reports
            print(f"\n📋 Generating reports...")
            csv_report = self.report_generator.generate_csv_report()
            summary_report = self.report_generator.generate_text_summary()
            
            print(f"✅ CSV Report: {csv_report}")
            print(f"\n📊 Summary Report:")
            print(summary_report)
            
            print(f"\n🎉 Email sending completed!")
            
        except Exception as e:
            logger.log_error(f"Email sending error: {str(e)}")
            print(f"❌ Email sending error: {str(e)}")
            sys.exit(1)
    
    def run_test_email(self):
        """Send a test email"""
        try:
            print("\n🧪 Sending test email...")
            
            if Config.DRY_RUN:
                print("⚠️  DRY_RUN mode enabled - test email will not be sent")
                return
            
            # Test SMTP connection
            if not self.email_sender.test_connection():
                print("❌ SMTP connection test failed")
                sys.exit(1)
            
            # Send test email
            with self.email_sender:
                success, message = self.email_sender.send_test_email()
            
            if success:
                print(f"✅ Test email sent successfully!")
                print(f"   Message: {message}")
            else:
                print(f"❌ Test email failed!")
                print(f"   Error: {message}")
            
        except Exception as e:
            logger.log_error(f"Test email error: {str(e)}")
            print(f"❌ Test email error: {str(e)}")
    
    def preview_template(self, template_name: str):
        """Preview a template with sample data"""
        try:
            print(f"\n👀 Previewing template: {template_name}")
            print("=" * 50)
            
            # Check if template exists
            available_templates = self.template_engine.list_available_templates()
            if template_name not in available_templates:
                print(f"❌ Template '{template_name}' not found")
                print(f"Available templates: {', '.join(available_templates)}")
                return
            
            # Get template variables
            variables = self.template_engine.get_template_variables(template_name)
            print(f"📝 Template variables: {', '.join(variables)}")
            print()
            
            # Show preview
            preview = self.template_engine.preview_template(template_name)
            print(preview)
            
        except Exception as e:
            logger.log_error(f"Template preview error: {str(e)}")
            print(f"❌ Template preview error: {str(e)}")
    
    def show_status(self):
        """Show system status and configuration"""
        try:
            print("\n📊 Email Automation System Status")
            print("=" * 50)
            
            # Configuration
            print(f"🔧 Configuration:")
            print(f"   SMTP Host: {Config.SMTP_HOST}")
            print(f"   SMTP Port: {Config.SMTP_PORT}")
            print(f"   SMTP User: {Config.SMTP_USER}")
            print(f"   Dry Run: {Config.DRY_RUN}")
            print(f"   Log Level: {Config.LOG_LEVEL}")
            
            # Available templates
            templates = self.template_engine.list_available_templates()
            print(f"\n📄 Available Templates: {len(templates)}")
            for template in templates:
                print(f"   - {template}")
            
            # Data files
            print(f"\n📁 Data Files:")
            print(f"   Contacts: {Config.CONTACTS_FILE}")
            print(f"   Reminders: {Config.REMINDERS_FILE}")
            
            # Output directories
            print(f"\n📂 Output Directories:")
            print(f"   Templates: {Config.TEMPLATES_DIR}")
            print(f"   Outputs: {Config.OUTPUTS_DIR}")
            print(f"   Logs: {Config.LOGS_DIR}")
            
            # Try to load data summary
            try:
                self.data_loader.load_contacts()
                self.data_loader.load_reminders()
                summary = self.data_loader.get_data_summary()
                
                print(f"\n📈 Data Summary:")
                print(f"   Total Contacts: {summary.get('total_contacts', 'N/A')}")
                print(f"   Total Reminders: {summary.get('total_reminders', 'N/A')}")
                print(f"   Merged Records: {summary.get('merged_records', 'N/A')}")
                
            except Exception as e:
                print(f"\n⚠️  Could not load data: {str(e)}")
            
        except Exception as e:
            logger.log_error(f"Status display error: {str(e)}")
            print(f"❌ Status display error: {str(e)}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Email Automation & Reminder System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --dry-run          # Test without sending emails
  python main.py --send             # Send actual emails
  python main.py --test             # Send test email
  python main.py --preview-template meeting_reminder
  python main.py --status           # Show system status
        """
    )
    
    parser.add_argument('--dry-run', action='store_true', 
                       help='Run in dry-run mode (no emails sent)')
    parser.add_argument('--send', action='store_true',
                       help='Send actual emails')
    parser.add_argument('--test', action='store_true',
                       help='Send a test email')
    parser.add_argument('--preview-template', metavar='TEMPLATE_NAME',
                       help='Preview a specific template')
    parser.add_argument('--status', action='store_true',
                       help='Show system status')
    
    args = parser.parse_args()
    
    # If no arguments provided, show help
    if not any(vars(args).values()):
        parser.print_help()
        return
    
    # Initialize system
    try:
        system = EmailAutomationSystem()
        
        # Execute requested action
        if args.dry_run:
            system.run_dry_run()
        elif args.send:
            system.run_send_emails()
        elif args.test:
            system.run_test_email()
        elif args.preview_template:
            system.preview_template(args.preview_template)
        elif args.status:
            system.show_status()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.log_error(f"System error: {str(e)}")
        print(f"❌ System error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
