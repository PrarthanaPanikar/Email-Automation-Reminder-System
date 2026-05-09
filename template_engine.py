"""
Template engine module for Email Automation System
Handles loading, parsing, and rendering of email templates
"""

import re
from pathlib import Path
from typing import Dict, Optional, Tuple
from jinja2 import Template, TemplateError
from .logger import logger
from .config import Config

class TemplateEngine:
    """Handles email template processing and rendering"""
    
    def __init__(self):
        self.template_cache = {}
        self.templates_dir = Path(Config.TEMPLATES_DIR)
    
    def load_template(self, template_name: str) -> Optional[str]:
        """Load template content from file"""
        try:
            template_path = self.templates_dir / f"{template_name}.txt"
            
            if not template_path.exists():
                logger.log_error(f"Template file not found: {template_path}")
                return None
            
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            logger.log_info(f"Successfully loaded template: {template_name}")
            return content
            
        except Exception as e:
            logger.log_error(f"Error loading template {template_name}: {str(e)}")
            return None
    
    def render_template(self, template_name: str, context: Dict) -> Tuple[str, str]:
        """
        Render template with provided context
        Returns tuple of (subject, body)
        """
        try:
            # Load template content
            template_content = self.load_template(template_name)
            if not template_content:
                raise ValueError(f"Template {template_name} not found")
            
            # Parse subject and body
            subject, body = self._parse_template_content(template_content)
            
            # Render subject and body with context
            rendered_subject = self._render_string(subject, context)
            rendered_body = self._render_string(body, context)
            
            logger.log_info(f"Successfully rendered template: {template_name}")
            return rendered_subject, rendered_body
            
        except Exception as e:
            logger.log_error(f"Error rendering template {template_name}: {str(e)}")
            raise
    
    def _parse_template_content(self, content: str) -> Tuple[str, str]:
        """Parse template content to extract subject and body"""
        lines = content.strip().split('\n')
        subject = ""
        body_lines = []
        
        # Extract subject (first line starting with "Subject:")
        for line in lines:
            line = line.strip()
            if line.lower().startswith('subject:'):
                subject = line[8:].strip()  # Remove "Subject:" prefix
            elif line:  # Non-empty line after subject
                body_lines.append(line)
        
        # If no explicit subject found, use first line as subject
        if not subject and body_lines:
            subject = body_lines.pop(0)
        
        body = '\n'.join(body_lines)
        
        return subject, body
    
    def _render_string(self, template_string: str, context: Dict) -> str:
        """Render a template string with context using Jinja2"""
        try:
            template = Template(template_string)
            rendered = template.render(**context)
            return rendered
            
        except TemplateError as e:
            logger.log_error(f"Jinja2 template error: {str(e)}")
            # Fallback to simple string replacement
            return self._simple_render(template_string, context)
        except Exception as e:
            logger.log_error(f"Error rendering template string: {str(e)}")
            raise
    
    def _simple_render(self, template_string: str, context: Dict) -> str:
        """Simple template rendering using string replacement (fallback)"""
        try:
            rendered = template_string
            for key, value in context.items():
                placeholder = f"{{{key}}}"
                rendered = rendered.replace(placeholder, str(value))
            
            # Handle missing placeholders gracefully
            missing_placeholders = re.findall(r'\{([^}]+)\}', rendered)
            for placeholder in missing_placeholders:
                rendered = rendered.replace(f"{{{placeholder}}}", f"[MISSING: {placeholder}]")
            
            return rendered
            
        except Exception as e:
            logger.log_error(f"Error in simple template rendering: {str(e)}")
            return template_string
    
    def validate_template(self, template_name: str) -> bool:
        """Validate template syntax and required variables"""
        try:
            template_content = self.load_template(template_name)
            if not template_content:
                return False
            
            subject, body = self._parse_template_content(template_content)
            
            # Check for basic template syntax
            placeholders = re.findall(r'\{([^}]+)\}', subject + body)
            
            logger.log_info(f"Template {template_name} validation passed. Found placeholders: {placeholders}")
            return True
            
        except Exception as e:
            logger.log_error(f"Template validation failed for {template_name}: {str(e)}")
            return False
    
    def get_template_variables(self, template_name: str) -> list:
        """Extract all variable names from a template"""
        try:
            template_content = self.load_template(template_name)
            if not template_content:
                return []
            
            subject, body = self._parse_template_content(template_content)
            placeholders = re.findall(r'\{([^}]+)\}', subject + body)
            
            # Remove duplicates and return sorted list
            return sorted(list(set(placeholders)))
            
        except Exception as e:
            logger.log_error(f"Error extracting template variables: {str(e)}")
            return []
    
    def list_available_templates(self) -> list:
        """List all available template files"""
        try:
            if not self.templates_dir.exists():
                logger.log_warning(f"Templates directory not found: {self.templates_dir}")
                return []
            
            template_files = []
            for file_path in self.templates_dir.glob("*.txt"):
                template_name = file_path.stem
                template_files.append(template_name)
            
            return sorted(template_files)
            
        except Exception as e:
            logger.log_error(f"Error listing templates: {str(e)}")
            return []
    
    def create_context_from_data(self, contact_data: Dict, reminder_data: Dict) -> Dict:
        """Create template context from contact and reminder data"""
        context = {}
        
        # Add contact data
        if contact_data:
            for key, value in contact_data.items():
                context[key] = value
        
        # Add reminder data
        if reminder_data:
            for key, value in reminder_data.items():
                context[key] = value
        
        # Add current date/time
        from datetime import datetime
        context['current_date'] = datetime.now().strftime('%Y-%m-%d')
        context['current_time'] = datetime.now().strftime('%H:%M:%S')
        context['current_datetime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return context
    
    def preview_template(self, template_name: str, sample_context: Dict = None) -> str:
        """Preview template with sample data"""
        try:
            if sample_context is None:
                sample_context = {
                    'name': 'John Doe',
                    'email': 'john.doe@company.com',
                    'department': 'Sales',
                    'phone': '+1234567890',
                    'reminder_title': 'Team Meeting',
                    'reminder_date': '2024-01-15 10:00'
                }
            
            subject, body = self.render_template(template_name, sample_context)
            
            preview = f"Template: {template_name}\n"
            preview += f"Subject: {subject}\n"
            preview += f"Body:\n{body}"
            
            return preview
            
        except Exception as e:
            logger.log_error(f"Error previewing template {template_name}: {str(e)}")
            return f"Error previewing template: {str(e)}"
