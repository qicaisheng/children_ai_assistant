
from enum import Enum


maybe_play_story: bool = False

class UserIntent(Enum):
    MAYBE_PLAY_STORY = "MAYBE_PLAY_STORY",
    PLAY_STORY = "PLAY_STORY",
    CONVERSATION = "CONVERSATION",

def enable_maybe_play_story():
    global maybe_play_story
    maybe_play_story = True

def disable_maybe_play_story():
    global maybe_play_story
    maybe_play_story = False
