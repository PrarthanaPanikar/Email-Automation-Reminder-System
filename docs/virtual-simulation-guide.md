# Virtual Simulation Guide

## 🎯 Overview

This guide explains how to safely simulate a real email automation system without sending actual emails to real people. Perfect for testing, learning, and demonstration purposes.

---

## 🔒 Safety First: Why Simulation Matters

### Risks of Real Email Testing:
- **Spam complaints**: Real recipients might mark emails as spam
- **Privacy violations**: Sending to real people without consent
- **Reputation damage**: Professional emails sent accidentally
- **Legal issues**: GDPR/CCPA compliance concerns
- **Cost implications**: Email service provider limits and charges

### Benefits of Simulation:
- **Safe testing**: No risk to real people
- **Cost-effective**: No email service charges
- **Instant feedback**: See results immediately
- **Unlimited testing**: Test as much as needed
- **Learning focus**: Concentrate on system functionality

---

## 🛠 Setting Up Simulation Environment

### Step 1: Create Dummy Contact Data

#### Sample Contacts CSV (`data/contacts.csv`)
```csv
name,email,phone,department
John Doe,john.doe@demo.local,+1234567890,Sales
Jane Smith,jane.smith@demo.local,+0987654321,HR
Mike Johnson,mike.j@demo.local,+1122334455,Marketing
Sarah Williams,sarah.w@demo.local,+5544332211,Finance
David Brown,david.b@demo.local,+9988776655,Operations
```

**Key Points:**
- Use `.local` domains to prevent real email delivery
- Include realistic names and departments
- Add phone numbers for complete data simulation
- Keep data structure consistent with real scenarios

#### Advanced Contact Data
```csv
name,email,phone,department,role,location
John Doe,john.doe@demo.local,+1-555-0101,Sales,Manager,New York
Jane Smith,jane.smith@demo.local,+1-555-0102,HR,Director,San Francisco
Mike Johnson,mike.j@demo.local,+1-555-0103,Marketing,Analyst,Chicago
Sarah Williams,sarah.w@demo.local,+1-555-0104,Finance,Lead,Boston
David Brown,david.b@demo.local,+1-555-0105,Operations,Coordinator,Austin
```

### Step 2: Create Sample Reminder Data

#### Basic Reminders CSV (`data/reminders.csv`)
```csv
contact_email,reminder_title,reminder_date,template_name
john.doe@demo.local,Team Meeting,2024-01-15 10:00,meeting_reminder
jane.smith@demo.local,Payment Due,2024-01-20 09:00,payment_due
mike.j@demo.local,Project Review,2024-01-18 14:00,meeting_reminder
sarah.w@demo.local,Quarterly Report,2024-01-25 16:00,payment_due
david.b@demo.local,Training Session,2024-01-22 11:00,meeting_reminder
```

#### Advanced Reminder Scenarios
```csv
contact_email,reminder_title,reminder_date,template_name,priority
john.doe@demo.local,Urgent Client Meeting,2024-01-15 10:00,meeting_reminder,High
jane.smith@demo.local,Monthly Payment Due,2024-01-20 09:00,payment_due,Medium
mike.j@demo.local,Code Review Session,2024-01-18 14:00,meeting_reminder,Low
sarah.w@demo.local,Financial Report Deadline,2024-01-25 16:00,payment_due,High
david.b@demo.local,New Employee Training,2024-01-22 11:00,meeting_reminder,Medium
```

### Step 3: Configure Dry Run Mode

#### Environment Configuration (`.env`)
```env
# Email Configuration (can be fake for simulation)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=test@demo.local
SMTP_PASS=fake-password-for-testing

# System Configuration
DRY_RUN=True
LOG_LEVEL=INFO

# File Paths
CONTACTS_FILE=data/contacts.csv
REMINDERS_FILE=data/reminders.csv
TEMPLATES_DIR=templates
OUTPUTS_DIR=outputs
LOGS_DIR=logs
```

**Important:** Set `DRY_RUN=True` to prevent actual email sending.

---

## 🧪 Running Simulation Tests

### Test 1: Basic Dry Run
```bash
# Run the system in dry-run mode
python main.py --dry-run
```

