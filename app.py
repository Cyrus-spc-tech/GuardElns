"""
GuardELNS - Main Streamlit Application
Enterprise-Level Network Security Dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np
import time
import yaml
from datetime import datetime
import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from monitoring.traffic_capture import TrafficCapture
from detection.anomaly_detector import AnomalyDetector
from visualization.dashboard import (
    create_protocol_pie_chart,
    create_traffic_timeline,
    create_anomaly_scatter,
    create_port_heatmap,
    create_network_graph,
    create_risk_gauge
)

# Page configuration
st.set_page_config(
    page_title="GuardELNS - Network Security",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .alert-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .alert-danger {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
    }
    .alert-warning {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
    }
    .alert-success {
        background-color: #e8f5e9;
        border-left: 4px solid #4caf50;
    }
</style>
""", unsafe_allow_html=True)

# Load configuration
@st.cache_resource
def load_config():
    try:
        with open('config/config.yaml', 'r') as f:
            return yaml.safe_load(f)
    except:
        return {
            'network': {'interface': 'auto', 'packet_count': 1000},
            'detection': {'model': 'isolation_forest', 'contamination': 0.1},
            'visualization': {'refresh_interval': 5}
        }

config = load_config()

# Initialize session state
if 'capture' not in st.session_state:
    st.session_state.capture = TrafficCapture(
        interface=config['network']['interface'],
        packet_count=config['network']['packet_count']
    )

if 'detector' not in st.session_state:
    st.session_state.detector = AnomalyDetector(
        model_type=config['detection']['model'],
        contamination=config['detection']['contamination']
    )

if 'is_monitoring' not in st.session_state:
    st.session_state.is_monitoring = False

if 'model_trained' not in st.session_state:
    st.session_state.model_trained = False

if 'anomaly_count' not in st.session_state:
    st.session_state.anomaly_count = 0

if 'total_analyzed' not in st.session_state:
    st.session_state.total_analyzed = 0

