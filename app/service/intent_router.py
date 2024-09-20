import json

from pydantic import BaseModel

import app.core.story as core_story
from app.core.conversation_message import Message, MessageType, get_current_role_messages
from app.core.llm_client import get_client, get_model
from app.core.story import story_names, get_story_by_name
from app.core.user_intent import UserIntent, enable_maybe_play_story, disable_maybe_play_story, maybe_play_story
from app.service.message_service import get_message_service

PLAY_STORY_KEYWORDS = ["听", "放", "故事", "绘本", "书", "讲"]
SYSTEM_PROMPT = "你能够判断用户的意图，然后基于用户的意图调用不同的tools。如果判断用户是想听故事，并且也有对应的故事，就调用play tool；如果没有对应的故事，或者判断就是对话，就调用conversation tool；如果判断用户想听故事，但是没有说出对应的故事名称，引导用户回复想听的故事名称。"

RAG_QA_STORY_KEYWORDS = ["什么", "怎么", "如何", "哪", "？"]


class SemanticRouteResult(BaseModel):
    user_intent: UserIntent
    arguments: dict = {}


def route(input_text: str) -> SemanticRouteResult:
    message_service = get_message_service()
    if core_story.get_current_story():
        for keyword in RAG_QA_STORY_KEYWORDS:
            if keyword in input_text:
                return SemanticRouteResult(user_intent=UserIntent.RAG_QA_STORY)
    if maybe_play_story():
        history_messages = message_service.get_latest_current_user_and_role_messages(4)
        return semantic_route(input_text, history_messages)

    if keywords_check_intent(input_text) == UserIntent.CONVERSATION:
        disable_maybe_play_story()
        return SemanticRouteResult(user_intent=UserIntent.CONVERSATION)

    history_messages = message_service.get_latest_current_user_and_role_messages(4)
    return semantic_route(input_text, history_messages)


def keywords_check_intent(input_text: str):
    for keyword in PLAY_STORY_KEYWORDS:
        if keyword in input_text:
            return UserIntent.MAYBE_PLAY_STORY
    return UserIntent.CONVERSATION


play_function_call_parameters = {
    "name": "play",
    "description": "只有当知道用户想听的故事，并且故事名称在enum list中，才调用该方法。否则不调用",
    "strict": True,
    "parameters": {
        "type": "object",
        "properties": {
            "story": {
                "type": "string",
                "enum": story_names(),
                "description": "需要播放的故事名称，提取到的故事名称必须跟enum里面的故事名语义高度相近",
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


def semantic_route(input: str, history: list[Message] = []) -> SemanticRouteResult:
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
        return process_function_call(completion)
    if completion.choices[0].finish_reason == "stop":
        output_text = completion.choices[0].message.content
        if output_text:
            print(f"may be play story, output_text: {output_text}")
            enable_maybe_play_story()
            return SemanticRouteResult(user_intent=UserIntent.MAYBE_PLAY_STORY, arguments={"output_text": output_text})
        else:  # fix for openai function call issue which finish_reason is stop, and content none but with call tools
            return process_function_call(completion)
    return SemanticRouteResult(user_intent=UserIntent.CONVERSATION)


def process_function_call(completion) -> SemanticRouteResult:
    disable_maybe_play_story()
    for tool_call in completion.choices[0].message.tool_calls:
        arguments = json.loads(tool_call.function.arguments)
        if tool_call.function.name == "play":
            story = arguments['story']
            if story in story_names():
                print(f"play story: {story}")
                return SemanticRouteResult(user_intent=UserIntent.PLAY_STORY,
                                           arguments={"story": get_story_by_name(story)})
            else:
                return SemanticRouteResult(user_intent=UserIntent.CONVERSATION)
        if tool_call.function.name == "conversation":
            print("-----------conversation-----------")
            return SemanticRouteResult(user_intent=UserIntent.CONVERSATION)

# print(route("想听故事"))
# print(route("好听"))

# history_messages = [
#     Message(role_code=1, content="想听大灰狼故事", message_type=MessageType.USER_MESSAGE, audio_id=None),
#     Message(role_code=1, content="从前大灰狼肚子空空的，导出找好吃的，最后找到羊阿姨，羊阿姨做了很多好吃的，大灰狼舍不得吃羊阿姨，最后跟羊阿姨做了好朋友。这个故事好不好听啊", message_type=MessageType.ASSISTANT_MESSAGE, audio_id=None),
# ]

# print(semantic_route("好听", history_messages))
