# GuardELNS Prototype

## Overview

GuardELNS (Guard Enhanced Learning Network Security) is a real-time network traffic monitoring and anomaly detection system designed for educational demonstration purposes. It utilizes machine learning (via a PyTorch autoencoder), synthetic traffic generation, and an interactive Streamlit dashboard to visualize network activity, detect anomalies, and profile risks. This prototype is based on the project synopsis submitted by Khushboo Bansal, Nishtha Jain, and Tanish Gupta under the guidance of Dr. Ravneet Kaur (January 2025).

## Features

- **Real-Time Monitoring**: Captures synthetic network traffic and refreshes the dashboard every 10 seconds.
- **Anomaly Detection**: Employs an autoencoder to identify irregular patterns in traffic data.
- **Risk Profiling**: Assigns risk scores and levels (Low, Medium, High) to source IPs.
- **Visualization**: Provides network graphs, anomaly trends, heatmaps, and a risk profile table.
- **IoT Simulation**: Simulates IoT traffic using MQTT for stress testing purposes.
- **Alerting**: Generates console alerts for high-risk events (email alerts can be configured).

## Setup

### Prerequisites

- **Python 3.12**: Download from https://www.python.org/downloads/.
- **Windows Environment**: Tested on Windows 10/11 using PowerShell.
- **Dependencies**: Ensure all required Python packages are installed.

### Installation

1. **Clone or Create Project**:
   - Create a directory `D:\Builte\GuardElns\guardelns` and copy all files into it.
   - Alternatively, use Git: `git clone <repository-url>` (if hosted).

2. **Install Dependencies**:
   - Open PowerShell in the project directory.
   - Run: `pip install -r requirements.txt`.

3. **Install Npcap (Optional for Live Capture)**:
   - Download and install from https://npcap.com/.
   - Note: Live capture requires Npcap; synthetic data will be used as a fallback.

4. **Install Mosquitto (for IoT Simulation)**:
   - Download and install Mosquitto for simulating IoT traffic.
