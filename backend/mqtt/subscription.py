import paho.mqtt.client as mqtt
import mqtt.event as mqtt_event
import mqtt.publisher as mqtt_publisher
from utils.uuid_util import get_uuid4_no_hyphen
from core.role import get_role_by_code


def processTopic1(client, userdata, msg: mqtt.MQTTMessage):
    print(f"Received on {msg.topic}: {msg.payload.decode()}")

def processEventPost(client, userdata, msg: mqtt.MQTTMessage):
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
    elif mqtt_event.ReceivedIdentifier.PRESS_SMALL_BTN.value == event.identifier:
        role_code = event.outParams.get('keyCode')
        role_changed = event.outParams.get('changed') == 1
        if role_changed:
            role = get_role_by_code(role_code)
            data = mqtt_publisher.UpdateStartVoiceData(url= role.self_introduction_voice, keyCode=role_code, etag="")
            mqtt_publisher.update_start_voice(data=data)

def processCommandAck(client, userdata, msg: mqtt.MQTTMessage):
    print(f"Received on {msg.topic}: {msg.payload.decode()}")

def processDataPost(client, userdata, msg: mqtt.MQTTMessage):
    print(f"Received on {msg.topic}: {msg.payload.decode()}")


subscriptions={
    "test/topic1": processTopic1,
    "/user/folotoy/+/thing/event/post": processEventPost,
    "/user/folotoy/+/thing/command/callAck": processCommandAck,
    "/user/folotoy/+/thing/data/post": processDataPost,
}