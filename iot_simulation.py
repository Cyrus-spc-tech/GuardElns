import paho.mqtt.client as mqtt
import time
import random
import threading
from config import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC

def simulate_iot():
    try:
        client = mqtt.Client()
        client.connect(MQTT_BROKER, MQTT_PORT)
        for _ in range(100):
            data = {"temp": random.normalvariate(25, 2)}
            client.publish(MQTT_TOPIC, str(data))
            time.sleep(1)
        for _ in range(50):
            client.publish(MQTT_TOPIC, "flood")
            time.sleep(0.01)
    except Exception as e:
        print(f"IoT simulation failed (MQTT broker may not be running): {e}")

def start_simulation_thread():
    try:
        thread = threading.Thread(target=simulate_iot, daemon=True)
        thread.start()
    except Exception as e:
        print(f"Failed to start IoT simulation thread: {e}")