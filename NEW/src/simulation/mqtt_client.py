"""
MQTT Client for IoT Communication
Simulates MQTT-based IoT device communication
"""

import json
import time
import random
from datetime import datetime
import threading

try:
    import paho.mqtt.client as mqtt
    MQTT_AVAILABLE = True
except ImportError:
    MQTT_AVAILABLE = False
    print("Warning: paho-mqtt not available. MQTT features disabled.")


class MQTTSimulator:
    """Simulates MQTT broker and client communication"""
    
    def __init__(self, broker="localhost", port=1883, client_id=None):
        self.broker = broker
        self.port = port
        self.client_id = client_id or f"guardelns_{random.randint(1000, 9999)}"
        self.client = None
        self.is_connected = False
        self.messages = []
        self.topics = [
            "home/temperature",
            "home/humidity",
            "security/camera",
            "security/door",
            "lights/living_room",
            "appliances/thermostat"
        ]
        
        if MQTT_AVAILABLE:
            self._initialize_client()
    
    def _initialize_client(self):
        """Initialize MQTT client"""
        self.client = mqtt.Client(self.client_id)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect
    
    def _on_connect(self, client, userdata, flags, rc):
        """Callback for connection"""
        if rc == 0:
            self.is_connected = True
            print(f"Connected to MQTT broker at {self.broker}:{self.port}")
            # Subscribe to all topics
            for topic in self.topics:
                client.subscribe(topic)
        else:
            print(f"Connection failed with code {rc}")
    
    def _on_message(self, client, userdata, msg):
        """Callback for received messages"""
        message_data = {
            'topic': msg.topic,
            'payload': msg.payload.decode(),
            'timestamp': datetime.now(),
            'qos': msg.qos
        }
        self.messages.append(message_data)
    
    def _on_disconnect(self, client, userdata, rc):
        """Callback for disconnection"""
        self.is_connected = False
        print("Disconnected from MQTT broker")
    
    def connect(self):
        """Connect to MQTT broker"""
        if not MQTT_AVAILABLE:
            print("MQTT not available - using simulation mode")
            self.is_connected = True
            return True
        
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
            time.sleep(1)  # Wait for connection
            return self.is_connected
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from MQTT broker"""
        if MQTT_AVAILABLE and self.client:
            self.client.loop_stop()
            self.client.disconnect()
        self.is_connected = False
    
    def publish(self, topic, payload, qos=0):
        """Publish message to topic"""
        if not self.is_connected:
            return False
        
        if MQTT_AVAILABLE and self.client:
            try:
                result = self.client.publish(topic, payload, qos)
                return result.rc == mqtt.MQTT_ERR_SUCCESS
            except Exception as e:
                print(f"Publish error: {e}")
                return False
        else:
            # Simulation mode
            self.messages.append({
                'topic': topic,
                'payload': payload,
                'timestamp': datetime.now(),
                'qos': qos
            })
            return True
    
    def generate_sensor_data(self, device_type):
        """Generate realistic sensor data"""
        data = {
            'timestamp': datetime.now().isoformat(),
            'device_id': f"{device_type}_{random.randint(1, 100)}"
        }
        
        if device_type == 'temperature':
            data['value'] = round(random.uniform(18.0, 28.0), 2)
            data['unit'] = 'celsius'
            
        elif device_type == 'humidity':
            data['value'] = round(random.uniform(30.0, 70.0), 2)
            data['unit'] = 'percent'
            
        elif device_type == 'camera':
            data['status'] = random.choice(['active', 'idle'])
            data['motion_detected'] = random.choice([True, False])
            
        elif device_type == 'door':
            data['status'] = random.choice(['open', 'closed'])
            data['locked'] = random.choice([True, False])
            
        elif device_type == 'light':
            data['status'] = random.choice(['on', 'off'])
            data['brightness'] = random.randint(0, 100)
            
        return json.dumps(data)
    
    def simulate_traffic(self, duration=60, interval=2):
        """Simulate MQTT traffic for testing"""
        print(f"Simulating MQTT traffic for {duration} seconds...")
        start_time = time.time()
        
        while time.time() - start_time < duration:
            # Publish to random topics
            topic = random.choice(self.topics)
            device_type = topic.split('/')[-1]
            payload = self.generate_sensor_data(device_type)
            
            self.publish(topic, payload)
            time.sleep(interval)
        
        print("MQTT simulation completed")
    
    def get_messages(self, limit=None):
        """Get received messages"""
        if limit:
            return self.messages[-limit:]
        return self.messages.copy()
    
    def clear_messages(self):
        """Clear message buffer"""
        self.messages.clear()
    
    def get_stats(self):
        """Get MQTT statistics"""
        return {
            'connected': self.is_connected,
            'total_messages': len(self.messages),
            'topics': len(self.topics),
            'broker': f"{self.broker}:{self.port}"
        }
