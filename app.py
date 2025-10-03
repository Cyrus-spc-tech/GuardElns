import streamlit as st
import time
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from database import init_db, get_latest_traffic
from preprocess import preprocess_traffic
from anomaly_detection import train_model, detect_anomalies
from risk_profiling import risk_profiling
from alerting import check_for_alerts
from capture import start_capture_thread
from iot_simulation import start_simulation_thread
from config import DB_PATH, REFRESH_INTERVAL

# Initialize
conn = init_db(DB_PATH)
start_capture_thread()  
start_simulation_thread()  

st.title("GuardELNS Dashboard")

placeholder = st.empty()
while True:
    with placeholder.container():
        
        df = get_latest_traffic(conn)
        features, processed_df = preprocess_traffic(df)
        model = train_model(features[:int(len(features)*0.8)])
        
        anomalies, scores = detect_anomalies(model, features)
        processed_df['anomaly'] = anomalies
        processed_df['confidence_score'] = scores
        
        profiles = risk_profiling(processed_df)
        check_for_alerts(profiles)  
        
        st.subheader("Network Graph")
        G = nx.from_pandas_edgelist(processed_df, 'src_ip', 'dst_ip', ['packet_size'])
        pos = nx.spring_layout(G)
        edge_x, edge_y = [], []  
        
        st.plotly_chart(fig)
        
        st.subheader("Anomaly Trends")
        st.line_chart(processed_df[['timestamp', 'confidence_score']])
        
        st.subheader("Anomaly Heatmap")
        fig, ax = plt.subplots()
        sns.heatmap(processed_df.pivot_table(index='src_ip', columns='dst_ip', values='confidence_score', aggfunc='mean'), ax=ax)
        st.pyplot(fig)
        
        st.subheader("Risk Profiles")
        st.dataframe(profiles)
    
    time.sleep(REFRESH_INTERVAL)
    st.rerun()  