**Expected Output:**
```
🔍 Running Email Automation System in DRY RUN mode
============================================================

📊 Loading data...
✅ Loaded 5 email records

📈 Data Summary:
   - Total Contacts: 5
   - Total Reminders: 5
   - Merged Records: 5

📧 Processing 5 emails...
   ✅ 1/5 - john.doe@demo.local - meeting_reminder
   ✅ 2/5 - jane.smith@demo.local - payment_due
   ✅ 3/5 - mike.j@demo.local - meeting_reminder
   ✅ 4/5 - sarah.w@demo.local - payment_due
   ✅ 5/5 - david.b@demo.local - meeting_reminder

📋 Generating reports...
✅ CSV Report: outputs/email_report_20240115_143022.csv

📊 Summary Report:
Email Automation System - Summary Report
Generated: 2024-01-15 14:30:22

=== OVERVIEW ===
Total Emails Sent: 5
Successful Emails: 5
Failed Emails: 0
Success Rate: 100.0%
Unique Recipients: 5

=== TEMPLATES USED ===
- meeting_reminder: 3 emails
- payment_due: 2 emails

🎉 Dry run completed successfully!
```

### Test 2: Template Preview
```bash
# Preview specific template
python main.py --preview-template meeting_reminder
```

**Expected Output:**
```
👀 Previewing template: meeting_reminder
==================================================

📝 Template variables: name, reminder_title, reminder_date, department

Template: meeting_reminder
Subject: Meeting Reminder: {reminder_title}

Body:
Dear {name},

This is a friendly reminder about your upcoming meeting:

Meeting: {reminder_title}
Date: {reminder_date}
Department: {department}

Please be prepared with your updates and any questions you might have...
```

### Test 3: System Status Check
```bash
# Check system status
python main.py --status
```

**Expected Output:**
```
📊 Email Automation System Status
==================================================

🔧 Configuration:
   SMTP Host: smtp.gmail.com
   SMTP Port: 587
   SMTP User: test@demo.local
   Dry Run: True
   Log Level: INFO

📄 Available Templates: 3
   - meeting_reminder
   - payment_due
   - welcome_email

📁 Data Files:
   Contacts: data/contacts.csv
   Reminders: data/reminders.csv

📂 Output Directories:
   Templates: templates
   Outputs: outputs
   Logs: logs

📈 Data Summary:
   Total Contacts: 5
   Total Reminders: 5
   Merged Records: 5
```

---

## 📊 Analyzing Simulation Results

### Understanding Log Files

#### Main Log (`logs/automation.log`)
```
2024-01-15 14:30:22,123 - automation - INFO - System validation passed
2024-01-15 14:30:22,145 - automation - INFO - Loading contacts from data/contacts.csv
2024-01-15 14:30:22,167 - automation - INFO - Successfully loaded 5 contacts
2024-01-15 14:30:22,189 - automation - INFO - Successfully loaded 5 reminders
2024-01-15 14:30:22,201 - automation - INFO - Successfully merged data. Total records: 5
```

#### Success Log (`logs/sent.log`)
```
2024-01-15 14:30:22,234 - sent - INFO - Email sent successfully - To: john.doe@demo.local, Subject: Meeting Reminder: Team Meeting, Template: meeting_reminder
2024-01-15 14:30:22,256 - sent - INFO - Email sent successfully - To: jane.smith@demo.local, Subject: Payment Due Notice: Monthly Payment Due, Template: payment_due
```

### Understanding CSV Reports

#### Email Report (`outputs/email_report_YYYYMMDD_HHMMSS.csv`)
```csv
timestamp,to_email,subject,status,template_name,error_message,date,time
2024-01-15 14:30:22,john.doe@demo.local,Meeting Reminder: Team Meeting,sent,meeting_reminder,,2024-01-15,14:30:22
2024-01-15 14:30:23,jane.smith@demo.local,Payment Due Notice: Monthly Payment Due,sent,payment_due,,2024-01-15,14:30:23
```

---

## 🎭 Advanced Simulation Scenarios

### Scenario 1: High Volume Testing
```csv
# Create 100+ test contacts
name,email,phone,department
User001,user001@demo.local,+1-555-0001,Sales
User002,user002@demo.local,+1-555-0002,HR
...
User100,user100@demo.local,+1-555-0100,Marketing
```

### Scenario 2: Error Testing
```csv
# Test with invalid data
name,email,phone,department
Invalid Email,invalid-email,123456,Sales
Missing Name,,1234567890,HR
Empty Fields,test@demo.local,,,
```

