from openai import OpenAI
import gradio as gr
import os


client = OpenAI(
    api_key = os.environ.get("ARK_API_KEY"),
    base_url = "https://ark.cn-beijing.volces.com/api/v3",
)

def predict(message, history):
    history_openai_format = []
    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human })
        history_openai_format.append({"role": "assistant", "content":assistant})
    history_openai_format.append({"role": "user", "content": message})
  
    response = client.chat.completions.create(model=os.environ.get("MODEL_ENDPOINT_ID"),
    messages= history_openai_format,
    temperature=1.0,
    stream=True)

    partial_message = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
              partial_message = partial_message + chunk.choices[0].delta.content
              yield partial_message

gr.ChatInterface(predict).launch()