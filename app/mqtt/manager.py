import paho.mqtt.client as mqtt
from app.mqtt.subscription import subscriptions
from app.mqtt.client import client as mqtt_client
import app.config as config

class MQTTManager:
    def __init__(self, broker_host: str, broker_port: int, subscriptions: dict):
        self.client = mqtt_client
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.subscriptions = subscriptions

        self.client.on_connect = self.on_connect

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully to MQTT broker")
            for topic, callback in self.subscriptions.items():
                client.subscribe(topic)
                client.message_callback_add(topic, callback)
        else:
            print(f"Failed to connect, return code {rc}")

    def connect(self):
        self.client.connect(self.broker_host, self.broker_port, 60)
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def add_subscription(self, topic: str, callback):
        self.subscriptions[topic] = callback
        self.client.subscribe(topic)
        self.client.message_callback_add(topic, callback)
        

mqtt_manager = MQTTManager(
    broker_host=config.mqtt_host,
    broker_port=config.mqtt_port,
    subscriptions=subscriptions
)
