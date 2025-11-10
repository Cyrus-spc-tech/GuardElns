"""
GuardELNS Demo Script
Demonstrates all features of the system
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from monitoring.traffic_capture import TrafficCapture
from detection.anomaly_detector import AnomalyDetector
from simulation.iot_simulator import IoTSimulator
from profiling.risk_engine import RiskEngine
from alerts.notification import AlertManager
from database.db_manager import DatabaseManager
import time
import pandas as pd


def print_header(title):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def demo_traffic_monitoring():
    """Demonstrate traffic monitoring"""
    print_header("1. TRAFFIC MONITORING DEMO")
    
    print("\n📡 Initializing traffic capture...")
    capture = TrafficCapture(interface="auto", packet_count=500)
    
    print("▶️  Starting packet capture (simulation mode)...")
    capture.start_capture()
    
    print("⏳ Capturing traffic for 8 seconds...")
    time.sleep(2)  # Give simulation time to start
    for i in range(6):
        time.sleep(1)
        stats = capture.get_stats()
        print(f"   Packets captured: {stats['total_packets']}")
    
    print("\n⏹️  Stopping capture...")
    capture.stop_capture()
    
    df = capture.get_packets_df()
    stats = capture.get_stats()
    
    print(f"\n✅ Capture complete!")
    print(f"   Total packets: {stats['total_packets']}")
    print(f"   TCP: {stats['tcp_packets']}")
    print(f"   UDP: {stats['udp_packets']}")
    print(f"   ICMP: {stats['icmp_packets']}")
    
    if not df.empty:
        print("\n📋 Sample packets:")
        print(df[['timestamp', 'src_ip', 'dst_ip', 'protocol', 'length']].head(5).to_string(index=False))
    else:
        print("\n⚠️  No packets captured yet (simulation starting up...)")
    
    return capture, df


def demo_anomaly_detection(df):
    """Demonstrate anomaly detection"""
    print_header("2. ANOMALY DETECTION DEMO")
    
    if df.empty or len(df) < 100:
        print(f"\n⚠️  Insufficient data for anomaly detection (need 100+ packets, have {len(df)})")
        print("   Skipping anomaly detection demo...")
        return None, None, None
    
    print("\n🤖 Initializing ML model (Isolation Forest)...")
    detector = AnomalyDetector(model_type='isolation_forest', contamination=0.1)
    
    print("🎓 Training model on captured traffic...")
    success = detector.train(df)
    
    if success:
        print("✅ Model trained successfully!")
        
        print("\n🔍 Detecting anomalies...")
        predictions = detector.predict(df)
        scores = detector.get_anomaly_scores(df)
        
        anomaly_count = predictions.sum()
        anomaly_rate = (anomaly_count / len(predictions)) * 100
        
        print(f"\n📊 Detection Results:")
        print(f"   Total samples analyzed: {len(predictions)}")
        print(f"   Anomalies detected: {anomaly_count}")
        print(f"   Anomaly rate: {anomaly_rate:.2f}%")
        
        if anomaly_count > 0:
            print("\n🚨 Anomalous packets:")
            anomaly_df = df[predictions == 1].copy()
            anomaly_df['score'] = scores[predictions == 1]
            print(anomaly_df[['src_ip', 'dst_ip', 'protocol', 'length', 'score']].head(5).to_string(index=False))
        
        return detector, predictions, scores
    else:
        print("❌ Model training failed!")
        return None, None, None


def demo_iot_simulation():
    """Demonstrate IoT simulation"""
    print_header("3. IoT SIMULATION DEMO")
    
    print("\n🏠 Initializing IoT environment...")
    simulator = IoTSimulator(num_devices=8, malicious_ratio=0.25)
    
    devices = simulator.get_device_info()
    print(f"\n📱 Created {len(devices)} IoT devices:")
    for device in devices:
        status = "🔴 COMPROMISED" if device['malicious'] else "🟢 NORMAL"
        print(f"   {device['device_id']}: {device['device_type']:20s} ({device['ip_address']}) - {status}")
    
    print("\n▶️  Starting IoT traffic simulation...")
    simulator.start_simulation()
    
    print("⏳ Generating traffic for 5 seconds...")
    time.sleep(5)
    
    print("\n⏹️  Stopping simulation...")
    simulator.stop_simulation()
    
    traffic = simulator.get_traffic_log()
    print(f"\n✅ Simulation complete!")
    print(f"   Total events generated: {len(traffic)}")
    
    # Show malicious traffic
    malicious_traffic = [t for t in traffic if t['malicious']]
    print(f"   Malicious events: {len(malicious_traffic)}")
    
    if malicious_traffic:
        print("\n🚨 Sample malicious traffic:")
        for event in malicious_traffic[:3]:
            print(f"   {event['device_type']:20s} -> {event['dst_ip']:15s} | Size: {event['length']:5d} bytes")
    
    return simulator


def demo_risk_profiling(df, predictions):
    """Demonstrate risk profiling"""
    print_header("4. RISK PROFILING DEMO")
    
    print("\n🎯 Initializing risk profiling engine...")
    engine = RiskEngine()
    
    print("📊 Analyzing network behavior...")
    engine.update_from_traffic(df, predictions)
    
    stats = engine.get_statistics()
    print(f"\n✅ Risk analysis complete!")
    print(f"   Total entities: {stats['total_entities']}")
    print(f"   High risk: {stats['high_risk']}")
    print(f"   Medium risk: {stats['medium_risk']}")
    print(f"   Low risk: {stats['low_risk']}")
    print(f"   Average risk score: {stats['avg_risk_score']:.2f}")
    
    high_risk = engine.get_high_risk_entities(threshold=50)
    if high_risk:
        print(f"\n⚠️  High-risk entities detected:")
        for entity in high_risk[:5]:
            print(f"   {entity['entity_id']:15s} | Risk: {entity['risk_score']:5.2f} | Level: {entity['risk_level']}")
    
    return engine


def demo_alert_system():
    """Demonstrate alert system"""
    print_header("5. ALERT SYSTEM DEMO")
    
    print("\n🔔 Initializing alert manager...")
    alert_manager = AlertManager(config={'enabled': True})
    
    print("\n📢 Creating sample alerts...")
    
    # Create various alerts
    alert_manager.create_alert(
        title="Suspicious Port Scan Detected",
        message="Device 192.168.1.105 scanned 50+ ports in 30 seconds",
        severity="HIGH",
        entity_id="192.168.1.105"
    )
    
    alert_manager.create_alert(
        title="Unusual Data Transfer",
        message="Large data transfer detected from IoT device",
        severity="MEDIUM",
        entity_id="192.168.1.120"
    )
    
    alert_manager.create_alert(
        title="New Device Connected",
        message="Unknown device joined the network",
        severity="LOW",
        entity_id="192.168.1.200"
    )
    
    alert_manager.create_alert(
        title="Potential Data Exfiltration",
        message="Critical: Sensitive data being sent to external IP",
        severity="CRITICAL",
        entity_id="192.168.1.50"
    )
    
    print("✅ Alerts created!")
    
    stats = alert_manager.get_statistics()
    print(f"\n📊 Alert Statistics:")
    print(f"   Total alerts: {stats['total_alerts']}")
    print(f"   Critical: {stats['by_severity']['CRITICAL']}")
    print(f"   High: {stats['by_severity']['HIGH']}")
    print(f"   Medium: {stats['by_severity']['MEDIUM']}")
    print(f"   Low: {stats['by_severity']['LOW']}")
    
    print("\n🚨 Recent alerts:")
    alerts = alert_manager.get_alerts(limit=5)
    for alert in alerts:
        severity_icon = {'LOW': '🟢', 'MEDIUM': '🟡', 'HIGH': '🟠', 'CRITICAL': '🔴'}
        icon = severity_icon.get(alert['severity'], '⚪')
        print(f"   {icon} [{alert['severity']:8s}] {alert['title']}")
    
    return alert_manager


def demo_database():
    """Demonstrate database operations"""
    print_header("6. DATABASE DEMO")
    
    print("\n💾 Initializing database...")
    db = DatabaseManager(db_path='data/database/demo_guardelns.db')
    
    print("✅ Database initialized!")
    
    # Log some events
    print("\n📝 Logging events...")
    db.log_system_event('INFO', 'demo', 'Demo started')
    db.log_system_event('INFO', 'demo', 'All modules initialized')
    
    # Get statistics
    stats = db.get_statistics()
    print(f"\n📊 Database Statistics:")
    print(f"   Traffic logs: {stats['total_traffic_logs']}")
    print(f"   Anomalies: {stats['total_anomalies']}")
    print(f"   Devices: {stats['total_devices']}")
    print(f"   Alerts: {stats['total_alerts']}")
    
    return db


def run_full_demo():
    """Run complete system demonstration"""
    print("\n" + "=" * 70)
    print("  🛡️  GuardELNS - Complete System Demonstration")
    print("=" * 70)
    print("\n  AI-Powered Enterprise-Level Network Security")
    print("  Chandigarh Engineering College Jhanjeri")
    print("\n" + "=" * 70)
    
    try:
        # Demo 1: Traffic Monitoring
        capture, df = demo_traffic_monitoring()
        
        # Demo 2: Anomaly Detection
        detector, predictions, scores = demo_anomaly_detection(df)
        
        # Demo 3: IoT Simulation
        simulator = demo_iot_simulation()
        
        # Demo 4: Risk Profiling
        if predictions is not None:
            engine = demo_risk_profiling(df, predictions)
        
        # Demo 5: Alert System
        alert_manager = demo_alert_system()
        
        # Demo 6: Database
        db = demo_database()
        
        # Summary
        print_header("DEMO COMPLETE")
        print("\n✅ All modules demonstrated successfully!")
        print("\n📊 System Capabilities:")
        print("   ✓ Real-time traffic monitoring")
        print("   ✓ ML-based anomaly detection")
        print("   ✓ IoT device simulation")
        print("   ✓ Risk profiling and scoring")
        print("   ✓ Intelligent alerting")
        print("   ✓ Database logging")
        
        print("\n🚀 Next Steps:")
        print("   1. Run the full dashboard: streamlit run app.py")
        print("   2. Run system tests: python tests/test_system.py")
        print("   3. Read the documentation: README.md")
        print("   4. Check quick start guide: QUICKSTART.md")
        
        print("\n" + "=" * 70)
        print("  Thank you for exploring GuardELNS!")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_full_demo()
