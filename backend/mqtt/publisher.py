from pydantic import BaseModel
from mqtt.client import publish as mqtt_publish
import mqtt.event as mqtt_event
import json

COMMAND_CALL_TOPIC = "/user/folotoy/48ca439bbfdc/thing/command/call"

class UpdateTokenData(BaseModel):
    token: str

class UpdateConfigData(BaseModel):
    speechUdpServerHost: str
    speechUdpServerPort: int

class UpdateStartVoiceData(BaseModel):
    url: str
    keyCode: int
    etag: str

class AudioPlay(BaseModel):
    recordingId: int
    order: int
    url: str

msg_id = 0
def next_msg_id():
    global msg_id
    msg_id += 1
    return msg_id

def update_token(data: UpdateTokenData):
    _publish_command(mqtt_event.PublishedIdentifier.UPDATE_TOKEN.value, data=dict(data))

def update_config(data: UpdateConfigData):
    event = mqtt_event.PublishedEvent(msgId=next_msg_id(), identifier=mqtt_event.PublishedIdentifier.UPDATE_CONFIG.value, inputParams=dict(data))
    mqtt_publish(COMMAND_CALL_TOPIC, dict(event))

def update_start_voice(data: UpdateStartVoiceData):
    event = mqtt_event.PublishedEvent(msgId=next_msg_id(), identifier=mqtt_event.PublishedIdentifier.UPDATE_START_VOICE.value, inputParams=dict(data))
    mqtt_publish(COMMAND_CALL_TOPIC, json.dumps(event))

def audio_play(data: AudioPlay):
    event = mqtt_event.PublishedEvent(msgId=next_msg_id(), identifier=mqtt_event.PublishedIdentifier.AUDIO_PLAY.value, inputParams=dict(data))
    mqtt_publish(COMMAND_CALL_TOPIC, json.dumps(event))

def _publish_command(identifier: str, data: dict):
    event = mqtt_event.PublishedEvent(msgId=next_msg_id(), identifier=identifier, inputParams=dict(data))
    event_str = json.dumps(dict(event))
    mqtt_publish(COMMAND_CALL_TOPIC, event_str)
    print(f"Public topic: {COMMAND_CALL_TOPIC}, msg: {event_str}")


