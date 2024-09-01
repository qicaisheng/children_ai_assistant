import json

from pydantic import BaseModel
from core.story import Story, play
from core.user_intent import UserIntent, enable_maybe_play_story, disable_maybe_play_story, maybe_play_story
from core.llm_client import get_client, get_model
from core.conversation_message import Message, MessageType, get_current_role_messages


PLAY_STORY_KEYWORDS = ["听", "放", "故事", "绘本", "书", "讲"]
SYSTEM_PROMPT = "你能够判断用户的意图，如果判断用户是想听故事，就提取用户想听的故事名称，如果不确定就引导用户想听的故事名称，用户是一个三岁小朋友，可能存在表达不清晰的地方"

def route(input: str):
    if maybe_play_story == True:
        histroy_messages = get_current_role_messages()[-4:]
        return semantic_route(input, histroy_messages)

    if keywords_check_intent(input) == UserIntent.CONVERSATION:
        disable_maybe_play_story()
        return SemanticRouteResult(UserIntent.CONVERSATION)
    
    return semantic_route(input)

def keywords_check_intent(input: str):
    for keyword in PLAY_STORY_KEYWORDS:
        if keyword in input:
            return UserIntent.MAYBE_PLAY_STORY
    return UserIntent.CONVERSATION

play_function_call_parameters = {
    "name": "play",
    "description": "播放对应故事音频。只有当知道用户想听的故事时，才调用该方法。",
    "strict": True,
    "parameters": {
        "type": "object",
        "properties": {
            "story": {
                "type": "string",
                "enum": Story.list(),
                "description": "需要播放的故事名称",
            },
        },
        "required": ["story"],
        "additionalProperties": False,
    }
}
conversation_function_call_parameters = {
    "name": "conversation",
    "description": "进行对话。当用户的意图不是听故事时，就进行对话。",
    "strict": True,
    "parameters": {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False,
    }
}

tools = [
    {
        "type": "function",
        "function": play_function_call_parameters
    },
    {
        "type": "function",
        "function": conversation_function_call_parameters
    }
]

class SemanticRouteResult(BaseModel):
    user_intent: UserIntent
    arguments: dict = {}
    

def semantic_route(input: str, history: list[Message] = []):
    history_messages = []
    for message in history:
        if message.message_type == MessageType.USER_MESSAGE:
            history_messages.append({"role": "user", "content": message.content})
        if message.message_type == MessageType.ASSISTANT_MESSAGE:
            history_messages.append({"role": "assistant", "content": message.content})
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history_messages + [{"role": "user", "content": input}]
    completion = get_client().chat.completions.create(
        model=get_model(),
        messages=messages,
        tools=tools,
        tool_choice="required"
    )
    print(completion)
    if completion.choices[0].finish_reason == "tool_calls":
        disable_maybe_play_story()
        for tool_call in completion.choices[0].message.tool_calls:
            arguments = json.loads(tool_call.function.arguments)
            if tool_call.function.name == "play":
                story = arguments['story']
                print(f"play story: {story}")
                return SemanticRouteResult(user_intent=UserIntent.PLAY_STORY, arguments={"story": story}) 
            if tool_call.function.name == "conversation":
                print("-----------conversation-----------")
                return SemanticRouteResult(user_intent=UserIntent.CONVERSATION)
    if completion.choices[0].finish_reason == "stop":
        output_text = completion.choices[0].message.content
        print(f"may be play story, output_text: {output_text}")
        enable_maybe_play_story()
        return SemanticRouteResult(user_intent=UserIntent.MAYBE_PLAY_STORY, arguments={"output_text": output_text})
