# GuardELNS Installation Guide

## 📋 Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation Methods](#installation-methods)
3. [Dependency Installation](#dependency-installation)
4. [Configuration](#configuration)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Setup](#advanced-setup)

---

## 🖥️ System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, Linux (Ubuntu 18.04+), macOS 10.14+
- **Python**: 3.8 or higher
- **RAM**: 4 GB
- **Storage**: 500 MB free space
- **Network**: Internet connection for installation

### Recommended Requirements
- **OS**: Windows 11, Ubuntu 22.04, macOS 12+
- **Python**: 3.10 or higher
- **RAM**: 8 GB or more
- **Storage**: 2 GB free space
- **CPU**: Multi-core processor
- **Network**: Stable internet connection

### Software Prerequisites
- Python 3.8+ with pip
- Git (for cloning repository)
- Administrator/sudo access (for packet capture)

---

## 🚀 Installation Methods

### Method 1: Automated Installation (Recommended)

#### Windows
```cmd
# Download and extract the project
# Navigate to project directory
cd GuardELNS

# Run the automated setup
run.bat
```

#### Linux/macOS
```bash
# Clone or download the project
cd GuardELNS

# Make script executable
chmod +x run.sh

# Run the automated setup
./run.sh
```

### Method 2: Manual Installation

#### Step 1: Clone/Download Project
```bash
# Using Git
git clone <repository-url>
cd GuardELNS

# Or download and extract ZIP file
```

#### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Create Data Directories
```bash
# Windows
mkdir data\logs data\database data\models

# Linux/macOS
mkdir -p data/logs data/database data/models
```

#### Step 5: Run Application
```bash
streamlit run app.py
```

### Method 3: Docker Installation (Advanced)

```bash
# Build Docker image
docker build -t guardelns:latest .

# Run container
docker run -p 8501:8501 guardelns:latest
```

---

## 📦 Dependency Installation

### Core Dependencies

```bash
# Install all dependencies
pip install -r requirements.txt
```

### Individual Package Installation

If you encounter issues, install packages individually:

```bash
# Web Framework
pip install streamlit==1.31.0

# Data Processing
pip install pandas==2.1.4 numpy==1.26.3

# Machine Learning
pip install scikit-learn==1.4.0 pyod==1.1.3

# Network Monitoring
pip install scapy==2.5.0

# Visualization
pip install plotly==5.18.0 matplotlib==3.8.2 seaborn==0.13.1 networkx==3.2.1

# IoT & Communication
pip install paho-mqtt==1.6.1

# Configuration & Utilities
pip install pyyaml==6.0.1 sqlalchemy==2.0.25 psutil==5.9.8 requests==2.31.0 python-dotenv==1.0.1
```

### Optional Dependencies

```bash
# For PostgreSQL support
pip install psycopg2-binary

# For advanced deep learning
pip install tensorflow  # or pytorch

# For email notifications
pip install secure-smtplib
```

---

## ⚙️ Configuration

### Basic Configuration

Edit `config/config.yaml`:

```yaml
network:
  interface: "auto"  # Change to specific interface if needed
  packet_count: 1000

detection:
  model: "isolation_forest"
  contamination: 0.1

visualization:
  refresh_interval: 5
```

### Network Interface Configuration

#### Find Your Network Interface

**Windows:**
```cmd
ipconfig
# Look for your active adapter name
```

**Linux:**
```bash
ip link show
# or
ifconfig
```

**macOS:**
```bash
networksetup -listallhardwareports
```

#### Update Configuration

```yaml
network:
  interface: "eth0"  # Linux
  # or
  interface: "en0"   # macOS
  # or
  interface: "Ethernet"  # Windows
```

### Alert Configuration

For email alerts, update:

```yaml
alerts:
  enabled: true
  email_enabled: true
  smtp_server: "smtp.gmail.com"
  smtp_port: 587
  sender_email: "your-email@gmail.com"
  receiver_email: "admin@example.com"
```

**Note:** For Gmail, you need to:
1. Enable 2-factor authentication
2. Generate an app-specific password
3. Use the app password in configuration

### Database Configuration

#### SQLite (Default)
```yaml
database:
  type: "sqlite"
  sqlite_path: "data/database/guardelns.db"
```

#### PostgreSQL (Production)
```yaml
database:
  type: "postgresql"
  postgresql_host: "localhost"
  postgresql_port: 5432
  postgresql_db: "guardelns"
  postgresql_user: "admin"
  postgresql_password: "your-password"
```

---

## ✅ Verification

### Test Installation

#### 1. Run System Tests
```bash
python tests/test_system.py
```

Expected output:
```
=== Testing Traffic Capture ===
✓ TrafficCapture initialized
✓ Capture started
✓ Captured X packets
...
✓ All tests completed successfully!
```

#### 2. Run Demo Script
```bash
python demo.py
```

Expected output:
```
🛡️  GuardELNS - Complete System Demonstration
...
✅ All modules demonstrated successfully!
```

#### 3. Start Dashboard
```bash
streamlit run app.py
```

Expected behavior:
- Browser opens automatically
- Dashboard loads at `http://localhost:8501`
- No error messages in terminal

### Verify Components

#### Check Python Version
```bash
python --version
# Should show 3.8 or higher
```

#### Check Installed Packages
```bash
pip list | grep streamlit
pip list | grep scikit-learn
pip list | grep scapy
```

#### Check Data Directories
```bash
# Windows
dir data

# Linux/macOS
ls -la data/
```

Should show: `logs/`, `database/`, `models/`

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Issue 1: "Python not found"

**Solution:**
```bash
# Windows: Add Python to PATH
# Or use full path
C:\Python310\python.exe -m pip install -r requirements.txt

# Linux/macOS: Install Python
sudo apt install python3 python3-pip  # Ubuntu
brew install python3  # macOS
```

#### Issue 2: "pip not found"

**Solution:**
```bash
# Windows
python -m ensurepip --upgrade

# Linux
sudo apt install python3-pip

# macOS
python3 -m ensurepip --upgrade
```

#### Issue 3: "Scapy not working" / "Permission denied"

**Solution:**

**Windows:**
- Install Npcap: https://npcap.com/
- Run as Administrator

**Linux:**
```bash
# Install dependencies
sudo apt install python3-dev libpcap-dev

# Run with sudo
sudo streamlit run app.py
```

**macOS:**
```bash
# Install libpcap
brew install libpcap

# Run with sudo
sudo streamlit run app.py
```

**Alternative:** Use simulation mode (automatic fallback)

#### Issue 4: "Port 8501 already in use"

**Solution:**
```bash
# Use different port
streamlit run app.py --server.port 8502

# Or kill existing process
# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Linux/macOS
lsof -ti:8501 | xargs kill -9
```

#### Issue 5: "Module not found" errors

**Solution:**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Or install specific package
pip install <package-name>
```

#### Issue 6: "Database locked" error

**Solution:**
```bash
# Close all instances of the application
# Delete database file
rm data/database/guardelns.db  # Linux/macOS
del data\database\guardelns.db  # Windows

# Restart application
```

#### Issue 7: "Model training failed"

**Solution:**
- Ensure at least 100 packets captured
- Wait longer for traffic generation
- Check data quality
- Try different model type in config

#### Issue 8: Virtual environment issues

**Solution:**
```bash
# Delete and recreate venv
rm -rf venv  # Linux/macOS
rmdir /s venv  # Windows

# Create new venv
python -m venv venv

# Activate and reinstall
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

#### Issue 9: Streamlit not opening browser

**Solution:**
```bash
# Manually open browser
# Navigate to: http://localhost:8501

# Or specify browser
streamlit run app.py --browser.serverAddress localhost
```

#### Issue 10: Memory errors

**Solution:**
- Reduce packet_count in config
- Clear old data regularly
- Increase system RAM
- Use database cleanup:
```python
from src.database.db_manager import DatabaseManager
db = DatabaseManager()
db.clear_old_data(days=7)
```

---

## 🔬 Advanced Setup

### Production Deployment

#### 1. Use PostgreSQL
```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Create database
sudo -u postgres createdb guardelns

# Update config.yaml
```

#### 2. Set Up Systemd Service (Linux)

Create `/etc/systemd/system/guardelns.service`:
```ini
[Unit]
Description=GuardELNS Network Security
After=network.target

[Service]
Type=simple
User=guardelns
WorkingDirectory=/opt/guardelns
ExecStart=/opt/guardelns/venv/bin/streamlit run app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable guardelns
sudo systemctl start guardelns
```

#### 3. Configure Reverse Proxy (Nginx)

```nginx
server {
    listen 80;
    server_name guardelns.example.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

#### 4. Enable HTTPS

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d guardelns.example.com
```

### Docker Deployment

#### Create Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

#### Build and Run
```bash
docker build -t guardelns:latest .
docker run -d -p 8501:8501 --name guardelns guardelns:latest
```

### Cloud Deployment

#### AWS EC2
1. Launch EC2 instance (Ubuntu 22.04)
2. Install dependencies
3. Clone repository
4. Configure security groups (port 8501)
5. Run application

#### Google Cloud Platform
```bash
# Deploy to Cloud Run
gcloud run deploy guardelns \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### Azure
```bash
# Deploy to Azure App Service
az webapp up --name guardelns --runtime "PYTHON:3.10"
```

---

## 📊 Performance Optimization

### 1. Database Optimization
```python
# Regular cleanup
db.clear_old_data(days=30)

# Index optimization
# Add indexes to frequently queried columns
```

### 2. Memory Management
```yaml
# Reduce packet buffer
network:
  packet_count: 500  # Instead of 1000
```

### 3. Caching
```python
# Use Streamlit caching
@st.cache_data
def load_data():
    # Your data loading code
    pass
```

---

## 🆘 Getting Help

### Resources
- **Documentation**: README.md, QUICKSTART.md
- **Demo**: Run `python demo.py`
- **Tests**: Run `python tests/test_system.py`
- **Logs**: Check `data/logs/guardelns.log`

### Support Channels
- GitHub Issues
- Project documentation
- Team contact

### Reporting Issues

When reporting issues, include:
1. Operating system and version
2. Python version
3. Error message (full traceback)
4. Steps to reproduce
5. Configuration file (remove sensitive data)

---

## ✅ Post-Installation Checklist

- [ ] Python 3.8+ installed
- [ ] All dependencies installed
- [ ] Virtual environment activated
- [ ] Data directories created
- [ ] Configuration file updated
- [ ] System tests passed
- [ ] Demo script runs successfully
- [ ] Dashboard accessible
- [ ] No error messages

---

**Installation Complete! 🎉**

Proceed to [QUICKSTART.md](QUICKSTART.md) for usage instructions.
