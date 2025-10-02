import sqlite3
import pandas as pd

def init_db(db_path):
    conn = sqlite3.connect(db_path)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS traffic (
            id INTEGER PRIMARY KEY,
            src_ip TEXT,
            dst_ip TEXT,
            src_port INTEGER,
            dst_port INTEGER,
            protocol TEXT,
            packet_size INTEGER,
            timestamp REAL,
            anomaly BOOLEAN,
            confidence_score REAL,
            risk_score REAL
        )
    ''')
    conn.commit()
    return conn

def insert_traffic(conn, df):
    df.to_sql('traffic', conn, if_exists='append', index=False)

def get_latest_traffic(conn, limit=1000):
    return pd.read_sql(f'SELECT * FROM traffic ORDER BY timestamp DESC LIMIT {limit}', conn)