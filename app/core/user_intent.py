
from enum import Enum


_maybe_play_story: bool = False

class UserIntent(Enum):
    MAYBE_PLAY_STORY = "MAYBE_PLAY_STORY",
    PLAY_STORY = "PLAY_STORY",
    CONVERSATION = "CONVERSATION",
    RAG_QA_STORY = "RAG_QA_STORY",

def enable_maybe_play_story():
    global _maybe_play_story
    _maybe_play_story = True

def disable_maybe_play_story():
    global _maybe_play_story
    _maybe_play_story = False

def maybe_play_story() -> bool:
    return _maybe_play_story
