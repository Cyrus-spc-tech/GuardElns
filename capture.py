import pandas as pd
import time
import threading
from database import insert_traffic, init_db
from config import CAPTURE_COUNT, DB_PATH
import random

def generate_synthetic_traffic():
    # Create a new connection in this thread
    conn = init_db(DB_PATH)
    print("Synthetic traffic generator started...")
    while True:
        data = []
        for _ in range(CAPTURE_COUNT):
            data.append({
                'src_ip': f'192.168.1.{random.randint(1, 10)}',
                'dst_ip': f'192.168.1.{random.randint(1, 10)}',
                'src_port': random.randint(1000, 65535),
                'dst_port': random.randint(80, 8080),
                'protocol': random.choice(['TCP', 'UDP']),
                'packet_size': random.normalvariate(500, 100),
                'timestamp': time.time(),
                'anomaly': None,
                'confidence_score': None,
                'risk_score': None
            })
        df = pd.DataFrame(data)
        insert_traffic(conn, df)
        print(f"Inserted {len(df)} synthetic packets...")
        time.sleep(1)

def start_capture_thread():
    thread = threading.Thread(target=generate_synthetic_traffic, daemon=True)
    thread.start()