"""
Alert and Notification System
Sends proactive security alerts for anomalies and high-risk events
"""

import smtplib
import json
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from collections import deque


class AlertManager:
    """Manages security alerts and notifications"""
    
    SEVERITY_LEVELS = {
        'LOW': {'color': '#00CC96', 'priority': 1},
        'MEDIUM': {'color': '#FFA15A', 'priority': 2},
        'HIGH': {'color': '#EF553B', 'priority': 3},
        'CRITICAL': {'color': '#DC143C', 'priority': 4}
    }
    
    def __init__(self, config=None):
        self.config = config or {}
        self.alerts = deque(maxlen=1000)
        self.alert_count = {'LOW': 0, 'MEDIUM': 0, 'HIGH': 0, 'CRITICAL': 0}
        self.enabled = self.config.get('enabled', True)
        
    def create_alert(self, title, message, severity='MEDIUM', entity_id=None, metadata=None):
        """Create a new alert"""
        alert = {
            'id': len(self.alerts) + 1,
            'timestamp': datetime.now(),
            'title': title,
            'message': message,
            'severity': severity,
            'entity_id': entity_id,
            'metadata': metadata or {},
            'acknowledged': False
        }
        
        self.alerts.append(alert)
        self.alert_count[severity] += 1
        
        # Send notifications if enabled
        if self.enabled:
            self._send_notifications(alert)
        
        return alert
    
    def _send_notifications(self, alert):
        """Send alert through configured channels"""
        # Email notification
        if self.config.get('email_enabled'):
            self._send_email(alert)
        
        # Slack notification
        if self.config.get('slack_webhook'):
            self._send_slack(alert)
        
        # Discord notification
        if self.config.get('discord_webhook'):
            self._send_discord(alert)
    
    def _send_email(self, alert):
        """Send email notification"""
        try:
            smtp_server = self.config.get('smtp_server', 'smtp.gmail.com')
            smtp_port = self.config.get('smtp_port', 587)
            sender = self.config.get('sender_email')
            receiver = self.config.get('receiver_email')
            password = self.config.get('email_password')
            
            if not all([sender, receiver, password]):
                return False
            
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = receiver
            msg['Subject'] = f"[GuardELNS] {alert['severity']} Alert: {alert['title']}"
            
            body = f"""
            GuardELNS Security Alert
            
            Severity: {alert['severity']}
            Time: {alert['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}
            Title: {alert['title']}
            
            Message:
            {alert['message']}
            
            Entity ID: {alert.get('entity_id', 'N/A')}
            
            ---
            This is an automated alert from GuardELNS Network Security System.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"Email notification error: {e}")
            return False
    
    def _send_slack(self, alert):
        """Send Slack notification"""
        try:
            webhook_url = self.config.get('slack_webhook')
            if not webhook_url:
                return False
            
            color = self.SEVERITY_LEVELS[alert['severity']]['color']
            
            payload = {
                'attachments': [{
                    'color': color,
                    'title': f"{alert['severity']} Alert: {alert['title']}",
                    'text': alert['message'],
                    'fields': [
                        {'title': 'Time', 'value': alert['timestamp'].strftime('%Y-%m-%d %H:%M:%S'), 'short': True},
                        {'title': 'Entity', 'value': alert.get('entity_id', 'N/A'), 'short': True}
                    ],
                    'footer': 'GuardELNS Security System',
                    'ts': int(alert['timestamp'].timestamp())
                }]
            }
            
            response = requests.post(webhook_url, json=payload, timeout=5)
            return response.status_code == 200
            
        except Exception as e:
            print(f"Slack notification error: {e}")
            return False
    
    def _send_discord(self, alert):
        """Send Discord notification"""
        try:
            webhook_url = self.config.get('discord_webhook')
            if not webhook_url:
                return False
            
            color_map = {
                'LOW': 0x00CC96,
                'MEDIUM': 0xFFA15A,
                'HIGH': 0xEF553B,
                'CRITICAL': 0xDC143C
            }
            
            payload = {
                'embeds': [{
                    'title': f"🚨 {alert['severity']} Alert",
                    'description': f"**{alert['title']}**\n\n{alert['message']}",
                    'color': color_map.get(alert['severity'], 0xFFA15A),
                    'fields': [
                        {'name': 'Time', 'value': alert['timestamp'].strftime('%Y-%m-%d %H:%M:%S'), 'inline': True},
                        {'name': 'Entity', 'value': alert.get('entity_id', 'N/A'), 'inline': True}
                    ],
                    'footer': {'text': 'GuardELNS Security System'},
                    'timestamp': alert['timestamp'].isoformat()
                }]
            }
            
            response = requests.post(webhook_url, json=payload, timeout=5)
            return response.status_code == 204
            
        except Exception as e:
            print(f"Discord notification error: {e}")
            return False
    
    def get_alerts(self, severity=None, limit=None, unacknowledged_only=False):
        """Get alerts with optional filtering"""
        alerts_list = list(self.alerts)
        
        # Filter by severity
        if severity:
            alerts_list = [a for a in alerts_list if a['severity'] == severity]
        
        # Filter by acknowledgment status
        if unacknowledged_only:
            alerts_list = [a for a in alerts_list if not a['acknowledged']]
        
        # Sort by timestamp (newest first)
        alerts_list.sort(key=lambda x: x['timestamp'], reverse=True)
        
        # Limit results
        if limit:
            alerts_list = alerts_list[:limit]
        
        return alerts_list
    
    def acknowledge_alert(self, alert_id):
        """Mark alert as acknowledged"""
        for alert in self.alerts:
            if alert['id'] == alert_id:
                alert['acknowledged'] = True
                return True
        return False
    
    def get_statistics(self):
        """Get alert statistics"""
        total = sum(self.alert_count.values())
        unacknowledged = sum(1 for a in self.alerts if not a['acknowledged'])
        
        return {
            'total_alerts': total,
            'unacknowledged': unacknowledged,
            'by_severity': self.alert_count.copy(),
            'recent_count': len(self.alerts)
        }
    
    def clear_alerts(self):
        """Clear all alerts"""
        self.alerts.clear()
        self.alert_count = {'LOW': 0, 'MEDIUM': 0, 'HIGH': 0, 'CRITICAL': 0}
    
    def test_notifications(self):
        """Test notification channels"""
        test_alert = {
            'timestamp': datetime.now(),
            'title': 'Test Alert',
            'message': 'This is a test notification from GuardELNS',
            'severity': 'LOW',
            'entity_id': 'test_device'
        }
        
        results = {
            'email': False,
            'slack': False,
            'discord': False
        }
        
        if self.config.get('email_enabled'):
            results['email'] = self._send_email(test_alert)
        
        if self.config.get('slack_webhook'):
            results['slack'] = self._send_slack(test_alert)
        
        if self.config.get('discord_webhook'):
            results['discord'] = self._send_discord(test_alert)
        
        return results


class AlertRules:
    """Defines rules for triggering alerts"""
    
    @staticmethod
    def check_anomaly_threshold(anomaly_count, total_packets, threshold=0.1):
        """Check if anomaly rate exceeds threshold"""
        if total_packets == 0:
            return None
        
        rate = anomaly_count / total_packets
        
        if rate > threshold * 3:
            return 'CRITICAL'
        elif rate > threshold * 2:
            return 'HIGH'
        elif rate > threshold:
            return 'MEDIUM'
        return None
    
    @staticmethod
    def check_risk_score(risk_score):
        """Check risk score level"""
        if risk_score >= 90:
            return 'CRITICAL'
        elif risk_score >= 70:
            return 'HIGH'
        elif risk_score >= 50:
            return 'MEDIUM'
        elif risk_score >= 30:
            return 'LOW'
        return None
    
    @staticmethod
    def check_port_scan(df, time_window=60, port_threshold=20):
        """Detect potential port scanning"""
        if df.empty:
            return []
        
        # Group by source IP and count unique destination ports
        port_scans = []
        for src_ip in df['src_ip'].unique():
            src_df = df[df['src_ip'] == src_ip]
            unique_ports = src_df['dst_port'].nunique()
            
            if unique_ports > port_threshold:
                port_scans.append({
                    'entity_id': src_ip,
                    'unique_ports': unique_ports,
                    'severity': 'HIGH' if unique_ports > port_threshold * 2 else 'MEDIUM'
                })
        
        return port_scans
    
    @staticmethod
    def check_data_exfiltration(df, size_threshold=10000):
        """Detect potential data exfiltration"""
        if df.empty:
            return []
        
        large_transfers = df[df['length'] > size_threshold]
        
        exfiltration_alerts = []
        for _, row in large_transfers.iterrows():
            exfiltration_alerts.append({
                'entity_id': row['src_ip'],
                'dst_ip': row['dst_ip'],
                'size': row['length'],
                'severity': 'HIGH'
            })
        
        return exfiltration_alerts
