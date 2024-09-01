

from enum import Enum
import json
from core.llm_client import get_client, get_model

SYSTEM_PROMPT = "你能够判断用户的意图，如果判断用户是想听故事，就提取用户想听的故事名称，如果不确定就引导用户想听的故事名称，用户是一个三岁小朋友，可能存在表达不清晰的地方"


class Story(Enum):
    DAYOULUN = "挽救大游轮"
    XIAOYEYAN = "走失的小野雁"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


def play(story: str):
    print(f"play story: {story}")

function_call_parameters = {
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

tools = [
    {
        "type": "function",
        "function": function_call_parameters
    }
]

def llm_response(input: str):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}, 
        {"role": "user", "content": input}
    ]
    completion = get_client().chat.completions.create(
        model=get_model(),
        messages=messages,
        tools=tools,
        tool_choice="required"
    )
    print(completion)
    if completion.choices[0].finish_reason == "tool_calls":
        for tool_call in completion.choices[0].message.tool_calls:
            arguments = json.loads(tool_call.function.arguments)
            if tool_call.function.name == "play":
                story = arguments['story']
                print(f"play story: {story}")
                play(story)
    if completion.choices[0].finish_reason == "stop":
        output_text = completion.choices[0].message.content
        print(f"output_text: {output_text}")
        return output_text



"""
user: 我想听小野雁
ChatCompletion(id='202408311757183ad0f993db084e24', choices=[Choice(finish_reason='tool_calls', index=0, logprobs=None, message=ChatCompletionMessage(content='', role='assistant', function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_202408311757183ad0f993db084e24', function=Function(arguments='{"story": "走失的小野雁"}', name='play'), type='function', index=0)]))], created=1725098238, model='GLM-4-AirX', object=None, service_tier=None, system_fingerprint=None, usage=CompletionUsage(completion_tokens=13, prompt_tokens=177, total_tokens=190), request_id='202408311757183ad0f993db084e24')
user: 我想听故事
ChatCompletion(id='20240831175855e380717db6414bd9', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='好的，您想听哪个故事呢？请告诉我故事名称。', role='assistant', function_call=None, tool_calls=None))], created=1725098336, model='GLM-4-AirX', object=None, service_tier=None, system_fingerprint=None, usage=CompletionUsage(completion_tokens=16, prompt_tokens=175, total_tokens=191), request_id='20240831175855e380717db6414bd9')
"""

print(llm_response("我听到一个有趣的事情"))
