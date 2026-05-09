# How to Run the Email Automation System

## 🚀 Quick Start Guide

This guide provides step-by-step instructions to run the Email Automation & Reminder System.

---

## 📋 Prerequisites Checklist

Before running the system, ensure you have:

- ✅ Python 3.8+ installed
- ✅ Virtual environment created and activated
- ✅ Dependencies installed (`pip install -r requirements.txt`)
- ✅ Environment variables configured (`.env` file)
- ✅ Data files prepared (`contacts.csv`, `reminders.csv`)
- ✅ Template files created in `templates/` directory

---

## 🛠 Running the System

### Option 1: Dry Run Mode (Recommended for Testing)

**Purpose**: Test the system without sending real emails

```bash
# Run in dry-run mode
python main.py --dry-run
```

**What happens:**
- Loads and validates all data
- Processes email templates
- Simulates email sending
- Generates reports and logs
- **No actual emails are sent**

**Expected Output:**
```
🔍 Running Email Automation System in DRY RUN mode
============================================================

📊 Loading data...
✅ Loaded 10 email records

📈 Data Summary:
   - Total Contacts: 10
   - Total Reminders: 10
   - Merged Records: 10

📧 Processing 10 emails...
   ✅ 1/10 - john.doe@company.com - meeting_reminder
   ✅ 2/10 - jane.smith@company.com - payment_due
   ...

📋 Generating reports...
✅ CSV Report: outputs/email_report_20240115_143022.csv

📊 Summary Report:
Email Automation System - Summary Report
Generated: 2024-01-15 14:30:22

=== OVERVIEW ===
Total Emails Sent: 10
Successful Emails: 10
Failed Emails: 0
Success Rate: 100.0%

🎉 Dry run completed successfully!
```

### Option 2: Send Real Emails

**Purpose**: Actually send emails to recipients

⚠️ **WARNING**: This will send real emails to addresses in your CSV files!

```bash
# Send actual emails
python main.py --send
```

**What happens:**
- Validates SMTP connection
- Loads and processes data
- Sends real emails via SMTP
- Tracks success/failure
- Generates reports

**Expected Output:**
```
📧 Running Email Automation System - SENDING EMAILS
============================================================

🔌 Testing SMTP connection...
✅ SMTP connection test passed

📊 Loading and processing data...
✅ Processing 10 emails...

   ✅ 1/10 - john.doe@company.com - meeting_reminder
   ✅ 2/10 - jane.smith@company.com - payment_due
   ...

📋 Generating reports...
✅ CSV Report: outputs/email_report_20240115_143045.csv

🎉 Email sending completed!
```

### Option 3: Send Test Email

**Purpose**: Test email configuration with a single test email

```bash
# Send test email to your own address
python main.py --test
```

**Expected Output:**
```
🧪 Sending test email...

🔌 Testing SMTP connection...
✅ SMTP connection test passed

✅ Test email sent successfully!
   Message: Email sent successfully
```

### Option 4: Preview Templates

**Purpose**: See how templates will look with sample data

```bash
# Preview specific template
python main.py --preview-template meeting_reminder

# List available templates first
python main.py --status
```

**Expected Output:**
```
👀 Previewing template: meeting_reminder
==================================================

📝 Template variables: name, reminder_title, reminder_date, department

Template: meeting_reminder
Subject: Meeting Reminder: Team Meeting

Body:
Dear John Doe,

This is a friendly reminder about your upcoming meeting:

Meeting: Team Meeting
Date: 2024-01-15 10:00
Department: Sales

Please be prepared with your updates...
```

### Option 5: System Status

**Purpose**: Check system configuration and data status

```bash
# Show system status
python main.py --status
```

**Expected Output:**
```
📊 Email Automation System Status
==================================================

🔧 Configuration:
   SMTP Host: smtp.gmail.com
   SMTP Port: 587
   SMTP User: your-email@gmail.com
   Dry Run: True
   Log Level: INFO

📄 Available Templates: 3
   - meeting_reminder
   - payment_due
   - welcome_email

📈 Data Summary:
   Total Contacts: 10
   Total Reminders: 10
   Merged Records: 10
```

---

## 📊 Understanding the Output

### Generated Files

#### 1. CSV Report (`outputs/email_report_YYYYMMDD_HHMMSS.csv`)
```csv
timestamp,to_email,subject,status,template_name,error_message,date,time
2024-01-15 14:30:22,john.doe@company.com,Meeting Reminder: Team Meeting,sent,meeting_reminder,,2024-01-15,14:30:22
2024-01-15 14:30:23,jane.smith@company.com,Payment Due Notice: Payment Due,sent,payment_due,,2024-01-15,14:30:23
```

#### 2. Log Files (`logs/`)
- `automation.log` - Main system logs
- `sent.log` - Successful email sends
- `failed.log` - Failed email attempts
- `system.log` - System events

#### 3. Summary Report (displayed in terminal)
Shows statistics like:
- Total emails processed
- Success/failure rates
- Templates used
- Processing time

