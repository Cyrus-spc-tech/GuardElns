
# GuardELNS Prototype

## Overview
GuardELNS (Guard Enhanced Learning Network Security) is a real-time network traffic monitoring and anomaly detection system designed for educational demonstration. It leverages machine learning (using a PyTorch autoencoder), synthetic traffic generation, and an interactive Streamlit dashboard to visualize network activity, detect anomalies, and profile risks. This prototype aligns with the project synopsis submitted by Khushboo Bansal, Nishtha Jain, and Tanish Gupta under Dr. Ravneet Kaur (Jan 2025).

## Features
- **Real-Time Monitoring**: Captures synthetic network traffic and updates the dashboard every 10 seconds.
- **Anomaly Detection**: Uses an autoencoder to identify unusual patterns in traffic data.
- **Risk Profiling**: Assigns risk scores and levels (Low, Medium, High) to source IPs.
- **Visualization**: Includes network graphs, anomaly trends, heatmaps, and a risk profile table.
- **IoT Simulation**: Simulates IoT traffic using MQTT for stress testing.
- **Alerting**: Triggers console alerts for high-risk events (email alerts configurable).

## Setup

### Prerequisites
- **Python 3.12**: Install from https://www.python.org/downloads/
- **Windows Environment**: Tested on Windows 10/11 with PowerShell.
- **Dependencies**: Install required Python packages.

### Installation
1. **Clone or Create Project**:
   - Create a directory `D:\Builte\GuardElns\guardelns` and copy all files into it.
   - Alternatively, use Git: `git clone <repository-url>` (if hosted).

2. **Install Dependencies**:
   - Open PowerShell in the project directory.
   - Run: `pip install -r requirements.txt`

3. **Install Npcap (Optional for Live Capture)**:
   - Download and install from https://npcap.com/.
   - Note: Live capture requires Npcap; synthetic data is used as a fallback.

4. **Install Mosquitto (for IoT Simulation)**:
   - Download the Windows installer from https://mosquitto.org/download/.
   - Run the installer and start the Mosquitto service (e.g., `mosquitto -v` in cmd to test).
   - Alternatively, use Docker: Install Docker Desktop, then `docker run -p 1883:1883 eclipse-mosquitto`.

5. **Verify Database**:
   - Ensure the `data/traffic.db` file is created after running the app (use DB Browser for SQLite to check).

## Running the Application
1. **Start the App**:
   - In PowerShell, navigate to `D:\Builte\GuardElns\guardelns`.
   - Run: `python app.py`
   - Open http://localhost:8501 in your browser.

2. **Check Output**:
   - The dashboard should display synthetic traffic data, graphs, and risk profiles.
   - Look for console logs (e.g., "Inserted 100 synthetic packets...") to confirm data generation.

## Demo Guide
- **Preparation**: Ensure all dependencies are installed and Mosquitto is running.
- **Sequence**:
  1. Start the app and show the initial dashboard (may take a moment to populate).
  2. Highlight real-time updates by observing changing graphs and tables.
  3. Demonstrate IoT simulation by monitoring MQTT traffic (optional: inject anomalies manually).
  4. Explain risk profiling and alerting with synthetic high-risk events.
- **Fallback**: If live data fails, rely on synthetic data and mention Npcap requirements.
- **Slides**: Use the uploaded synopsis images (cover page, Table of Contents, etc.) to align with pages 2-13.

## Deployment (Optional)
- **Docker**:
  - Install Docker Desktop.
  - Build the image: `docker build -t guardelns .`
  - Run the container: `docker run -p 8501:8501 guardelns`
  - Access at http://localhost:8501.

## Troubleshooting
- **Permission Errors**: Run PowerShell as Administrator or delete `models/autoencoder.pth` to retrain.
- **Empty Data**: Check console logs for capture thread activity; increase `REFRESH_INTERVAL` in `config.py` if needed.
- **Type Errors**: Ensure `preprocess.py` handles all data types correctly; verify `df.dtypes`.
- **Mosquitto Issues**: Verify the service is running (`netstat -a | find "1883"` in cmd).

## Contributors
- Khushboo Bansal
- Nishtha Jain
- Tanish Gupta
- Supervised by: Dr. Ravneet Kaur

## License
This project is for educational purposes only. No commercial use intended.
