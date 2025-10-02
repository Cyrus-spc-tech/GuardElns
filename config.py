# Configuration settings
DB_PATH = 'data/traffic.db'
CAPTURE_COUNT = 100  # Packets per capture loop
REFRESH_INTERVAL = 10  # Dashboard refresh in seconds
ANOMALY_THRESHOLD = 0.01  # Adjust based on model
EMAIL_TO = 'tanishgupta12389@gmail.com'  # For alerts
MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_TOPIC = 'iot/sensor'