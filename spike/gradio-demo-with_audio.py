from openai import OpenAI
import gradio as gr
import os
import streaming_asr_demo as asr
import tts_websocket_demo as tts
import database
from conversation_history_summarization import generate_new_summary

client = OpenAI(
    api_key=os.environ.get("ARK_API_KEY"),
    base_url="https://ark.cn-beijing.volces.com/api/v3",
)


def click_js():
    return """function audioRecord() {
    var xPathRes = document.evaluate ('//*[contains(@class, "record")]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null); 
    xPathRes.singleNodeValue.click();}"""


def action(btn):
    """Changes button text on click"""
    if btn == '按住说话': return '停止'
    else: return '按住说话'


with gr.Blocks() as demo1:
    introduction_msg = gr.Textbox(label="介绍", value="小朋友，我是你的幼儿园老师，有什么要问我的吗？可以按【按住说话】按钮开始说话")

    chatbot = gr.Chatbot(visible=True)
    input_audio_button = gr.Button("按住说话")
    input_msg = gr.Textbox(visible=True)
    input_audio = gr.Audio(
        label="输入音频",
        sources=["microphone"],
        type='filepath',
        waveform_options=gr.WaveformOptions(
            waveform_color="#01C6FF",
            waveform_progress_color="#0066B4",
            skip_length=2,
            show_controls=False,
        ),
        editable=False,
        interactive=True,
        elem_id='input_audio_elem',
        visible=False
    )

    input_audio_button.click(fn=action, inputs=input_audio_button, outputs=input_audio_button).\
        then(fn=lambda: None, js=click_js())

    output_audio = gr.Audio(autoplay=True, label="输出音频")

    def user(user_message, history):
        return "", history + [[user_message, None]]

    def bot(history):
        MAX_CONVERSATION_ROUND = 3
        initial_message = {
            "role": "system", 
            "content": "你是一名知识渊博，能回答小孩十万个为什么的虚拟幼儿园老师，有耐心，能够引导孩子进行思考学习，需要用简单通俗比喻的话和三岁小朋友互动。但是如果不知道的问题，不能胡说八道"
        }
        history_openai_format = []
        for human, assistant in history[-MAX_CONVERSATION_ROUND:]:
            history_openai_format.append({"role": "user", "content": human})
            if assistant != None:
                history_openai_format.append({"role": "assistant", "content": assistant})
        response = client.chat.completions.create(
            model = os.environ.get("MODEL_ENDPOINT_ID"),
            messages = [initial_message] + history_openai_format,
            temperature = 1.0,
            stream = True,
        )

        history[-1][1] = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                history[-1][1] += chunk.choices[0].delta.content
                yield history
        database.chat_history = history
        print(database.chat_history)

    def update_summary():
        summary = generate_new_summary(database.summary, database.chat_history[-1:])
        database.summary = summary


    input_msg.submit(user, inputs=[input_msg, chatbot], outputs=[input_msg, chatbot], queue=False).then(
        bot, inputs=chatbot, outputs=chatbot
    ).then(update_summary)


    def clear_audio(audio):
        return None
    
    async def speak(history):
        print('-------speak start1-------')
        print(history)
        print('-------speak start2-------')
        text = history[-1][1]
        return await tts.speak(text)

    # input_audio.stop_recording(fn=asr.recognize, inputs=input_audio, outputs=input_msg).then(
    #     user, inputs=[input_msg, chatbot], outputs=[input_msg, chatbot], queue=False
    # ).then(
    #     bot, inputs=chatbot, outputs=chatbot
    # ).then(
    #     speak, inputs=chatbot, outputs=output_audio
    # ).then(
    #     clear_audio, inputs=input_audio, outputs=input_audio
    # )

with gr.Blocks() as demo2:
    refresh_btm = gr.Button("刷新")
    
    chatbot2 = gr.Chatbot(value=database.chat_history, label="小朋友对话记录")

    summary_btm = gr.Button("查看对话总结")
    summary_msg = gr.Textbox(label="小朋友对话总结")


    refresh_btm.click(lambda: database.chat_history, outputs=chatbot2)

    def summary():
        return database.summary

    summary_btm.click(summary, outputs=summary_msg)



demo = gr.TabbedInterface([demo1, demo2], ["小朋友语音对话页面", "家长管理页面"])
demo.launch()
