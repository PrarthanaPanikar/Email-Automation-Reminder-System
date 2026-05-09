"""
Logging module for Email Automation System
Handles all logging operations with different log levels and file rotation
"""

import logging
import logging.handlers
from pathlib import Path
from datetime import datetime
from .config import Config

class EmailAutomationLogger:
    """Centralized logging system for the email automation application"""
    
    def __init__(self):
        self.setup_loggers()
    
    def setup_loggers(self):
        """Setup different loggers for different purposes"""
        # Ensure log directory exists
        Path(Config.LOGS_DIR).mkdir(parents=True, exist_ok=True)
        
        # Main application logger
        self.app_logger = self._create_logger(
            'automation',
            Config.get_log_path('automation'),
            logging.INFO
        )
        
        # Success logger for sent emails
        self.success_logger = self._create_logger(
            'sent',
            Config.get_log_path('sent'),
            logging.INFO
        )
        
        # Failure logger for failed emails
        self.failure_logger = self._create_logger(
            'failed',
            Config.get_log_path('failed'),
            logging.ERROR
        )
        
        # System logger for system events
        self.system_logger = self._create_logger(
            'system',
            Config.get_log_path('system'),
            logging.INFO
        )
    
    def _create_logger(self, name, log_file, level):
        """Create a logger with file rotation"""
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        # Avoid duplicate handlers
        if logger.handlers:
            return logger
        
        # Create rotating file handler
        handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=Config.LOG_MAX_BYTES,
            backupCount=Config.LOG_BACKUP_COUNT
        )
        
        # Create formatter
        formatter = logging.Formatter(Config.LOG_FORMAT)
        handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(handler)
        
        return logger
    
    def log_info(self, message, logger_type='app'):
        """Log informational message"""
        logger = getattr(self, f'{logger_type}_logger', self.app_logger)
        logger.info(message)
    
    def log_success(self, email_to, subject, template_name):
        """Log successful email sending"""
        message = f"Email sent successfully - To: {email_to}, Subject: {subject}, Template: {template_name}"
        self.success_logger.info(message)
        self.app_logger.info(message)
    
    def log_failure(self, email_to, subject, error_message):
        """Log failed email sending"""
        message = f"Email send failed - To: {email_to}, Subject: {subject}, Error: {error_message}"
        self.failure_logger.error(message)
        self.app_logger.error(message)
    
    def log_system_event(self, event_type, details):
        """Log system events"""
        message = f"System Event - {event_type}: {details}"
        self.system_logger.info(message)
        self.app_logger.info(message)
    
    def log_error(self, message, logger_type='app'):
        """Log error message"""
        logger = getattr(self, f'{logger_type}_logger', self.app_logger)
        logger.error(message)
    
    def log_warning(self, message, logger_type='app'):
        """Log warning message"""
        logger = getattr(self, f'{logger_type}_logger', self.app_logger)
        logger.warning(message)
    
    def log_debug(self, message, logger_type='app'):
        """Log debug message"""
        logger = getattr(self, f'{logger_type}_logger', self.app_logger)
        logger.debug(message)
    
    def get_log_stats(self):
        """Get statistics from log files"""
        stats = {}
        
        try:
            # Count successful emails
            sent_log = Config.get_log_path('sent')
            if sent_log.exists():
                with open(sent_log, 'r') as f:
                    stats['sent_count'] = len(f.readlines())
            else:
                stats['sent_count'] = 0
            
            # Count failed emails
            failed_log = Config.get_log_path('failed')
            if failed_log.exists():
                with open(failed_log, 'r') as f:
                    stats['failed_count'] = len(f.readlines())
            else:
                stats['failed_count'] = 0
            
            # Calculate success rate
            total = stats['sent_count'] + stats['failed_count']
            if total > 0:
                stats['success_rate'] = (stats['sent_count'] / total) * 100
            else:
                stats['success_rate'] = 0
            
        except Exception as e:
            self.log_error(f"Error getting log stats: {str(e)}")
            stats = {'sent_count': 0, 'failed_count': 0, 'success_rate': 0}
        
        return stats

# Global logger instance
logger = EmailAutomationLogger()
