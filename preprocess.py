import pandas as pd
import numpy as np

def preprocess_traffic(df):
    df = df.dropna()
    
    df['protocol'] = df['protocol'].map({'TCP': 1, 'UDP': 2, 'Other': 0}).astype(float)
    
    df['time_delta'] = df['timestamp'].diff().fillna(0).astype(float)
    df['byte_ratio'] = df['packet_size'] / (df['time_delta'] + 1e-5)
    
    numerical_cols = ['src_port', 'dst_port', 'packet_size', 'time_delta', 'byte_ratio', 'protocol']
    df[numerical_cols] = df[numerical_cols].astype(float)  
    
    df[numerical_cols] = (df[numerical_cols] - df[numerical_cols].min()) / (df[numerical_cols].max() - df[numerical_cols].min() + 1e-5)
    
    features = df[numerical_cols].values
    return features, df

if __name__ == "__main__":
    import pandas as pd
    df = pd.DataFrame({
        'src_port': [1000, 2000],
        'dst_port': [80, 8080],
        'packet_size': [500, 600],
        'protocol': ['TCP', 'UDP'],
        'timestamp': [1.0, 2.0]
    })
    features, _ = preprocess_traffic(df)
    print("Features dtype:", features.dtype)  