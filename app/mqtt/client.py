import paho.mqtt.client as mqtt


client = mqtt.Client()

def publish(topic: str, message: str):
    return client.publish(topic, message)
