# System Architecture & Data Flow Design

## 🏗️ System Architecture Overview

### High-Level Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Input Layer   │    │ Processing Layer│    │  Output Layer   │
│                 │    │                 │    │                 │
│ • Contact CSV   │───▶│ • Template      │───▶│ • Sent Emails   │
│ • Reminder CSV  │    │   Engine        │    │ • Failed Emails │
│ • Email Templates│   │ • Scheduler     │    │ • Reports       │
│ • Config Files  │    │ • Email Sender  │    │ • Logs          │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Component Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                    Email Automation System                     │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │   Config    │  │   Data      │  │  Template   │  │ Logger  │ │
│  │   Manager   │  │   Loader    │  │   Engine    │  │ Service │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │  Scheduler  │  │   Email     │  │   Report    │  │ Error   │ │
│  │   Service   │  │   Sender    │  │ Generator   │  │ Handler │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │    SMTP     │  │   CSV       │  │   Log       │  │  Output │ │
│  │  Provider   │  │   Writer    │  │   Writer    │  │ Manager │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## 📊 Data Flow Diagram

### Complete Data Flow
```
┌─────────────────┐
│   contacts.csv  │
├─────────────────┤
│ name            │
│ email           │
│ phone           │
│ department      │
└─────────────────┘
        │
        ▼
┌─────────────────┐
│  reminders.csv  │
├─────────────────┤
│ contact_email   │
│ reminder_title  │
│ reminder_date   │
│ template_name   │
└─────────────────┘
        │
        ▼
┌─────────────────┐
│   templates/    │
│   *.txt files   │
├─────────────────┤
│ Subject: ...    │
│ Dear {name},    │
│ {reminder_title}│
│ {reminder_date} │
└─────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Processing Pipeline                          │
├─────────────────────────────────────────────────────────────────┤
│ 1. Load Contacts & Reminders                                     │
│ 2. Match contacts with reminders                                │
│ 3. Load appropriate template                                    │
│ 4. Personalize template with contact data                       │
│ 5. Schedule email delivery                                       │
│ 6. Send email via SMTP                                          │
│ 7. Log success/failure                                          │
│ 8. Generate reports                                             │
└─────────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   sent.log      │  │  failed.log     │  │  report.csv     │
├─────────────────┤  ├─────────────────┤  ├─────────────────┤
│ timestamp       │  │ timestamp       │  │ name            │
│ email           │  │ email           │  │ email           │
│ subject         │  │ subject         │  │ subject         │
│ status          │  │ error           │  │ status          │
└─────────────────┘  └─────────────────┘  │ timestamp       │
                                             └─────────────────┘
```

## 🔧 Module Architecture

### 1. Configuration Module
```python
# config.py
class Config:
    - SMTP settings
    - File paths
    - Logging levels
    - Security settings
```

### 2. Data Loading Module
```python
# data_loader.py
class DataLoader:
    - load_contacts()
    - load_reminders()
    - validate_data()
    - merge_data()
```

### 3. Template Engine Module
```python
# template_engine.py
class TemplateEngine:
    - load_template()
    - render_template()
    - validate_template()
    - cache_templates()
```

### 4. Email Sender Module
```python
# email_sender.py
class EmailSender:
    - connect_smtp()
    - send_email()
    - handle_attachments()
    - track_delivery()
```

### 5. Scheduler Module
```python
# scheduler.py
class Scheduler:
    - schedule_emails()
    - process_queue()
    - handle_retries()
    - cleanup_completed()
```

### 6. Logging Module
```python
# logger.py
class Logger:
    - log_success()
    - log_failure()
    - log_system_events()
    - rotate_logs()
```

### 7. Report Generator Module
```python
# report_generator.py
class ReportGenerator:
    - generate_csv_report()
    - calculate_statistics()
    - create_summary()
    - export_data()
```

## 🔄 Processing Workflow

