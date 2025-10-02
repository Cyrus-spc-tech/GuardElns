import pandas as pd

def risk_profiling(df):
    profiles = df.groupby('src_ip').agg({
        'confidence_score': 'mean',
        'packet_size': 'sum',
        'anomaly': 'sum'
    }).reset_index()
    profiles['risk_score'] = profiles['confidence_score'] * 100
    profiles['risk_level'] = pd.cut(profiles['risk_score'], bins=[0, 30, 70, 100], labels=['Low', 'Medium', 'High'])
    return profiles