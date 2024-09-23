import paho.mqtt.client as mqtt
import app.mqtt.event as mqtt_event
import app.mqtt.publisher as mqtt_publisher
import app.service.login_service as login_service
from app.core.role import get_role_by_code, set_current_role_code
from app.repository.user import get_user_repository
from app.system.db import yield_postgresql_session


def processTopic1(client, userdata, msg: mqtt.MQTTMessage):
    print(f"Received on {msg.topic}: {msg.payload.decode()}")


def processEventPost(client, userdata, msg: mqtt.MQTTMessage):
    print(f"Received on {msg.topic}: {msg.payload.decode()}")
    _device_sn = get_device_sn(msg.topic)

    next(yield_postgresql_session())

    _current_user = get_user_repository().get_by_device_sn(_device_sn)
    event: mqtt_event.ReceivedEvent
    try:
        event = mqtt_event.ReceivedEvent.model_validate_json(msg.payload.decode())
    except ValueError as e:
        print(f"Validation error: {e}")
        return
    if mqtt_event.ReceivedIdentifier.LOGIN.value == event.identifier:
        role_code = event.outParams.get('role')
        login_service.device_login(device_sn=_device_sn, role_code=role_code)
    elif mqtt_event.ReceivedIdentifier.PRESS_SMALL_BTN.value == event.identifier:
        role_code = event.outParams.get('keyCode')
        role_changed = event.outParams.get('changed') == 1
        if role_changed:
            set_current_role_code(role_code)
            role = get_role_by_code(role_code)
            data = mqtt_publisher.UpdateStartVoiceData(url=role.self_introduction_voice, keyCode=role_code, etag="")
            mqtt_publisher.update_start_voice(data=data)


def processCommandAck(client, userdata, msg: mqtt.MQTTMessage):
    print(f"Received on {msg.topic}: {msg.payload.decode()}")


def processDataPost(client, userdata, msg: mqtt.MQTTMessage):
    print(f"Received on {msg.topic}: {msg.payload.decode()}")


def get_device_sn(topic: str) -> str:
    try:
        return topic.split('/')[3]
    except IndexError:
        raise ValueError("Invalid topic format")


subscriptions = {
    "test/topic1": processTopic1,
    "/user/folotoy/+/thing/event/post": processEventPost,
    "/user/folotoy/+/thing/command/callAck": processCommandAck,
    "/user/folotoy/+/thing/data/post": processDataPost,
}
