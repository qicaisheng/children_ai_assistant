

from enum import Enum

from pydantic import BaseModel
from app.core.llm_client import get_client, get_model
import app.config as config

stories = [
    {
        "name": "海上救援",
        "audio_ids": [],
        "season": 1,
        "episode": "1A"
    },
    {
        "name": "秋季庆典",
        "audio_ids": [],
        "season": 1,
        "episode": "1B"
    },
    {
        "name": "狗狗拯救海龟",
        "audio_ids": [],
        "season": 1,
        "episode": "2A"
    },
    {
        "name": "游上岸的小鲸鱼",
        "audio_ids": [],
        "season": 1,
        "episode": "2B"
    },
    {
        "name": "",
        "audio_ids": [],
        "season": 1,
        "episode": "1B"
    },
    {
        "name": "猫咪惹的祸",
        "audio_ids": [],
        "season": 1,
        "episode": "3A"
    },
    {
        "name": "火车危机",
        "audio_ids": [],
        "season": 1,
        "episode": "3B"
    },
    {
        "name": "狗狗跳舞机",
        "audio_ids": [],
        "season": 1,
        "episode": "4A"
    },
    {
        "name": "迷雾危机",
        "audio_ids": [],
        "season": 1,
        "episode": "4B"
    },
    {
        "name": "走失的小野雁",
        "audio_ids": ["走失的小野雁.mp3"],
        "season": 1,
        "episode": "5A"
    },
    {
        "name": "飞向高空",
        "audio_ids": ["飞向高空.mp3"],
        "season": 1,
        "episode": "5B"
    },
    {
        "name": "冰上救援",
        "audio_ids": [],
        "season": 1,
        "episode": "6A"
    },
    {
        "name": "雪怪之谜",
        "audio_ids": [],
        "season": 1,
        "episode": "6B"
    },
    {
        "name": "逃跑的小象",
        "audio_ids": [],
        "season": 1,
        "episode": "7A"
    },
    {
        "name": "鸡飞狗跳",
        "audio_ids": [],
        "season": 1,
        "episode": "7B"
    },
    {
        "name": "狗狗车队",
        "audio_ids": [],
        "season": 1,
        "episode": "8A"
    },
    {
        "name": "狗狗去救火",
        "audio_ids": [],
        "season": 1,
        "episode": "8B"
    },
    {
        "name": "差点泡汤的点心",
        "audio_ids": [],
        "season": 1,
        "episode": "9A"
    },
    {
        "name": "雪地救援任务",
        "audio_ids": [],
        "season": 1,
        "episode": "9B"
    },
    {
        "name": "鬼盗船惊魂记",
        "audio_ids": [],
        "season": 1,
        "episode": "10"
    },
    {
        "name": "圣诞狗狗",
        "audio_ids": [],
        "season": 1,
        "episode": "11"
    },
    {
        "name": "小砾来报道",
        "audio_ids": [],
        "season": 1,
        "episode": "12A"
    },
    {
        "name": "拯救海象",
        "audio_ids": [],
        "season": 1,
        "episode": "12B"
    },
    {
        "name": "兔兔麻烦",
        "audio_ids": [],
        "season": 1,
        "episode": "13A"
    },
    {
        "name": "狗狗去选美",
        "audio_ids": [],
        "season": 1,
        "episode": "13B"
    },
    {
        "name": "抢救冒险湾",
        "audio_ids": [],
        "season": 1,
        "episode": "14A"
    },
    {
        "name": "沉入海底的雕像",
        "audio_ids": [],
        "season": 1,
        "episode": "14B"
    },
    {
        "name": "牛仔大冒险",
        "audio_ids": [],
        "season": 1,
        "episode": "15A"
    },
    {
        "name": "亚力出任务",
        "audio_ids": [],
        "season": 1,
        "episode": "15B"
    },
    {
        "name": "亚力上学去",
        "audio_ids": [],
        "season": 1,
        "episode": "16A"
    },
    {
        "name": "大停电",
        "audio_ids": [],
        "season": 1,
        "episode": "16B"
    },
    {
        "name": "狗狗去游泳",
        "audio_ids": [],
        "season": 1,
        "episode": "17A"
    },
    {
        "name": "狗狗马戏团",
        "audio_ids": [],
        "season": 1,
        "episode": "17B"
    },
    {
        "name": "彩蛋寻宝",
        "audio_ids": [],
        "season": 1,
        "episode": "18"
    },
    {
        "name": "超狗危机",
        "audio_ids": [],
        "season": 1,
        "episode": "19A"
    },
    {
        "name": "莱德的机器狗",
        "audio_ids": [],
        "season": 1,
        "episode": "19B"
    },
    {
        "name": "猴子大闹冒险湾",
        "audio_ids": [],
        "season": 1,
        "episode": "20A"
    },
    {
        "name": "小小猫头鹰",
        "audio_ids": [],
        "season": 1,
        "episode": "20B"
    },
    {
        "name": "迷路的小蝙蝠",
        "audio_ids": [],
        "season": 1,
        "episode": "21A"
    },
    {
        "name": "狗狗看牙医",
        "audio_ids": [],
        "season": 1,
        "episode": "21B"
    },
    {
        "name": "露营去",
        "audio_ids": [],
        "season": 1,
        "episode": "22A"
    },
    {
        "name": "离家出走的小乌龟",
        "audio_ids": [],
        "season": 1,
        "episode": "22B"
    },
    {
        "name": "狗狗与豆茎",
        "audio_ids": [],
        "season": 1,
        "episode": "23A"
    },
    {
        "name": "天生一对宝",
        "audio_ids": [],
        "season": 1,
        "episode": "23B"
    },
    {
        "name": "灯塔比舞去",
        "audio_ids": [],
        "season": 1,
        "episode": "24A"
    },
    {
        "name": "莱德遇险",
        "audio_ids": [],
        "season": 1,
        "episode": "24B"
    },
    {
        "name": "狗狗赛车去",
        "audio_ids": [],
        "season": 1,
        "episode": "25A"
    },
    {
        "name": "蛋糕大赛",
        "audio_ids": [],
        "season": 1,
        "episode": "25B"
    },
    {
        "name": "寻找海盗的宝藏",
        "audio_ids": [],
        "season": 1,
        "episode": "26"
    },
]

current_story: str = None

class Story(BaseModel):
    name: str
    audio_ids: list[str]
    season: int
    episode: str

    def get_audio_urls(self) -> list[str]:
        urls = []
        for id in self.audio_ids:
            url = config.audio_base_url + id
            urls.append(url)
        return urls

def story_names() -> list[str]:
    names = []
    for story in stories:
        names.append(story["name"])
    return names

def get_story_by_name(name: str) -> Story:
    for story in stories:
        if name == story["name"]:
            return Story(**story)
    return None

def set_current_story(story: str):
    global current_story
    current_story = story

def get_current_story() -> str:
    return current_story

def clear_current_story():
    global current_story
    current_story = None
    


