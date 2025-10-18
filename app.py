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
start_capture_thread()  # Start real-time capture
start_simulation_thread()  # Optional: Start IoT sim

st.title("GuardELNS Dashboard")

placeholder = st.empty()
while True:
    with placeholder.container():
        
        df = get_latest_traffic(conn)
        
        # Check if we have enough data
        if len(df) < 10:
            st.warning("Waiting for data... Please wait a few seconds.")
            time.sleep(5)
            st.rerun()
            continue
            
        features, processed_df = preprocess_traffic(df)
        
        # Ensure we have enough data for training
        if len(features) < 10:
            st.warning("Not enough data for analysis yet...")
            time.sleep(5)
            st.rerun()
            continue
            
        train_size = max(int(len(features)*0.8), 5)
        model = train_model(features[:train_size])
        
        # Detect anomalies
        anomalies, scores = detect_anomalies(model, features)
        processed_df['anomaly'] = anomalies
        processed_df['confidence_score'] = scores
        
        # Risk profiling
        profiles = risk_profiling(processed_df)
        check_for_alerts(profiles)  # Trigger alerts
        
        # Network Graph
        st.subheader("Network Graph")
        G = nx.from_pandas_edgelist(processed_df, 'src_ip', 'dst_ip', ['packet_size'])
        pos = nx.spring_layout(G)
        
        # Create edge traces
        edge_x, edge_y = [], []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')
        
        # Create node traces
        node_x = []
        node_y = []
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
        
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                colorscale='YlGnBu',
                size=10,
                colorbar=dict(
                    thickness=15,
                    title=dict(text='Node Connections', side='right'),
                    xanchor='left'
                )
            )
        )
        
        # Color nodes by number of connections
        node_adjacencies = []
        node_text = []
        for node, adjacencies in enumerate(G.adjacency()):
            node_adjacencies.append(len(adjacencies[1]))
            node_text.append(f'{adjacencies[0]}<br># of connections: {len(adjacencies[1])}')
        
        node_trace.marker.color = node_adjacencies
        node_trace.text = node_text
        
        # Create figure
        fig = go.Figure(data=[edge_trace, node_trace],
                       layout=go.Layout(
                           showlegend=False,
                           hovermode='closest',
                           margin=dict(b=0, l=0, r=0, t=0),
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                       )
        st.plotly_chart(fig)
        
        # Anomaly Trends
        st.subheader("Anomaly Trends")
        st.line_chart(processed_df[['timestamp', 'confidence_score']])
        
        # Heatmap
        st.subheader("Anomaly Heatmap")
        fig, ax = plt.subplots()
        sns.heatmap(processed_df.pivot_table(index='src_ip', columns='dst_ip', values='confidence_score', aggfunc='mean'), ax=ax)
        st.pyplot(fig)
        
        st.subheader("Risk Profiles")
        st.dataframe(profiles)
    
    time.sleep(REFRESH_INTERVAL)
    st.rerun()  