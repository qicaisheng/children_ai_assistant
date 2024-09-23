from pydantic import BaseModel
from app.mqtt.client import publish as mqtt_publish
import app.mqtt.event as mqtt_event
import json

COMMAND_CALL_TOPIC = "/user/folotoy/{device_sn}/thing/command/call"

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

def update_token(data: UpdateTokenData, device_sn: str):
    _publish_command(mqtt_event.PublishedIdentifier.UPDATE_TOKEN.value, data=dict(data), device_sn=device_sn)

def update_config(data: UpdateConfigData, device_sn: str):
    return _publish_command(mqtt_event.PublishedIdentifier.UPDATE_CONFIG.value, data=dict(data), device_sn=device_sn)

def update_start_voice(data: UpdateStartVoiceData, device_sn: str):
    _publish_command(mqtt_event.PublishedIdentifier.UPDATE_START_VOICE.value, data=dict(data), device_sn=device_sn)

def audio_play(data: AudioPlay, device_sn: str):
    _publish_command(mqtt_event.PublishedIdentifier.AUDIO_PLAY.value, data=dict(data), device_sn=device_sn)

def audio_play_cmd(data: AudioPlayCMD, device_sn: str):
    _publish_command(mqtt_event.PublishedIdentifier.AUDIO_PLAY_CMD.value, data=dict(data), device_sn=device_sn)

def _publish_command(identifier: str, data: dict, device_sn: str):
    topic = COMMAND_CALL_TOPIC.format(device_sn=device_sn)
    event = mqtt_event.PublishedEvent(msgId=next_msg_id(), identifier=identifier, inputParams=dict(data))
    event_str = json.dumps(dict(event))
    print(f"Public topic: {topic}, msg: {event_str}")
    return mqtt_publish(topic, event_str)


