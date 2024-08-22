import paho.mqtt.client as mqtt


def processTopic1(client, userdata, msg: mqtt.MQTTMessage):
    print(msg)
    print(f"Received on {msg.topic}: {msg.payload.decode()}")


subscriptions={
    "test/topic1": processTopic1,
}