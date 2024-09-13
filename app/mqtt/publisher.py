from pydantic import BaseModel
from app.mqtt.client import publish as mqtt_publish
import app.mqtt.event as mqtt_event
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

class AudioPlayCMD(BaseModel):
    recordingId: int
    total: int

msg_id = 0
def next_msg_id():
    global msg_id
    msg_id += 1
    return msg_id

def update_token(data: UpdateTokenData):
    _publish_command(mqtt_event.PublishedIdentifier.UPDATE_TOKEN.value, data=dict(data))

def update_config(data: UpdateConfigData):
    return _publish_command(mqtt_event.PublishedIdentifier.UPDATE_CONFIG.value, data=dict(data))

def update_start_voice(data: UpdateStartVoiceData):
    _publish_command(mqtt_event.PublishedIdentifier.UPDATE_START_VOICE.value, data=dict(data))

def audio_play(data: AudioPlay):
    _publish_command(mqtt_event.PublishedIdentifier.AUDIO_PLAY.value, data=dict(data))

def audio_play_cmd(data: AudioPlayCMD):
    _publish_command(mqtt_event.PublishedIdentifier.AUDIO_PLAY_CMD.value, data=dict(data))

def _publish_command(identifier: str, data: dict):
    event = mqtt_event.PublishedEvent(msgId=next_msg_id(), identifier=identifier, inputParams=dict(data))
    event_str = json.dumps(dict(event))
    print(f"Public topic: {COMMAND_CALL_TOPIC}, msg: {event_str}")
    return mqtt_publish(COMMAND_CALL_TOPIC, event_str)


