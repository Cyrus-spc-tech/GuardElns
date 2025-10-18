import pandas as pd
import numpy as np

def preprocess_traffic(df):
    # Only drop rows with missing essential values (not anomaly/confidence/risk which are filled later)
    essential_cols = ['src_ip', 'dst_ip', 'src_port', 'dst_port', 'protocol', 'packet_size', 'timestamp']
    df = df.dropna(subset=essential_cols)
    
    # Map protocol to integers and ensure numeric conversion
    df['protocol'] = df['protocol'].map({'TCP': 1, 'UDP': 2, 'Other': 0}).fillna(0).astype(float)
    
    # Calculate derived features
    df['time_delta'] = df['timestamp'].diff().fillna(0).astype(float)
    df['byte_ratio'] = df['packet_size'] / (df['time_delta'] + 1e-5)
    
    # Select numerical columns for normalization
    numerical_cols = ['src_port', 'dst_port', 'packet_size', 'time_delta', 'byte_ratio', 'protocol']
    df[numerical_cols] = df[numerical_cols].astype(float)  # Explicitly convert to float
    
    # Normalize the data
    df[numerical_cols] = (df[numerical_cols] - df[numerical_cols].min()) / (df[numerical_cols].max() - df[numerical_cols].min() + 1e-5)
    
    # Extract features as a numeric NumPy array
    features = df[numerical_cols].values
    return features, df

# Optional: Add debug print to verify dtype
if __name__ == "__main__":
    # Example usage for testing
    import pandas as pd
    df = pd.DataFrame({
        'src_port': [1000, 2000],
        'dst_port': [80, 8080],
        'packet_size': [500, 600],
        'protocol': ['TCP', 'UDP'],
        'timestamp': [1.0, 2.0]
    })
    features, _ = preprocess_traffic(df)
    print("Features dtype:", features.dtype)  # Should print a numeric type like float64