import paho.mqtt.client as mqtt
import mqtt.event as mqtt_event
import mqtt.publisher as mqtt_publisher
from utils.uuid_util import get_uuid4_no_hyphen


def processTopic1(client, userdata, msg: mqtt.MQTTMessage):
    print(msg)
    print(f"Received on {msg.topic}: {msg.payload.decode()}")

def processEventPost(client, userdata, msg: mqtt.MQTTMessage):
    print(client)
    print(userdata)
    print(msg)
    print(f"Received on {msg.topic}: {msg.payload.decode()}")
    event: mqtt_event.ReceivedEvent
    try:
        event = mqtt_event.ReceivedEvent.model_validate_json(msg.payload.decode())
    except ValueError as e:
        print(f"Validation error: {e}")
        return
    if mqtt_event.ReceivedIdentifier.LOGIN.value == event.identifier:
        data = mqtt_publisher.UpdateTokenData(token=get_uuid4_no_hyphen())
        mqtt_publisher.update_token(data=data)

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