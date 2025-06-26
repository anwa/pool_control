import paho.mqtt.client as mqtt
import json
from utils.logger import logger
from utils.config import config


class MQTTClient:
    def __init__(self, broker, port, user, password, client_id="poolcontrol"):
        self.client = mqtt.Client(client_id)
        self.client.username_pw_set(user, password)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.broker = broker
        self.port = port

    def connect(self):
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        logger.info("Connected to MQTT Broker")
        # Subscribe to topics if needed

    def on_message(self, client, userdata, msg):
        logger.info(f"MQTT Message: {msg.topic} {msg.payload}")

    def publish(self, topic, payload, retain=False):
        self.client.publish(topic, json.dumps(payload), retain=retain)

    def send_autodiscovery(
        self, sensor_name, unique_id, unit, device_class, state_topic
    ):
        topic = f"homeassistant/sensor/{unique_id}/config"
        payload = {
            "name": sensor_name,
            "state_topic": state_topic,
            "unit_of_measurement": unit,
            "device_class": device_class,
            "unique_id": unique_id,
            "availability_topic": "poolcontrol/status",
        }
        self.publish(topic, payload, retain=True)
