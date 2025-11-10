"""
Database Manager
Handles data storage and logging
"""

import sqlite3
import pandas as pd
from datetime import datetime
import os
import json


class DatabaseManager:
    """Manages SQLite database for GuardELNS"""
    
    def __init__(self, db_path='data/database/guardelns.db'):
        self.db_path = db_path
        self._ensure_database()
        self._create_tables()
    
    def _ensure_database(self):
        """Ensure database directory exists"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def _create_tables(self):
        """Create database tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Traffic logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS traffic_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                src_ip TEXT,
                dst_ip TEXT,
                src_port INTEGER,
                dst_port INTEGER,
                protocol TEXT,
                length INTEGER,
                flags TEXT,
                is_anomaly BOOLEAN DEFAULT 0,
                anomaly_score REAL DEFAULT 0.0
            )
        ''')
        
        # Anomaly records table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS anomaly_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                entity_id TEXT,
                anomaly_type TEXT,
                severity TEXT,
                description TEXT,
                metadata TEXT
            )
        ''')
        
        # Device profiles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS device_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT UNIQUE,
                device_type TEXT,
                risk_score REAL,
                risk_level TEXT,
                anomaly_count INTEGER,
                total_events INTEGER,
                first_seen DATETIME,
                last_seen DATETIME,
                last_updated DATETIME
            )
        ''')
        
        # Alerts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                title TEXT,
                message TEXT,
                severity TEXT,
                entity_id TEXT,
                acknowledged BOOLEAN DEFAULT 0,
                metadata TEXT
            )
        ''')
        
        # System logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                log_level TEXT,
                module TEXT,
                message TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def log_traffic(self, df, predictions=None, scores=None):
        """Log network traffic to database"""
        if df.empty:
            return 0
        
        conn = sqlite3.connect(self.db_path)
        
        # Add anomaly information if available
        if predictions is not None:
            df['is_anomaly'] = predictions
        if scores is not None:
            df['anomaly_score'] = scores
        
        # Insert into database
        df.to_sql('traffic_logs', conn, if_exists='append', index=False)
        
        rows_inserted = len(df)
        conn.close()
        
        return rows_inserted
    
    def log_anomaly(self, entity_id, anomaly_type, severity, description, metadata=None):
        """Log an anomaly event"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO anomaly_records 
            (timestamp, entity_id, anomaly_type, severity, description, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now(),
            entity_id,
            anomaly_type,
            severity,
            description,
            json.dumps(metadata) if metadata else None
        ))
        
        conn.commit()
        conn.close()
    
    def update_device_profile(self, profile_dict):
        """Update or insert device profile"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO device_profiles
            (device_id, device_type, risk_score, risk_level, anomaly_count, 
             total_events, first_seen, last_seen, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            profile_dict['entity_id'],
            profile_dict.get('entity_type', 'device'),
            profile_dict['risk_score'],
            profile_dict['risk_level'],
            profile_dict['anomaly_count'],
            profile_dict['total_events'],
            profile_dict['first_seen'],
            profile_dict['last_seen'],
            datetime.now()
        ))
        
        conn.commit()
        conn.close()
    
    def log_alert(self, alert_dict):
        """Log an alert"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO alerts
            (timestamp, title, message, severity, entity_id, acknowledged, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            alert_dict['timestamp'],
            alert_dict['title'],
            alert_dict['message'],
            alert_dict['severity'],
            alert_dict.get('entity_id'),
            alert_dict.get('acknowledged', False),
            json.dumps(alert_dict.get('metadata', {}))
        ))
        
        conn.commit()
        conn.close()
    
    def log_system_event(self, level, module, message):
        """Log a system event"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO system_logs (timestamp, log_level, module, message)
            VALUES (?, ?, ?, ?)
        ''', (datetime.now(), level, module, message))
        
        conn.commit()
        conn.close()
    
    def get_traffic_logs(self, limit=1000, anomalies_only=False):
        """Retrieve traffic logs"""
        conn = sqlite3.connect(self.db_path)
        
        query = "SELECT * FROM traffic_logs"
        if anomalies_only:
            query += " WHERE is_anomaly = 1"
        query += f" ORDER BY timestamp DESC LIMIT {limit}"
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df
    
    def get_anomaly_records(self, limit=100, severity=None):
        """Retrieve anomaly records"""
        conn = sqlite3.connect(self.db_path)
        
        query = "SELECT * FROM anomaly_records"
        if severity:
            query += f" WHERE severity = '{severity}'"
        query += f" ORDER BY timestamp DESC LIMIT {limit}"
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df
    
    def get_device_profiles(self, risk_level=None):
        """Retrieve device profiles"""
        conn = sqlite3.connect(self.db_path)
        
        query = "SELECT * FROM device_profiles"
        if risk_level:
            query += f" WHERE risk_level = '{risk_level}'"
        query += " ORDER BY risk_score DESC"
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df
    
    def get_alerts(self, limit=100, unacknowledged_only=False):
        """Retrieve alerts"""
        conn = sqlite3.connect(self.db_path)
        
        query = "SELECT * FROM alerts"
        if unacknowledged_only:
            query += " WHERE acknowledged = 0"
        query += f" ORDER BY timestamp DESC LIMIT {limit}"
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df
    
    def get_statistics(self):
        """Get database statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Traffic logs count
        cursor.execute("SELECT COUNT(*) FROM traffic_logs")
        stats['total_traffic_logs'] = cursor.fetchone()[0]
        
        # Anomaly count
        cursor.execute("SELECT COUNT(*) FROM traffic_logs WHERE is_anomaly = 1")
        stats['total_anomalies'] = cursor.fetchone()[0]
        
        # Device count
        cursor.execute("SELECT COUNT(*) FROM device_profiles")
        stats['total_devices'] = cursor.fetchone()[0]
        
        # Alert count
        cursor.execute("SELECT COUNT(*) FROM alerts")
        stats['total_alerts'] = cursor.fetchone()[0]
        
        # Unacknowledged alerts
        cursor.execute("SELECT COUNT(*) FROM alerts WHERE acknowledged = 0")
        stats['unacknowledged_alerts'] = cursor.fetchone()[0]
        
        conn.close()
        
        return stats
    
    def clear_old_data(self, days=30):
        """Clear data older than specified days"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff_date = datetime.now() - pd.Timedelta(days=days)
        
        cursor.execute("DELETE FROM traffic_logs WHERE timestamp < ?", (cutoff_date,))
        cursor.execute("DELETE FROM anomaly_records WHERE timestamp < ?", (cutoff_date,))
        cursor.execute("DELETE FROM alerts WHERE timestamp < ?", (cutoff_date,))
        cursor.execute("DELETE FROM system_logs WHERE timestamp < ?", (cutoff_date,))
        
        conn.commit()
        rows_deleted = cursor.rowcount
        conn.close()
        
        return rows_deleted
    
    def export_to_csv(self, table_name, output_path):
        """Export table to CSV"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        conn.close()
        
        df.to_csv(output_path, index=False)
        return len(df)
    
    def backup_database(self, backup_path):
        """Create database backup"""
        import shutil
        shutil.copy2(self.db_path, backup_path)
        return os.path.exists(backup_path)
