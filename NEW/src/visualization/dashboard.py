"""
Dashboard Visualization Components
Creates interactive charts and visualizations
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import networkx as nx
from datetime import datetime, timedelta


def create_protocol_pie_chart(stats):
    """Create pie chart for protocol distribution"""
    labels = ['TCP', 'UDP', 'ICMP', 'Other']
    values = [
        stats.get('tcp_packets', 0),
        stats.get('udp_packets', 0),
        stats.get('icmp_packets', 0),
        stats.get('other_packets', 0)
    ]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.3,
        marker=dict(colors=['#636EFA', '#EF553B', '#00CC96', '#AB63FA'])
    )])
    
    fig.update_layout(
        title="Protocol Distribution",
        height=400,
        showlegend=True
    )
    
    return fig


def create_traffic_timeline(df):
    """Create timeline chart of traffic volume"""
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df_grouped = df.groupby(pd.Grouper(key='timestamp', freq='1S')).size().reset_index(name='count')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_grouped['timestamp'],
        y=df_grouped['count'],
        mode='lines',
        fill='tozeroy',
        line=dict(color='#636EFA', width=2),
        name='Packets/sec'
    ))
    
    fig.update_layout(
        title="Traffic Volume Over Time",
        xaxis_title="Time",
        yaxis_title="Packets per Second",
        height=400,
        hovermode='x unified'
    )
    
    return fig


def create_anomaly_scatter(df, predictions, scores):
    """Create scatter plot showing anomalies"""
    if df.empty or len(predictions) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    df_plot = df.copy()
    df_plot['anomaly'] = predictions
    df_plot['score'] = scores
    df_plot['timestamp'] = pd.to_datetime(df_plot['timestamp'])
    
    # Separate normal and anomalous packets
    normal = df_plot[df_plot['anomaly'] == 0]
    anomalous = df_plot[df_plot['anomaly'] == 1]
    
    fig = go.Figure()
    
    # Normal packets
    fig.add_trace(go.Scatter(
        x=normal['timestamp'],
        y=normal['length'],
        mode='markers',
        name='Normal',
        marker=dict(color='#00CC96', size=6, opacity=0.6),
        hovertemplate='<b>Normal Traffic</b><br>Time: %{x}<br>Length: %{y}<br>Score: %{customdata:.3f}',
        customdata=normal['score']
    ))
    
    # Anomalous packets
    fig.add_trace(go.Scatter(
        x=anomalous['timestamp'],
        y=anomalous['length'],
        mode='markers',
        name='Anomaly',
        marker=dict(color='#EF553B', size=10, symbol='x'),
        hovertemplate='<b>Anomaly Detected!</b><br>Time: %{x}<br>Length: %{y}<br>Score: %{customdata:.3f}',
        customdata=anomalous['score']
    ))
    
    fig.update_layout(
        title="Anomaly Detection Results",
        xaxis_title="Time",
        yaxis_title="Packet Length",
        height=400,
        hovermode='closest'
    )
    
    return fig


def create_port_heatmap(df):
    """Create heatmap of port activity"""
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    # Get top ports
    top_src_ports = df['src_port'].value_counts().head(10)
    top_dst_ports = df['dst_port'].value_counts().head(10)
    
    # Create matrix
    ports = sorted(set(list(top_src_ports.index) + list(top_dst_ports.index)))
    matrix = []
    
    for src in ports:
        row = []
        for dst in ports:
            count = len(df[(df['src_port'] == src) & (df['dst_port'] == dst)])
            row.append(count)
        matrix.append(row)
    
    fig = go.Figure(data=go.Heatmap(
        z=matrix,
        x=[str(p) for p in ports],
        y=[str(p) for p in ports],
        colorscale='Viridis',
        hovertemplate='Src Port: %{y}<br>Dst Port: %{x}<br>Count: %{z}<extra></extra>'
    ))
    
    fig.update_layout(
        title="Port Communication Heatmap",
        xaxis_title="Destination Port",
        yaxis_title="Source Port",
        height=500
    )
    
    return fig


def create_network_graph(df, limit=50):
    """Create network topology graph"""
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    # Create network graph
    G = nx.Graph()
    
    # Add edges (limit to prevent overcrowding)
    df_sample = df.head(limit)
    for _, row in df_sample.iterrows():
        if pd.notna(row['src_ip']) and pd.notna(row['dst_ip']):
            G.add_edge(row['src_ip'], row['dst_ip'])
    
    # Get positions
    pos = nx.spring_layout(G, k=0.5, iterations=50)
    
    # Create edge trace
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines'
    )
    
    # Create node trace
    node_x = []
    node_y = []
    node_text = []
    node_size = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(f"{node}<br>Connections: {G.degree(node)}")
        node_size.append(10 + G.degree(node) * 2)
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=node_text,
        marker=dict(
            size=node_size,
            color='#636EFA',
            line=dict(width=2, color='white')
        )
    )
    
    # Create figure
    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        title="Network Topology",
        showlegend=False,
        hovermode='closest',
        height=600,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
    
    return fig


def create_risk_gauge(risk_score):
    """Create gauge chart for risk score"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=risk_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Network Risk Score"},
        delta={'reference': 50},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 30], 'color': "#00CC96"},
                {'range': [30, 70], 'color': "#FFA15A"},
                {'range': [70, 100], 'color': "#EF553B"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 80
            }
        }
    ))
    
    fig.update_layout(height=300)
    return fig
