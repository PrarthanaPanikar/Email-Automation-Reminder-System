# Installation Guide

## 🎯 System Requirements

### Minimum Requirements:
- **Python**: 3.8 or higher
- **RAM**: 2GB minimum
- **Storage**: 100MB free space
- **Internet**: Required for SMTP connection

### Recommended:
- **Python**: 3.9 or 3.10
- **RAM**: 4GB or more
- **Storage**: 500MB free space
- **IDE**: VS Code, PyCharm, or similar

---

## 🐍 Python Setup

### Windows Installation

#### Option 1: Download from python.org
1. **Download Python**
   - Go to [python.org](https://www.python.org/downloads/)
   - Download latest Python 3.8+ version
   - Run the installer

2. **Important Installation Steps**
   - ✅ Check "Add Python to PATH"
   - ✅ Check "Install for all users" (optional)
   - Click "Install Now"

3. **Verify Installation**
   ```cmd
   python --version
   pip --version
   ```

#### Option 2: Using Microsoft Store
1. Open Microsoft Store
2. Search for "Python 3.9" or higher
3. Click "Get" or "Install"
4. Verify with `python --version`

### macOS Installation

#### Option 1: Download from python.org
1. **Download Python**
   - Go to [python.org](https://www.python.org/downloads/macos/)
   - Download latest Python 3.8+ version
   - Open the downloaded .pkg file

2. **Installation Steps**
   - Follow the installer prompts
   - Enter admin password if required
   - Complete installation

3. **Verify Installation**
   ```bash
   python3 --version
   pip3 --version
   ```

#### Option 2: Using Homebrew
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.9

# Verify installation
python3 --version
```

### Linux Installation

#### Ubuntu/Debian
```bash
# Update package list
sudo apt update

# Install Python 3.8+
sudo apt install python3 python3-pip python3-venv

# Verify installation
python3 --version
pip3 --version
```

#### CentOS/RHEL/Fedora
```bash
# For CentOS/RHEL
sudo yum install python3 python3-pip

# For Fedora
sudo dnf install python3 python3-pip

# Verify installation
python3 --version
pip3 --version
```

---

## 📁 Project Setup

### Step 1: Clone or Download Project

#### Option 1: Git Clone (Recommended)
```bash
git clone <repository-url>
cd Email-Automation-Reminder-System
```

#### Option 2: Download ZIP
1. Download the ZIP file from GitHub
2. Extract to desired location
3. Navigate to project folder
4. Open terminal/command prompt in that folder

### Step 2: Create Virtual Environment

#### Windows
```cmd
# Create virtual environment
python -m venv email_automation_env

# Activate virtual environment
email_automation_env\Scripts\activate

# Verify activation (command prompt should show (email_automation_env))
```

#### macOS/Linux
```bash
# Create virtual environment
python3 -m venv email_automation_env

# Activate virtual environment
source email_automation_env/bin/activate

# Verify activation (command prompt should show (email_automation_env))
```

### Step 3: Install Dependencies

#### Install from requirements.txt
```bash
pip install -r requirements.txt
```

#### Manual Installation (if needed)
```bash
pip install pandas
pip install jinja2
pip install schedule
pip install python-dotenv
pip install secure-smtplib
```

---

## 🔧 Environment Configuration

### Step 1: Create Environment File

#### Copy the example file
```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

#### Edit the .env file
```bash
# Use any text editor to edit .env
notepad .env  # Windows
nano .env      # macOS/Linux
code .env      # VS Code
```

### Step 2: Configure Email Settings

#### For Gmail Users
1. **Enable 2-Factor Authentication**
   - Go to [Google Account settings](https://myaccount.google.com/)
   - Security → 2-Step Verification → Enable

2. **Generate App Password**
   - Go to [App Passwords](https://myaccount.google.com/apppasswords)
   - Select "Mail" for app
   - Select "Other (Custom name)" → Enter "Email Automation"
   - Copy the 16-character password

3. **Update .env file**
   ```env
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASS=your-16-character-app-password
   DRY_RUN=False
   ```

#### For Other Email Providers

**Outlook/Hotmail:**
```env
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USER=your-email@outlook.com
SMTP_PASS=your-password
```

**Yahoo Mail:**
```env
SMTP_HOST=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USER=your-email@yahoo.com
SMTP_PASS=your-app-password
```

**Custom SMTP:**
```env
SMTP_HOST=your-smtp-server.com
SMTP_PORT=587
SMTP_USER=your-username
SMTP_PASS=your-password
```

---

## 🧪 Test Installation

### Step 1: Verify Python Environment
```bash
# Check Python version
python --version

# Check installed packages
pip list

# Test imports
python -c "import pandas, jinja2, schedule; print('All imports successful')"
```

### Step 2: Test Project Structure
```bash
# List project files
dir  # Windows
ls   # macOS/Linux

# Check if all folders exist
dir data templates src outputs logs  # Windows
ls data templates src outputs logs   # macOS/Linux
```

### Step 3: Run Dry Run Test
```bash
# Test the system without sending emails
python main.py --dry-run
```

---

## 🔍 Troubleshooting

### Common Installation Issues

#### Issue 1: "Python is not recognized"
**Solution:**
- Ensure Python is added to PATH during installation
- Reinstall Python with "Add to PATH" checked
- Use full path to Python executable

#### Issue 2: "pip is not recognized"
**Solution:**
- Ensure Python is properly installed
- Try using `python -m pip` instead of `pip`
- Upgrade pip: `python -m pip install --upgrade pip`

#### Issue 3: Virtual environment activation fails
**Windows:**
```cmd
# Try PowerShell execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**macOS/Linux:**
```bash
# Check permissions
chmod +x email_automation_env/bin/activate
```

#### Issue 4: Module import errors
**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check Python path
python -c "import sys; print(sys.path)"
```

#### Issue 5: SMTP authentication fails
**Solution:**
- Verify email and password are correct
- For Gmail, ensure App Password is used (not regular password)
- Check if 2-factor authentication is enabled
- Try different SMTP port (465 with SSL, 587 with TLS)

### Platform-Specific Issues

#### Windows Issues
- **Antivirus blocking**: Add exception for Python and project folder
- **Firewall**: Allow Python through firewall for SMTP connections
- **Path issues**: Use full paths if environment variables don't work

#### macOS Issues
- **Python versions**: Use `python3` and `pip3` instead of `python` and `pip`
- **Permissions**: Use `sudo` if needed for system-wide installations
- **Gatekeeper**: Allow apps from unidentified developers for Python

#### Linux Issues
- **Package manager**: Use distribution's package manager for Python
- **Dependencies**: Install system dependencies if needed
- **Permissions**: Check file permissions for project folders

---

## 📱 IDE Setup

### Visual Studio Code (Recommended)
1. **Install VS Code**
   - Download from [code.visualstudio.com](https://code.visualstudio.com/)

2. **Install Extensions**
   - Python extension (Microsoft)
   - Python Docstring Generator
   - GitLens (for Git integration)

3. **Configure Workspace**
   - Open project folder in VS Code
   - Select Python interpreter (virtual environment)
   - Configure settings for linting and formatting

### PyCharm
1. **Install PyCharm Community**
   - Download from [jetbrains.com/pycharm](https://www.jetbrains.com/pycharm/)

2. **Configure Project**
   - Open project folder
   - Set Python interpreter to virtual environment
   - Configure run configurations

### Other Editors
- **Sublime Text**: Install Package Control and Python packages
- **Atom**: Install Python packages and script runner
- **Notepad++**: Good for simple editing, limited debugging

---

## ✅ Installation Checklist

### Before Starting:
- [ ] Python 3.8+ installed
- [ ] Git installed (for cloning)
- [ ] Text editor or IDE ready
- [ ] Internet connection available

### After Installation:
- [ ] Virtual environment created and activated
- [ ] Dependencies installed successfully
- [ ] Environment variables configured
- [ ] Project structure verified
- [ ] Dry run test passes
- [ ] Sample data files created

### Ready to Run:
- [ ] Email credentials configured
- [ ] Test emails can be sent
- [ ] Logging system works
- [ ] Reports are generated
- [ ] Project is fully functional

---

## 🎓 Next Steps

After successful installation:

1. **Read the documentation** in `/docs` folder
2. **Review the implementation plan** for step-by-step guidance
3. **Create sample data** for testing
4. **Run the system** in dry-run mode first
5. **Test with real emails** after dry-run works
6. **Customize templates** for your needs
7. **Upload to GitHub** for portfolio

---

## 🆘 Getting Help

If you encounter issues:

1. **Check the logs** in `logs/automation.log`
2. **Review troubleshooting section** above
3. **Search online** for specific error messages
4. **Create an issue** in the GitHub repository
5. **Join Python communities** for support

Remember: This is a learning project. Don't hesitate to ask for help!