### Step-by-Step Processing
```
1. INITIALIZATION
   ├─ Load configuration
   ├─ Setup logging
   ├─ Validate environment
   └─ Initialize modules

2. DATA LOADING
   ├─ Read contacts.csv
   ├─ Read reminders.csv
   ├─ Validate email addresses
   ├─ Check template existence
   └─ Merge contact+reminder data

3. TEMPLATE PROCESSING
   ├─ Load template file
   ├─ Validate template syntax
   ├─ Replace variables
   ├─ Generate subject/body
   └─ Validate output

4. SCHEDULING
   ├─ Parse reminder dates
   ├─ Sort by priority
   ├─ Create send queue
   ├─ Set retry schedule
   └─ Start scheduler

5. EMAIL SENDING
   ├─ Connect to SMTP
   ├─ Compose email
   ├─ Send message
   ├─ Track response
   └─ Handle errors

6. LOGGING & REPORTING
   ├─ Log success/failure
   ├─ Update statistics
   ├─ Generate reports
   ├─ Cleanup old logs
   └─ Send notifications
```

## 📁 File System Architecture

### Input Files Structure
```
data/
├── contacts.csv
│   ├── Header: name,email,phone,department
│   ├── Row: John Doe,john@email.com,+1234567890,Sales
│   └── Row: Jane Smith,jane@email.com,+0987654321,HR
│
└── reminders.csv
    ├── Header: contact_email,reminder_title,reminder_date,template_name
    ├── Row: john@email.com,Team Meeting,2024-01-15 10:00,meeting_reminder
    └── Row: jane@email.com,Payment Due,2024-01-20 09:00,payment_due
```

### Template Files Structure
```
templates/
├── meeting_reminder.txt
│   ├── Subject: Meeting Reminder: {reminder_title}
│   └── Body: Dear {name},\n\nReminder about {reminder_title}...
│
├── payment_due.txt
│   ├── Subject: Payment Due: {reminder_title}
│   └── Body: Dear {name},\n\nYour payment {reminder_title}...
│
└── welcome_email.txt
    ├── Subject: Welcome to Our Team!
    └── Body: Dear {name},\n\nWelcome to {department}...
```

### Output Files Structure
```
outputs/
├── email_report.csv
│   ├── Header: name,email,subject,status,timestamp,error
│   └── Data: All email send attempts with status
│
└── statistics.json
    ├── total_sent: 150
    ├── total_failed: 5
    ├── success_rate: 96.7%
    └── processing_time: "00:15:30"

logs/
├── automation.log
│   ├── 2024-01-15 10:00:00 - INFO - System started
│   ├── 2024-01-15 10:00:01 - INFO - Loaded 50 contacts
│   └── 2024-01-15 10:00:02 - SUCCESS - Email sent to john@email.com
│
├── sent.log
│   └── All successful email deliveries
│
└── failed.log
    └── All failed email attempts with error details
```

## 🔒 Security Architecture

### Data Protection
```
┌─────────────────────────────────────────────────────────────────┐
│                    Security Layer                               │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │ Environment │  │   Input      │  │   Email     │  │   Log   │ │
│  │ Variables   │  │ Validation  │  │ Encryption  │  │ Security│ │
│  │ Protection  │  │ & Sanitization│  │ Transport  │  │ PII     │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │   Rate      │  │   Error     │  │   Access    │  │  Audit  │ │
│  │ Limiting    │  │   Handling  │  │   Control   │  │ Trail   │ │
│  │ Protection  │  │ Prevention  │  │ Mechanisms  │  │ Logging │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Security Measures
1. **Environment Variables**: Sensitive data in `.env` files
2. **Input Validation**: Email format validation, SQL injection prevention
3. **Rate Limiting**: Prevent spam and API abuse
4. **Error Handling**: Don't expose sensitive information in errors
5. **Logging Security**: Don't log PII, secure log storage
6. **Access Control**: File permissions, user authentication

## 🚀 Performance Considerations

### Scalability Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                    Performance Layer                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │ Connection  │  │   Batch     │  │   Async     │  │  Cache  │ │
│  │   Pooling   │  │ Processing  │  │ Operations  │  │ Layer   │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │   Memory    │  │   Disk      │  │   Network   │  │ Monitor │ │ │
│  │ Management  │  │   I/O       │  │ Optimization│  │ & Alert │ │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Optimization Strategies
1. **Batch Processing**: Process emails in batches
2. **Connection Pooling**: Reuse SMTP connections
3. **Memory Management**: Efficient data structures
4. **Async Operations**: Non-blocking I/O where possible
5. **Caching**: Template caching, data caching
6. **Monitoring**: Performance metrics and alerts

This architecture provides a solid foundation for a scalable, secure, and maintainable email automation system that can grow from a student project to a production-grade system.
