from openai import OpenAI
import gradio as gr
import os


client = OpenAI(
    api_key=os.environ.get("ARK_API_KEY"),
    base_url="https://ark.cn-beijing.volces.com/api/v3",
)


def predict(message, history):
    print(history)
    messages = [
        {"role": "system", "content": "你是一名知识渊博，能回答小孩十万个为什么的虚拟幼儿园老师，有耐心，能够引导孩子进行思考学习，需要用简单通俗比喻的话和三岁小朋友互动。但是如果不知道的问题，不能胡说八道"}
    ]
    MAX_CONVERSATION_ROUND = 2

    history_openai_format = []
    for human, assistant in history[-MAX_CONVERSATION_ROUND:]:
        history_openai_format.append({"role": "user", "content": human})
        history_openai_format.append({"role": "assistant", "content": assistant})

    messages.extend(history_openai_format)
    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model=os.environ.get("MODEL_ENDPOINT_ID"),
        messages=messages,
        temperature=1.0,
        stream=True,
    )

    partial_message = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            partial_message = partial_message + chunk.choices[0].delta.content
            yield partial_message


gr.ChatInterface(predict).launch()
