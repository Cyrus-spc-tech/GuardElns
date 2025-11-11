"""
IoT Traffic Simulator
Generates realistic IoT device traffic for testing
"""

import random
import time
import threading
from datetime import datetime
import json


class IoTDevice:
    """Simulates an IoT device"""
    
    DEVICE_TYPES = {
        'smart_thermostat': {'ports': [8883, 1883], 'interval': (5, 15), 'data_size': (50, 200)},
        'security_camera': {'ports': [554, 8080], 'interval': (1, 3), 'data_size': (500, 2000)},
        'smart_light': {'ports': [1883, 8883], 'interval': (10, 30), 'data_size': (20, 100)},
        'door_sensor': {'ports': [1883], 'interval': (30, 120), 'data_size': (10, 50)},
        'motion_detector': {'ports': [1883, 8883], 'interval': (5, 20), 'data_size': (30, 80)},
        'smart_plug': {'ports': [1883, 8883], 'interval': (15, 45), 'data_size': (40, 120)},
    }
    
    def __init__(self, device_id, device_type=None):
        self.device_id = device_id
        self.device_type = device_type or random.choice(list(self.DEVICE_TYPES.keys()))
        self.config = self.DEVICE_TYPES[self.device_type]
        self.ip_address = f"192.168.1.{100 + device_id}"
        self.is_active = True
        self.malicious = False
        
    def generate_traffic(self):
        """Generate traffic data for this device"""
        return {
            'device_id': self.device_id,
            'device_type': self.device_type,
            'src_ip': self.ip_address,
            'dst_ip': '192.168.1.1',  # Gateway
            'src_port': random.randint(49152, 65535),
            'dst_port': random.choice(self.config['ports']),
            'protocol': 'TCP' if random.random() > 0.3 else 'UDP',
            'length': random.randint(*self.config['data_size']),
            'timestamp': datetime.now(),
            'malicious': self.malicious
        }
    
    def set_malicious(self, is_malicious=True):
        """Mark device as compromised"""
        self.malicious = is_malicious


class IoTSimulator:
    """Simulates multiple IoT devices"""
    
    def __init__(self, num_devices=10, malicious_ratio=0.1):
        self.num_devices = num_devices
        self.malicious_ratio = malicious_ratio
        self.devices = []
        self.traffic_log = []
        self.is_running = False
        self.simulation_thread = None
        self._initialize_devices()
        
    def _initialize_devices(self):
        """Create IoT devices"""
        for i in range(self.num_devices):
            device = IoTDevice(i)
            # Mark some devices as malicious
            if random.random() < self.malicious_ratio:
                device.set_malicious(True)
            self.devices.append(device)
        
        print(f"Initialized {self.num_devices} IoT devices")
        malicious_count = sum(1 for d in self.devices if d.malicious)
        print(f"Malicious devices: {malicious_count}")
    
    def start_simulation(self):
        """Start traffic generation"""
        if self.is_running:
            print("Simulation already running")
            return
        
        self.is_running = True
        self.simulation_thread = threading.Thread(target=self._run_simulation)
        self.simulation_thread.daemon = True
        self.simulation_thread.start()
        print("IoT simulation started")
    
    def _run_simulation(self):
        """Main simulation loop"""
        while self.is_running:
            # Each device generates traffic based on its interval
            for device in self.devices:
                if random.random() < 0.3:  # 30% chance per cycle
                    traffic = device.generate_traffic()
                    
                    # Add anomalous behavior for malicious devices
                    if device.malicious:
                        traffic = self._add_malicious_behavior(traffic)
                    
                    self.traffic_log.append(traffic)
            
            time.sleep(0.5)  # Simulation tick
    
    def _add_malicious_behavior(self, traffic):
        """Modify traffic to simulate attacks"""
        attack_type = random.choice(['port_scan', 'data_exfiltration', 'ddos'])
        
        if attack_type == 'port_scan':
            traffic['dst_port'] = random.randint(1, 1024)
            traffic['length'] = random.randint(40, 80)
            
        elif attack_type == 'data_exfiltration':
            traffic['length'] = random.randint(5000, 15000)  # Large data transfer
            traffic['dst_ip'] = f"203.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
            
        elif attack_type == 'ddos':
            traffic['length'] = random.randint(20, 60)
            traffic['dst_ip'] = '192.168.1.50'  # Target server
        
        return traffic
    
    def stop_simulation(self):
        """Stop traffic generation"""
        self.is_running = False
        if self.simulation_thread:
            self.simulation_thread.join(timeout=2)
        print("IoT simulation stopped")
    
    def get_traffic_log(self, limit=None):
        """Get generated traffic"""
        if limit:
            return self.traffic_log[-limit:]
        return self.traffic_log.copy()
    
    def clear_log(self):
        """Clear traffic log"""
        self.traffic_log.clear()
    
    def get_device_info(self):
        """Get information about simulated devices"""
        return [{
            'device_id': d.device_id,
            'device_type': d.device_type,
            'ip_address': d.ip_address,
            'malicious': d.malicious
        } for d in self.devices]
    
    def compromise_device(self, device_id):
        """Compromise a specific device"""
        if 0 <= device_id < len(self.devices):
            self.devices[device_id].set_malicious(True)
            print(f"Device {device_id} compromised")
            return True
        return False
    
    def heal_device(self, device_id):
        """Remove compromise from device"""
        if 0 <= device_id < len(self.devices):
            self.devices[device_id].set_malicious(False)
            print(f"Device {device_id} healed")
            return True
        return False