---

## 🔧 Troubleshooting Common Issues

### Issue 1: "Configuration validation failed"
**Solution:**
```bash
# Check .env file exists and is configured
cat .env

# Ensure required variables are set
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
```

### Issue 2: "Template not found"
**Solution:**
```bash
# Check template files exist
ls templates/

# Should show:
# meeting_reminder.txt
# payment_due.txt
# welcome_email.txt
```

### Issue 3: "CSV file not found"
**Solution:**
```bash
# Check data files exist
ls data/

# Copy example files if needed
cp data/contacts.csv.example data/contacts.csv
cp data/reminders.csv.example data/reminders.csv
```

### Issue 4: "SMTP connection failed"
**Solution:**
```bash
# Test SMTP settings with test email
python main.py --test

# Check .env configuration
# For Gmail, ensure you're using App Password, not regular password
```

### Issue 5: "No matching contacts/reminders"
**Solution:**
```bash
# Check email addresses match between files
python -c "
import pandas as pd
contacts = pd.read_csv('data/contacts.csv')
reminders = pd.read_csv('data/reminders.csv')
print('Contact emails:', contacts['email'].tolist())
print('Reminder emails:', reminders['contact_email'].tolist())
"
```

---

## 📈 Advanced Usage

### Custom Data Files

**Use different data files:**
```bash
# Edit .env file
CONTACTS_FILE=data/my_contacts.csv
REMINDERS_FILE=data/my_reminders.csv
```

### Custom Template Directory

**Use different template location:**
```bash
# Edit .env file
TEMPLATES_DIR=custom_templates
```

### Batch Processing

**Process multiple data files:**
```bash
# Create a script to process multiple files
for file in data/reminders_*.csv; do
    cp "$file" data/reminders.csv
    python main.py --dry-run
    mv outputs/email_report.csv "outputs/$(basename "$file" .csv)_report.csv"
done
```

### Scheduled Execution

**Run automatically with cron (Linux/Mac):**
```bash
# Edit crontab
crontab -e

# Add line to run daily at 9 AM
0 9 * * * cd /path/to/project && python main.py --send
```

**Run automatically with Task Scheduler (Windows):**
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger to daily
4. Action: Start program
5. Program: `python`
6. Arguments: `main.py --send`
7. Start in: Project directory

---

## 📱 Command Line Reference

### All Available Commands
```bash
python main.py --help

# Usage examples:
python main.py --dry-run              # Test without sending
python main.py --send                 # Send real emails
python main.py --test                 # Send test email
python main.py --preview-template NAME # Preview template
python main.py --status               # Show system status
```

### Command Line Options
- `--dry-run`: Run simulation without sending emails
- `--send`: Send actual emails
- `--test`: Send a single test email
- `--preview-template TEMPLATE_NAME`: Preview template rendering
- `--status`: Display system configuration and status

---

## 🔒 Security Best Practices

### Before Running with Real Emails:
1. **Verify dry-run works**: Always test with `--dry-run` first
2. **Check email addresses**: Ensure you're sending to correct recipients
3. **Test with small batches**: Start with 1-2 emails
4. **Review templates**: Check for any placeholder issues
5. **Backup data**: Keep copies of your CSV files

### Production Safety:
```bash
# Always run dry-run first
python main.py --dry-run

# Check the output carefully
cat outputs/email_report.csv

# Then send to small batch
python main.py --send
```

---

## 📊 Monitoring and Maintenance

### Daily Checks:
```bash
# Check system status
python main.py --status

# Review recent logs
tail -f logs/automation.log

# Check recent reports
ls -la outputs/ | tail -5
```

### Weekly Maintenance:
```bash
# Clean old logs (keep last 30 days)
find logs/ -name "*.log" -mtime +30 -delete

# Archive old reports
mkdir -p outputs/archive
mv outputs/email_report_*.csv outputs/archive/
```

---

## 🎯 Success Indicators

Your system is working correctly when:

✅ **Dry-run completes** without errors
✅ **All emails processed** show success status
✅ **CSV report generated** with correct data
✅ **Log files created** with detailed entries
✅ **Templates render** with correct variables
✅ **SMTP connection** test passes

---

## 🆘 Getting Help

If you encounter issues:

1. **Check the logs**: `logs/automation.log`
2. **Run status check**: `python main.py --status`
3. **Test with simple data**: Start with 1-2 records
4. **Verify configuration**: Check `.env` file
5. **Review documentation**: Check `docs/` folder

For additional help:
- Check the GitHub issues
- Review the troubleshooting guide
- Contact the project maintainer

---

## 🎉 Next Steps

After successful runs:

1. **Analyze reports**: Review generated CSV files
2. **Monitor logs**: Check for any patterns or issues
3. **Optimize templates**: Improve email content
4. **Scale up**: Add more contacts and reminders
5. **Schedule automation**: Set up regular execution

You're now ready to automate your email communications! 🚀
