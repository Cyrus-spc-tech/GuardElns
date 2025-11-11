"""
GuardELNS System Tests
Comprehensive testing for all modules
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.monitoring.traffic_capture import TrafficCapture
from src.detection.anomaly_detector import AnomalyDetector
from src.simulation.iot_simulator import IoTSimulator
from src.profiling.risk_engine import RiskEngine
from src.alerts.notification import AlertManager
from src.database.db_manager import DatabaseManager
import time


def test_traffic_capture():
    """Test traffic capture module"""
    print("\n=== Testing Traffic Capture ===")
    
    capture = TrafficCapture(interface="auto", packet_count=100)
    print("✓ TrafficCapture initialized")
    
    capture.start_capture()
    print("✓ Capture started")
    
    time.sleep(3)
    
    df = capture.get_packets_df()
    print(f"✓ Captured {len(df)} packets")
    
    stats = capture.get_stats()
    print(f"✓ Stats: {stats}")
    
    capture.stop_capture()
    print("✓ Capture stopped")
    
    return df


def test_anomaly_detection(df):
    """Test anomaly detection module"""
    print("\n=== Testing Anomaly Detection ===")
    
    detector = AnomalyDetector(model_type='isolation_forest', contamination=0.1)
    print("✓ AnomalyDetector initialized")
    
    if len(df) >= 100:
        success = detector.train(df)
        if success:
            print("✓ Model trained successfully")
            
            predictions = detector.predict(df)
            print(f"✓ Predictions: {len(predictions)} samples")
            print(f"  Anomalies detected: {predictions.sum()}")
            
            scores = detector.get_anomaly_scores(df)
            print(f"✓ Anomaly scores calculated")
            
            return predictions, scores
        else:
            print("✗ Model training failed")
    else:
        print(f"✗ Insufficient data: {len(df)} packets (need 100+)")
    
    return None, None


def test_iot_simulation():
    """Test IoT simulation module"""
    print("\n=== Testing IoT Simulation ===")
    
    simulator = IoTSimulator(num_devices=5, malicious_ratio=0.2)
    print("✓ IoTSimulator initialized")
    
    simulator.start_simulation()
    print("✓ Simulation started")
    
    time.sleep(3)
    
    traffic = simulator.get_traffic_log(limit=20)
    print(f"✓ Generated {len(traffic)} traffic events")
    
    devices = simulator.get_device_info()
    print(f"✓ Device info: {len(devices)} devices")
    for device in devices:
        status = "🔴 MALICIOUS" if device['malicious'] else "🟢 NORMAL"
        print(f"  {device['device_id']}: {device['device_type']} - {status}")
    
    simulator.stop_simulation()
    print("✓ Simulation stopped")
    
    return traffic


def test_risk_profiling(df, predictions):
    """Test risk profiling module"""
    print("\n=== Testing Risk Profiling ===")
    
    engine = RiskEngine()
    print("✓ RiskEngine initialized")
    
    engine.update_from_traffic(df, predictions)
    print("✓ Profiles updated from traffic")
    
    stats = engine.get_statistics()
    print(f"✓ Statistics: {stats}")
    
    high_risk = engine.get_high_risk_entities(threshold=50)
    print(f"✓ High-risk entities: {len(high_risk)}")
    
    if high_risk:
        print("  Top 3 high-risk entities:")
        for entity in high_risk[:3]:
            print(f"    {entity['entity_id']}: Risk Score = {entity['risk_score']}")
    
    return engine


def test_alert_system():
    """Test alert and notification system"""
    print("\n=== Testing Alert System ===")
    
    alert_manager = AlertManager(config={'enabled': True})
    print("✓ AlertManager initialized")
    
    # Create test alerts
    alert_manager.create_alert(
        title="Test Alert - Low Severity",
        message="This is a low severity test alert",
        severity="LOW"
    )
    
    alert_manager.create_alert(
        title="Test Alert - High Severity",
        message="This is a high severity test alert",
        severity="HIGH",
        entity_id="192.168.1.100"
    )
    
    print("✓ Test alerts created")
    
    alerts = alert_manager.get_alerts(limit=10)
    print(f"✓ Retrieved {len(alerts)} alerts")
    
    stats = alert_manager.get_statistics()
    print(f"✓ Alert statistics: {stats}")
    
    return alert_manager


def test_database():
    """Test database module"""
    print("\n=== Testing Database ===")
    
    db = DatabaseManager(db_path='data/database/test_guardelns.db')
    print("✓ DatabaseManager initialized")
    
    # Log system event
    db.log_system_event('INFO', 'test_system', 'Test system event')
    print("✓ System event logged")
    
    # Get statistics
    stats = db.get_statistics()
    print(f"✓ Database statistics: {stats}")
    
    return db


def run_all_tests():
    """Run all system tests"""
    print("=" * 60)
    print("GuardELNS System Tests")
    print("=" * 60)
    
    try:
        # Test 1: Traffic Capture
        df = test_traffic_capture()
        
        # Test 2: Anomaly Detection
        predictions, scores = test_anomaly_detection(df)
        
        # Test 3: IoT Simulation
        iot_traffic = test_iot_simulation()
        
        # Test 4: Risk Profiling
        if predictions is not None:
            engine = test_risk_profiling(df, predictions)
        
        # Test 5: Alert System
        alert_manager = test_alert_system()
        
        # Test 6: Database
        db = test_database()
        
        print("\n" + "=" * 60)
        print("✓ All tests completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