### Scenario 3: Time-based Testing
```csv
# Test with different reminder times
contact_email,reminder_title,reminder_date,template_name
test@demo.local,Past Reminder,2020-01-01 10:00,meeting_reminder
test@demo.local,Future Reminder,2030-01-01 10:00,payment_due
test@demo.local,Today Reminder,2024-01-15 14:30,meeting_reminder
```

---

## 🔍 Debugging Simulation Issues

### Common Issues and Solutions

#### Issue 1: "Template not found"
**Solution:** Check template file exists in `templates/` directory
```bash
ls templates/
# Should show: meeting_reminder.txt, payment_due.txt, etc.
```

#### Issue 2: "CSV file not found"
**Solution:** Ensure CSV files exist and are properly named
```bash
ls data/
# Should show: contacts.csv, reminders.csv
```

#### Issue 3: "No matching contacts/reminders"
**Solution:** Check email addresses match between files
```python
# Check for matching emails
import pandas as pd
contacts = pd.read_csv('data/contacts.csv')
reminders = pd.read_csv('data/reminders.csv')
print("Contact emails:", contacts['email'].tolist())
print("Reminder emails:", reminders['contact_email'].tolist())
```

#### Issue 4: "Permission denied"
**Solution:** Check file permissions and directory structure
```bash
# On Windows
icacls data/ /grant Users:(OI)(CI)F

# On Mac/Linux
chmod -R 755 data/ templates/ outputs/ logs/
```

---

## 📈 Performance Testing

### Load Testing Script
```python
# test_performance.py
import time
import pandas as pd
from main import EmailAutomationSystem

def generate_test_data(num_contacts=1000):
    """Generate large test dataset"""
    contacts = []
    reminders = []
    
    for i in range(num_contacts):
        contacts.append({
            'name': f'User{i:03d}',
            'email': f'user{i:03d}@demo.local',
            'phone': f'+1-555-{i:04d}',
            'department': ['Sales', 'HR', 'Marketing', 'Finance'][i % 4]
        })
        
        reminders.append({
            'contact_email': f'user{i:03d}@demo.local',
            'reminder_title': f'Test Reminder {i}',
            'reminder_date': '2024-01-15 10:00',
            'template_name': 'meeting_reminder'
        })
    
    pd.DataFrame(contacts).to_csv('data/large_contacts.csv', index=False)
    pd.DataFrame(reminders).to_csv('data/large_reminders.csv', index=False)

def run_performance_test():
    """Run performance test"""
    system = EmailAutomationSystem()
    
    start_time = time.time()
    system.run_dry_run()
    end_time = time.time()
    
    print(f"Processed {num_contacts} emails in {end_time - start_time:.2f} seconds")
    print(f"Rate: {num_contacts / (end_time - start_time):.2f} emails/second")

if __name__ == "__main__":
    generate_test_data(1000)
    run_performance_test()
```

---

## 🎯 Simulation Best Practices

### Do's:
- ✅ Use `.local` domains for email addresses
- ✅ Test with realistic data structures
- ✅ Verify all template variables are covered
- ✅ Test error scenarios
- ✅ Monitor log files during testing
- ✅ Save and analyze generated reports

### Don'ts:
- ❌ Use real email addresses
- ❌ Send to actual people without consent
- ❌ Ignore error messages in logs
- ❌ Skip dry-run testing
- ❌ Use production credentials
- ❌ Test with sensitive data

---

## 📚 Learning Outcomes

Through simulation, you'll learn:

1. **Data Processing**: CSV handling and validation
2. **Template Systems**: Variable replacement and rendering
3. **Error Handling**: Graceful failure management
4. **Logging**: System monitoring and debugging
5. **Reporting**: Data analysis and visualization
6. **Configuration**: Environment variable management
7. **Testing**: Safe development practices

---

## 🚀 Next Steps

After successful simulation:

1. **Review Logs**: Analyze all generated log files
2. **Check Reports**: Verify CSV report accuracy
3. **Test Edge Cases**: Try invalid data scenarios
4. **Performance Test**: Test with larger datasets
5. **Document Findings**: Record test results
6. **Prepare for Production**: Plan real deployment

This simulation approach ensures you understand the system completely before moving to real email sending!
