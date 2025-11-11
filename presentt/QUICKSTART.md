# GuardELNS Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Internet connection (for installing dependencies)

### Installation

#### Option 1: Automated Setup (Recommended)

**Windows:**
```bash
run.bat
```

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

#### Option 2: Manual Setup

1. **Create virtual environment**
```bash
python -m venv venv
```

2. **Activate virtual environment**

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
streamlit run app.py
```

### First Time Usage

1. **Access the Dashboard**
   - Open your browser and go to `http://localhost:8501`
   - You should see the GuardELNS dashboard

2. **Start Monitoring**
   - Click the "▶️ Start" button in the sidebar
   - The system will begin capturing network traffic (simulated if Scapy is not available)

3. **Train the ML Model**
   - Wait for at least 100 packets to be captured
   - Click "🎓 Train Model" in the sidebar
   - The model will learn normal network behavior

4. **View Anomalies**
   - Navigate to the "🔍 Anomaly Detection" tab
   - See detected anomalies highlighted in red
   - Review anomaly details in the table

5. **Explore Analytics**
   - Check the "📈 Analytics" tab for network graphs and statistics
   - View protocol distribution and port activity

## 📊 Dashboard Overview

### Main Tabs

1. **📊 Dashboard** - Real-time network monitoring and key metrics
2. **🔍 Anomaly Detection** - ML-based threat detection and analysis
3. **📈 Analytics** - Network topology and traffic patterns
4. **⚙️ System Info** - Configuration and system status

### Sidebar Controls

- **Monitoring Controls**
  - Start/Stop: Begin or end traffic capture
  - Clear Data: Reset all captured data

- **ML Model Controls**
  - Train Model: Train anomaly detection model
  - Status: Shows if model is trained

- **Settings**
  - Refresh Rate: Adjust dashboard update frequency
  - Display Options: Toggle visualizations

## 🧪 Testing the System

### Run System Tests
```bash
python tests/test_system.py
```

This will test all modules:
- Traffic capture
- Anomaly detection
- IoT simulation
- Risk profiling
- Alert system
- Database operations

### Simulate IoT Traffic

The system automatically simulates IoT traffic if real network capture is not available. You'll see:
- Smart thermostats
- Security cameras
- Smart lights
- Door sensors
- Motion detectors
- Smart plugs

## 🔧 Configuration

Edit `config/config.yaml` to customize:

```yaml
network:
  interface: "auto"  # or specify "eth0", "wlan0", etc.
  packet_count: 1000

detection:
  model: "isolation_forest"  # or "autoencoder", "ocsvm", "lof"
  contamination: 0.1

visualization:
  refresh_interval: 5  # seconds
```

## 📝 Common Issues

### Issue: "Scapy not available"
**Solution:** The system will automatically use simulation mode. For real packet capture, install Scapy with admin privileges.

### Issue: "Model training failed"
**Solution:** Ensure you have at least 100 packets captured before training.

### Issue: "Port 8501 already in use"
**Solution:** Stop other Streamlit applications or change the port:
```bash
streamlit run app.py --server.port 8502
```

### Issue: "Permission denied" for network capture
**Solution:** Run with administrator/sudo privileges:
```bash
sudo streamlit run app.py  # Linux/Mac
```

## 🎯 Next Steps

1. **Explore Features**
   - Try different ML models in the config
   - Adjust contamination threshold
   - Enable email/Slack alerts

2. **Customize**
   - Add custom alert rules
   - Modify risk scoring logic
   - Create custom visualizations

3. **Deploy**
   - Set up on a dedicated server
   - Configure real network interface
   - Enable database persistence

4. **Integrate**
   - Connect to MQTT broker for IoT devices
   - Set up email notifications
   - Export data for analysis

## 📚 Documentation

- Full documentation: See `README.md`
- API reference: Check individual module docstrings
- Configuration guide: See `config/config.yaml`

## 🆘 Support

For issues and questions:
- Check the documentation
- Run system tests to diagnose problems
- Review logs in `data/logs/`

## 🎓 Project Information

**Team:**
- Khushboo Bansal (2330736)
- Nishtha Jain (2330750)
- Tanish Gupta (2330787)

**Institution:** Chandigarh Engineering College Jhanjeri, Mohali  
**Department:** Artificial Intelligence & Data Science  
**Supervisor:** Dr. Ravneet Kaur

---

**Happy Monitoring! 🛡️**
