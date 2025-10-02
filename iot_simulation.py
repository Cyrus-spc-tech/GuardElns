import paho.mqtt.client as mqtt
import time
import random
import threading
from config import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC

def simulate_iot():
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT)
    for _ in range(100):
        data = {"temp": random.normalvariate(25, 2)}
        client.publish(MMQTT_TOPIC, str(data))
        time.sleep(1)
    for _ in range(50):
        client.publish(MQTT_TOPIC, "flood")
        time.sleep(0.01)

def start_simulation_thread():
    thread = threading.Thread(target=simulate_iot, daemon=True)
    thread.start()