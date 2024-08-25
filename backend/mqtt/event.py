from enum import Enum
from pydantic import BaseModel

class PublishedIdentifier(Enum):
    UPDATE_TOKEN = "updatetoken"
    UPDATE_CONFIG = "updateconfig"
    UPDATE_START_VOICE = "updatestartvoice"
    AUDIO_PLAY = "audioplay"
    AUDIO_PLAY_CMD = "audioplay_cmd"


class ReceivedIdentifier(Enum):
    LOGIN = "login"
    PRESS_SMALL_BTN = "press_small_btn"
    REAL_TIME_DATA = "real_time_data"
    DATA_CONFIG = "data_config"
    


class ReceivedEvent(BaseModel):
    msgId: int
    identifier: str
    outParams: dict


class PublishedEvent(BaseModel):
    msgId: int
    identifier: str
    inputParams: dict
