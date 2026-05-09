"""
Email sender module for Email Automation System
Handles SMTP connection and email sending functionality
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from typing import Tuple, Dict, Optional
from datetime import datetime
import time

from .logger import logger
from .config import Config

class EmailSender:
    """Handles email sending via SMTP"""
    
    def __init__(self):
        self.smtp_server = None
        self.connection_attempts = 0
        self.max_retries = Config.MAX_RETRY_ATTEMPTS
        self.retry_delay = Config.RETRY_DELAY_SECONDS
    
    def connect(self) -> bool:
        """Establish SMTP connection"""
        try:
            logger.log_info(f"Connecting to SMTP server: {Config.SMTP_HOST}:{Config.SMTP_PORT}")
            
            # Create SMTP server
            if Config.SMTP_PORT == 465:
                # SSL connection
                self.smtp_server = smtplib.SMTP_SSL(Config.SMTP_HOST, Config.SMTP_PORT)
                context = ssl.create_default_context()
                self.smtp_server.starttls(context=context)
            else:
                # TLS connection
                self.smtp_server = smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT)
                self.smtp_server.starttls()
            
            # Login to SMTP server
            self.smtp_server.login(Config.SMTP_USER, Config.SMTP_PASS)
            
            logger.log_info("Successfully connected to SMTP server")
            return True
            
        except Exception as e:
            logger.log_error(f"Failed to connect to SMTP server: {str(e)}")
            return False
    
    def disconnect(self):
        """Close SMTP connection"""
        try:
            if self.smtp_server:
                self.smtp_server.quit()
                logger.log_info("SMTP connection closed")
        except Exception as e:
            logger.log_error(f"Error closing SMTP connection: {str(e)}")
    
    def send_email(self, to_email: str, subject: str, body: str, 
                   from_name: str = None, reply_to: str = None) -> Tuple[bool, str]:
        """
        Send an email
        Returns tuple of (success, message)
        """
        try:
            # Check if we're in dry run mode
            if Config.DRY_RUN:
                logger.log_info(f"DRY RUN: Would send email to {to_email}")
                logger.log_info(f"DRY RUN: Subject: {subject}")
                logger.log_info(f"DRY RUN: Body preview: {body[:100]}...")
                return True, "Email would be sent (dry run mode)"
            
            # Connect to SMTP server if not connected
            if not self.smtp_server:
                if not self.connect():
                    return False, "Failed to connect to SMTP server"
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = formataddr((from_name or 'Email Automation System', Config.SMTP_USER))
            msg['To'] = to_email
            msg['Subject'] = subject
            
            if reply_to:
                msg['Reply-To'] = reply_to
            
            # Add body
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # Send email
            text = msg.as_string()
            self.smtp_server.sendmail(Config.SMTP_USER, to_email, text)
            
            logger.log_success(to_email, subject, "N/A")
            return True, "Email sent successfully"
            
        except smtplib.SMTPAuthenticationError as e:
            error_msg = f"SMTP authentication failed: {str(e)}"
            logger.log_failure(to_email, subject, error_msg)
            return False, error_msg
            
        except smtplib.SMTPRecipientsRefused as e:
            error_msg = f"Recipient refused: {str(e)}"
            logger.log_failure(to_email, subject, error_msg)
            return False, error_msg
            
        except smtplib.SMTPServerDisconnected as e:
            error_msg = f"SMTP server disconnected: {str(e)}"
            logger.log_failure(to_email, subject, error_msg)
            # Try to reconnect
            self.smtp_server = None
            return False, error_msg
            
        except Exception as e:
            error_msg = f"Unexpected error sending email: {str(e)}"
            logger.log_failure(to_email, subject, error_msg)
            return False, error_msg
    
    def send_email_with_retry(self, to_email: str, subject: str, body: str,
                            from_name: str = None, reply_to: str = None) -> Tuple[bool, str]:
        """
        Send email with retry logic
        Returns tuple of (success, message)
        """
        for attempt in range(self.max_retries):
            try:
                success, message = self.send_email(to_email, subject, body, from_name, reply_to)
                
                if success:
                    return True, message
                
                # If failed and not the last attempt, wait and retry
                if attempt < self.max_retries - 1:
                    logger.log_warning(f"Email send failed, retrying in {self.retry_delay} seconds (attempt {attempt + 1}/{self.max_retries})")
                    time.sleep(self.retry_delay)
                    
                    # Reset connection for retry
                    self.disconnect()
                    self.smtp_server = None
                
            except Exception as e:
                logger.log_error(f"Error in retry attempt {attempt + 1}: {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
        
        return False, f"Failed to send email after {self.max_retries} attempts"
    
    def test_connection(self) -> bool:
        """Test SMTP connection"""
        try:
            if self.connect():
                self.disconnect()
                logger.log_info("SMTP connection test successful")
                return True
            else:
                logger.log_error("SMTP connection test failed")
                return False
                
        except Exception as e:
            logger.log_error(f"SMTP connection test error: {str(e)}")
            return False
    
    def send_test_email(self, test_email: str = None) -> Tuple[bool, str]:
        """Send a test email to verify configuration"""
        if not test_email:
            test_email = Config.SMTP_USER
        
        subject = "Email Automation System - Test Email"
        body = f"""
This is a test email from the Email Automation System.

Test Details:
- Sent at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- SMTP Host: {Config.SMTP_HOST}
- SMTP Port: {Config.SMTP_PORT}
- Dry Run Mode: {Config.DRY_RUN}

If you received this email, your email configuration is working correctly!

Best regards,
Email Automation System
        """.strip()
        
        return self.send_email_with_retry(test_email, subject, body)
    
    def validate_email_address(self, email: str) -> bool:
        """Basic email address validation"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def get_connection_info(self) -> Dict:
        """Get current connection information"""
        return {
            'smtp_host': Config.SMTP_HOST,
            'smtp_port': Config.SMTP_PORT,
            'smtp_user': Config.SMTP_USER,
            'dry_run': Config.DRY_RUN,
            'max_retries': self.max_retries,
            'retry_delay': self.retry_delay,
            'connected': self.smtp_server is not None
        }
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()
