import paho.mqtt.client as mqtt


def processTopic1(client, userdata, msg: mqtt.MQTTMessage):
    print(msg)
    print(f"Received on {msg.topic}: {msg.payload.decode()}")

def processEventPost(client, userdata, msg: mqtt.MQTTMessage):
    print(msg)
    print(f"Received on {msg.topic}: {msg.payload.decode()}")

def processCommandAck(client, userdata, msg: mqtt.MQTTMessage):
    print(msg)
    print(f"Received on {msg.topic}: {msg.payload.decode()}")

def processDataPost(client, userdata, msg: mqtt.MQTTMessage):
    print(msg)
    print(f"Received on {msg.topic}: {msg.payload.decode()}")


subscriptions={
    "test/topic1": processTopic1,
    "/user/folotoy/+/thing/event/post": processEventPost,
    "/user/folotoy/+/thing/command/callAck": processCommandAck,
    "/user/folotoy/+/thing/data/post": processDataPost,
}