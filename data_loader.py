"""
Data loading module for Email Automation System
Handles loading and validation of contacts and reminders data
"""

import pandas as pd
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from .logger import logger
from .config import Config

class DataLoader:
    """Handles loading and validation of CSV data files"""
    
    def __init__(self):
        self.contacts_df = None
        self.reminders_df = None
        self.merged_data = None
    
    def load_contacts(self) -> pd.DataFrame:
        """Load contacts from CSV file"""
        try:
            logger.log_info(f"Loading contacts from {Config.CONTACTS_FILE}")
            
            if not Path(Config.CONTACTS_FILE).exists():
                raise FileNotFoundError(f"Contacts file not found: {Config.CONTACTS_FILE}")
            
            self.contacts_df = pd.read_csv(Config.CONTACTS_FILE)
            
            # Validate required columns
            required_columns = ['name', 'email']
            missing_columns = [col for col in required_columns if col not in self.contacts_df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns in contacts CSV: {missing_columns}")
            
            # Validate email addresses
            self._validate_emails()
            
            logger.log_info(f"Successfully loaded {len(self.contacts_df)} contacts")
            return self.contacts_df
            
        except Exception as e:
            logger.log_error(f"Error loading contacts: {str(e)}")
            raise
    
    def load_reminders(self) -> pd.DataFrame:
        """Load reminders from CSV file"""
        try:
            logger.log_info(f"Loading reminders from {Config.REMINDERS_FILE}")
            
            if not Path(Config.REMINDERS_FILE).exists():
                raise FileNotFoundError(f"Reminders file not found: {Config.REMINDERS_FILE}")
            
            self.reminders_df = pd.read_csv(Config.REMINDERS_FILE)
            
            # Validate required columns
            required_columns = ['contact_email', 'reminder_title', 'reminder_date', 'template_name']
            missing_columns = [col for col in required_columns if col not in self.reminders_df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns in reminders CSV: {missing_columns}")
            
            # Validate and parse dates
            self._validate_dates()
            
            logger.log_info(f"Successfully loaded {len(self.reminders_df)} reminders")
            return self.reminders_df
            
        except Exception as e:
            logger.log_error(f"Error loading reminders: {str(e)}")
            raise
    
    def merge_data(self) -> pd.DataFrame:
        """Merge contacts and reminders data"""
        try:
            if self.contacts_df is None:
                self.load_contacts()
            if self.reminders_df is None:
                self.load_reminders()
            
            # Merge on email address
            self.merged_data = pd.merge(
                self.reminders_df,
                self.contacts_df,
                left_on='contact_email',
                right_on='email',
                how='inner'
            )
            
            # Remove duplicate email column
            self.merged_data = self.merged_data.drop('email', axis=1)
            
            # Sort by reminder date
            self.merged_data['reminder_date'] = pd.to_datetime(self.merged_data['reminder_date'])
            self.merged_data = self.merged_data.sort_values('reminder_date')
            
            logger.log_info(f"Successfully merged data. Total records: {len(self.merged_data)}")
            return self.merged_data
            
        except Exception as e:
            logger.log_error(f"Error merging data: {str(e)}")
            raise
    
    def _validate_emails(self):
        """Validate email addresses in contacts DataFrame"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        invalid_emails = []
        
        for idx, row in self.contacts_df.iterrows():
            email = str(row['email']).strip()
            if not re.match(email_pattern, email):
                invalid_emails.append((idx, email))
        
        if invalid_emails:
            logger.log_warning(f"Found {len(invalid_emails)} invalid email addresses")
            for idx, email in invalid_emails:
                logger.log_warning(f"Invalid email at row {idx}: {email}")
    
    def _validate_dates(self):
        """Validate and parse reminder dates"""
        invalid_dates = []
        
        for idx, row in self.reminders_df.iterrows():
            date_str = str(row['reminder_date']).strip()
            try:
                # Try different date formats
                for date_format in ['%Y-%m-%d %H:%M', '%Y-%m-%d', '%m/%d/%Y %H:%M', '%m/%d/%Y']:
                    try:
                        datetime.strptime(date_str, date_format)
                        break
                    except ValueError:
                        continue
                else:
                    invalid_dates.append((idx, date_str))
            except Exception:
                invalid_dates.append((idx, date_str))
        
        if invalid_dates:
            logger.log_warning(f"Found {len(invalid_dates)} invalid date formats")
            for idx, date_str in invalid_dates:
                logger.log_warning(f"Invalid date at row {idx}: {date_str}")
    
    def get_pending_reminders(self, current_time: datetime = None) -> pd.DataFrame:
        """Get reminders that are due or will be due soon"""
        try:
            if self.merged_data is None:
                self.merge_data()
            
            if current_time is None:
                current_time = datetime.now()
            
            # Filter reminders that are due (past or within next hour)
            due_reminders = self.merged_data[
                self.merged_data['reminder_date'] <= current_time
            ].copy()
            
            logger.log_info(f"Found {len(due_reminders)} due reminders")
            return due_reminders
            
        except Exception as e:
            logger.log_error(f"Error getting pending reminders: {str(e)}")
            return pd.DataFrame()
    
    def get_contact_by_email(self, email: str) -> Optional[Dict]:
        """Get contact information by email address"""
        try:
            if self.contacts_df is None:
                self.load_contacts()
            
            contact = self.contacts_df[self.contacts_df['email'] == email]
            if not contact.empty:
                return contact.iloc[0].to_dict()
            return None
            
        except Exception as e:
            logger.log_error(f"Error getting contact by email: {str(e)}")
            return None
    
    def get_reminders_by_template(self, template_name: str) -> pd.DataFrame:
        """Get reminders that use a specific template"""
        try:
            if self.merged_data is None:
                self.merge_data()
            
            template_reminders = self.merged_data[
                self.merged_data['template_name'] == template_name
            ]
            
            return template_reminders
            
        except Exception as e:
            logger.log_error(f"Error getting reminders by template: {str(e)}")
            return pd.DataFrame()
    
    def get_data_summary(self) -> Dict:
        """Get summary statistics of loaded data"""
        try:
            summary = {}
            
            if self.contacts_df is not None:
                summary['total_contacts'] = len(self.contacts_df)
                summary['unique_departments'] = self.contacts_df['department'].nunique() if 'department' in self.contacts_df.columns else 0
            
            if self.reminders_df is not None:
                summary['total_reminders'] = len(self.reminders_df)
                summary['unique_templates'] = self.reminders_df['template_name'].nunique()
            
            if self.merged_data is not None:
                summary['merged_records'] = len(self.merged_data)
                summary['pending_reminders'] = len(self.get_pending_reminders())
            
            return summary
            
        except Exception as e:
            logger.log_error(f"Error getting data summary: {str(e)}")
            return {}