# Header
st.markdown('<div class="main-header">🛡️ GuardELNS</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Guard for Enterprise-Level Network Security</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/security-checked.png", width=100)
    st.title("Control Panel")
    
    st.markdown("---")
    
    # Monitoring controls
    st.subheader("🔍 Monitoring")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ Start", use_container_width=True, disabled=st.session_state.is_monitoring):
            st.session_state.capture.start_capture()
            st.session_state.is_monitoring = True
            st.success("Monitoring started!")
            st.rerun()
    
    with col2:
        if st.button("⏹️ Stop", use_container_width=True, disabled=not st.session_state.is_monitoring):
            st.session_state.capture.stop_capture()
            st.session_state.is_monitoring = False
            st.info("Monitoring stopped!")
            st.rerun()
    
    if st.button("🗑️ Clear Data", use_container_width=True):
        st.session_state.capture.clear_packets()
        st.session_state.anomaly_count = 0
        st.session_state.total_analyzed = 0
        st.success("Data cleared!")
        st.rerun()
    
    st.markdown("---")
    
    # Model controls
    st.subheader("🤖 ML Model")
    
    if st.button("🎓 Train Model", use_container_width=True):
        with st.spinner("Training model..."):
            df = st.session_state.capture.get_packets_df()
            if len(df) >= 100:
                success = st.session_state.detector.train(df)
                if success:
                    st.session_state.model_trained = True
                    st.success("Model trained successfully!")
                else:
                    st.error("Training failed!")
            else:
                st.warning(f"Need at least 100 packets. Current: {len(df)}")
        st.rerun()
    
    model_status = "✅ Trained" if st.session_state.model_trained else "❌ Not Trained"
    st.info(f"Status: {model_status}")
    
    st.markdown("---")
    
    # Settings
    st.subheader("⚙️ Settings")
    
    refresh_rate = st.slider(
        "Refresh Rate (seconds)",
        min_value=1,
        max_value=10,
        value=config['visualization']['refresh_interval']
    )
    
    show_network_graph = st.checkbox("Show Network Graph", value=True)
    show_heatmap = st.checkbox("Show Port Heatmap", value=True)
    
    st.markdown("---")
    
    # Info
    st.subheader("ℹ️ About")
    st.caption("GuardELNS v1.0")
    st.caption("AI-Powered Network Security")
    st.caption("© 2025 CEC Jhanjeri")

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🔍 Anomaly Detection", "📈 Analytics", "⚙️ System Info"])

with tab1:
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    stats = st.session_state.capture.get_stats()
    
    with col1:
        st.metric(
            label="Total Packets",
            value=f"{stats['total_packets']:,}",
            delta=f"+{stats['total_packets'] - st.session_state.total_analyzed}" if st.session_state.total_analyzed > 0 else None
        )
    
    with col2:
        st.metric(
            label="Anomalies Detected",
            value=st.session_state.anomaly_count,
            delta=None
        )
    
    with col3:
        anomaly_rate = (st.session_state.anomaly_count / max(st.session_state.total_analyzed, 1)) * 100
        st.metric(
            label="Anomaly Rate",
            value=f"{anomaly_rate:.2f}%",
            delta=None
        )
    
    with col4:
        status = "🟢 Active" if st.session_state.is_monitoring else "🔴 Inactive"
        st.metric(
            label="Status",
            value=status,
            delta=None
        )
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(
            create_protocol_pie_chart(stats),
            use_container_width=True
        )
    
    with col2:
        df = st.session_state.capture.get_packets_df(limit=100)
        st.plotly_chart(
            create_traffic_timeline(df),
            use_container_width=True
        )
    
    # Risk gauge
    risk_score = min(anomaly_rate * 10, 100)
    st.plotly_chart(
        create_risk_gauge(risk_score),
        use_container_width=True
    )
    
    # Recent packets table
    st.subheader("📋 Recent Network Activity")
    if not df.empty:
        display_df = df[['timestamp', 'src_ip', 'dst_ip', 'protocol', 'src_port', 'dst_port', 'length']].tail(20)
        st.dataframe(display_df, use_container_width=True, height=300)
    else:
        st.info("No packets captured yet. Start monitoring to see network activity.")

with tab2:
    st.header("🔍 Anomaly Detection")
    
    if not st.session_state.model_trained:
        st.warning("⚠️ Model not trained yet. Capture at least 100 packets and train the model from the sidebar.")
    else:
        df = st.session_state.capture.get_packets_df()
        
        if not df.empty and len(df) >= 10:
            # Detect anomalies
            predictions = st.session_state.detector.predict(df)
            scores = st.session_state.detector.get_anomaly_scores(df)
            
            # Update counts
            st.session_state.anomaly_count = int(predictions.sum())
            st.session_state.total_analyzed = len(predictions)
            
            # Anomaly scatter plot
            st.plotly_chart(
                create_anomaly_scatter(df, predictions, scores),
                use_container_width=True
            )
            
            # Anomaly details
            if st.session_state.anomaly_count > 0:
                st.markdown('<div class="alert-box alert-danger">⚠️ <b>Anomalies Detected!</b></div>', unsafe_allow_html=True)
                
                anomaly_df = df[predictions == 1].copy()
                anomaly_df['anomaly_score'] = scores[predictions == 1]
                anomaly_df = anomaly_df.sort_values('anomaly_score', ascending=False)
                
                st.subheader("🚨 Detected Anomalies")
                st.dataframe(
                    anomaly_df[['timestamp', 'src_ip', 'dst_ip', 'protocol', 'length', 'anomaly_score']],
                    use_container_width=True
                )
            else:
                st.markdown('<div class="alert-box alert-success">✅ <b>No anomalies detected. Network appears normal.</b></div>', unsafe_allow_html=True)
        else:
            st.info("Collecting data... Need at least 10 packets for analysis.")

with tab3:
    st.header("📈 Network Analytics")
    
    df = st.session_state.capture.get_packets_df()
    
    if not df.empty:
        # Port heatmap
        if show_heatmap:
            st.plotly_chart(
                create_port_heatmap(df),
                use_container_width=True
            )
        
        # Network graph
        if show_network_graph:
            st.plotly_chart(
                create_network_graph(df, limit=50),
                use_container_width=True
            )
        
        # Statistics
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Protocol Statistics")
            protocol_counts = df['protocol'].value_counts()
            st.bar_chart(protocol_counts)
        
        with col2:
            st.subheader("🔌 Top Destination Ports")
            top_ports = df['dst_port'].value_counts().head(10)
            st.bar_chart(top_ports)
    else:
        st.info("No data available for analytics. Start monitoring to collect data.")

with tab4:
    st.header("⚙️ System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔧 Configuration")
        st.json({
            "Network Interface": config['network']['interface'],
            "Detection Model": config['detection']['model'],
            "Contamination": config['detection']['contamination'],
            "Packet Count": config['network']['packet_count']
        })
    
    with col2:
        st.subheader("📊 System Status")
        st.json({
            "Monitoring Active": st.session_state.is_monitoring,
            "Model Trained": st.session_state.model_trained,
            "Total Packets": stats['total_packets'],
            "Anomalies": st.session_state.anomaly_count
        })
    
    st.markdown("---")
    
    st.subheader("👥 Project Team")
    team_data = {
        "Name": ["Khushboo Bansal", "Nishtha Jain", "Tanish Gupta"],
        "Roll No": ["2330736", "2330750", "2330787"],
        "Role": ["Developer", "Developer", "Developer"]
    }
    st.table(pd.DataFrame(team_data))
    
    st.markdown("---")
    
    st.subheader("🎓 Institution")
    st.info("""
    **Chandigarh Engineering College Jhanjeri, Mohali**  
    Department of Artificial Intelligence & Data Science  
    Affiliated to I.K. Gujral Punjab Technical University, Jalandhar  
    Batch: 2023-2027
    """)

# Auto-refresh
if st.session_state.is_monitoring:
    time.sleep(refresh_rate)
    st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "GuardELNS v1.0 | © 2025 CEC Jhanjeri | AI-Powered Network Security"
    "</div>",
    unsafe_allow_html=True
)
