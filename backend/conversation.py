from openai import OpenAI, ChatCompletion
import os


client = OpenAI(
    api_key = os.environ.get("ARK_API_KEY"),
    base_url = "https://ark.cn-beijing.volces.com/api/v3",
)

conversation_history = []
MAX_CONVERSATION_ROUND = 2
MAX_CONVERSATION_HISTORY_SIZE = 2 * MAX_CONVERSATION_ROUND

def answer(user_input: str):   
    global conversation_history 
    conversation_history = conversation_history[-MAX_CONVERSATION_HISTORY_SIZE:]
    conversation_history.append({"role": "user", "content": user_input})
    messages = [
        {"role": "system", "content": "你是一名知识渊博，能回答小孩十万个为什么的虚拟幼儿园老师，有耐心，能够引导孩子进行思考学习，需要用简单通俗比喻的话和三岁小朋友互动。但是如果不知道的问题，不能胡说八道"}
    ]
    messages.extend(conversation_history)
    response = client.chat.completions.create(
        model = os.environ.get("MODEL_ENDPOINT_ID"),
        messages = messages,
        stream=True
    )
    
    assistant_output = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            assistant_output = assistant_output + chunk.choices[0].delta.content
            yield chunk.choices[0].delta.content

    conversation_history.append({"role": "assistant", "content": assistant_output})


