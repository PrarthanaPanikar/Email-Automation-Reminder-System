"""
Configuration module for Email Automation System
Handles environment variables and system settings
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the email automation system"""
    
    # Email Configuration
    SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USER = os.getenv('SMTP_USER')
    SMTP_PASS = os.getenv('SMTP_PASS')
    
    # System Configuration
    DRY_RUN = os.getenv('DRY_RUN', 'True').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # File Paths
    BASE_DIR = Path(__file__).parent.parent
    CONTACTS_FILE = os.getenv('CONTACTS_FILE', str(BASE_DIR / 'data' / 'contacts.csv'))
    REMINDERS_FILE = os.getenv('REMINDERS_FILE', str(BASE_DIR / 'data' / 'reminders.csv'))
    TEMPLATES_DIR = os.getenv('TEMPLATES_DIR', str(BASE_DIR / 'templates'))
    OUTPUTS_DIR = os.getenv('OUTPUTS_DIR', str(BASE_DIR / 'outputs'))
    LOGS_DIR = os.getenv('LOGS_DIR', str(BASE_DIR / 'logs'))
    
    # Email Settings
    EMAIL_SUBJECT_PREFIX = os.getenv('EMAIL_SUBJECT_PREFIX', '[AUTOMATED]')
    MAX_RETRY_ATTEMPTS = int(os.getenv('MAX_RETRY_ATTEMPTS', '3'))
    RETRY_DELAY_SECONDS = int(os.getenv('RETRY_DELAY_SECONDS', '300'))
    
    # Logging Settings
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_MAX_BYTES = int(os.getenv('LOG_MAX_BYTES', '10485760'))  # 10MB
    LOG_BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT', '5'))
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present"""
        errors = []
        
        if not cls.SMTP_USER:
            errors.append("SMTP_USER is required")
        if not cls.SMTP_PASS:
            errors.append("SMTP_PASS is required")
        
        # Check if directories exist, create if they don't
        for dir_path in [cls.TEMPLATES_DIR, cls.OUTPUTS_DIR, cls.LOGS_DIR]:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
        
        # Check if files exist
        for file_path in [cls.CONTACTS_FILE, cls.REMINDERS_FILE]:
            if not Path(file_path).exists():
                errors.append(f"Required file not found: {file_path}")
        
        return errors
    
    @classmethod
    def get_template_path(cls, template_name):
        """Get full path to template file"""
        template_file = f"{template_name}.txt"
        return Path(cls.TEMPLATES_DIR) / template_file
    
    @classmethod
    def get_log_path(cls, log_name):
        """Get full path to log file"""
        log_file = f"{log_name}.log"
        return Path(cls.LOGS_DIR) / log_file
    
    @classmethod
    def get_output_path(cls, output_name):
        """Get full path to output file"""
        output_file = f"{output_name}.csv"
        return Path(cls.OUTPUTS_DIR) / output_file
