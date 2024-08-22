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
    event = mqtt_event.PublishedEvent(msgId=next_msg_id(), identifier=mqtt_event.PublishedIdentifier.UPDATE_TOKEN.value, inputParams=dict(data))
    mqtt_publish(COMMAND_CALL_TOPIC, json.dump(event))

def update_config(data: UpdateConfigData):
    event = mqtt_event.PublishedEvent(msgId=next_msg_id(), identifier=mqtt_event.PublishedIdentifier.UPDATE_CONFIG.value, inputParams=dict(data))
    mqtt_publish(COMMAND_CALL_TOPIC, json.dump(event))

def update_start_voice(data: UpdateStartVoiceData):
    event = mqtt_event.PublishedEvent(msgId=next_msg_id(), identifier=mqtt_event.PublishedIdentifier.UPDATE_START_VOICE.value, inputParams=dict(data))
    mqtt_publish(COMMAND_CALL_TOPIC, json.dump(event))

def audio_play(data: AudioPlay):
    event = mqtt_event.PublishedEvent(msgId=next_msg_id(), identifier=mqtt_event.PublishedIdentifier.AUDIO_PLAY.value, inputParams=dict(data))
    mqtt_publish(COMMAND_CALL_TOPIC, json.dump(event))


