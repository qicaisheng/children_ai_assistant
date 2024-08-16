from openai import OpenAI
import gradio as gr
import os
from user import User
import streaming_asr_demo as asr
import tts_websocket_demo as tts
import database
from conversation_history_summarization import generate_new_summary
from system_template import get_system_prompt
import gradio_parents_tab
import gradio_admin_tab
import llm_client


def click_js():
    return """function audioRecord() {
    var xPathRes = document.evaluate ('//*[contains(@class, "record")]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null); 
    xPathRes.singleNodeValue.click();}"""


def action(btn):
    """Changes button text on click"""
    if btn == '按住说话': return '停止'
    else: return '按住说话'


STAGE_INIT = "INIT"
STAGE_SETTING_ROLE = "STAGE_SETTING_ROLE"
STAGE_CONVERSATION = "STAGE_CONVERSATION"
stage = STAGE_INIT
ROLE_INIT = "幼儿园老师"
role = ROLE_INIT


first_audio_path = None

def is_conversation_stage():
    return stage==STAGE_CONVERSATION

def is_not_init_stage():
    return stage!=STAGE_INIT


with gr.Blocks() as childrend_page:
    gr.Markdown("#### 用户身份")
    with gr.Accordion("设置用户身份", open=False) as user_config:
        user_name = gr.Textbox(label="姓名", value="")
        user_nickname = gr.Textbox(label="小名", value="")
        user_gender=gr.Radio(label="性别", choices=["男", "女"])
        user_age = gr.Number(label="年龄", value=3, interactive=True)
        user_description = gr.Textbox(label="描述", value="")
        user_save_btn = gr.Button("保存")

        def save_user(user_name, user_nickname, user_gender, user_age, user_description):
            database.user = User(name=user_name, nickname=user_nickname, gender=user_gender, age=user_age, description=user_description)
            print(database.user)
        user_save_btn.click(fn=save_user, inputs=[user_name, user_nickname, user_gender, user_age, user_description]).\
            then(lambda: gr.update(open=False), outputs=user_config)

    refresh_roles_btn = gr.Button("刷新角色")
    roles_dropdown = gr.Dropdown(
        choices=database.get_saved_roles(), label="选择角色", info="选择对应的角色就可以跟TA开始对话了", interactive=True,
        value=ROLE_INIT
    )

    introduction_msg = gr.Textbox(label="介绍", value=database.get_introduction(role=role))
    
    with gr.Row():
        with gr.Column():
            chatbot = gr.Chatbot(label="对话框", value=database.get_history(role=role))
        with gr.Column():
            input_msg = gr.Textbox(label="文本输入框")
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
                elem_id='input_audio_elem'
            )
            output_audio = gr.Audio(autoplay=True, label="输出音频")
            first_audio_play_btn = gr.Button("Play", visible=False)


    input_audio_button = gr.Button("按住说话")

    def refresh_roles_ropdown():
        return gr.Dropdown(choices=database.get_saved_roles(), interactive=True)
    
    refresh_roles_btn.click(refresh_roles_ropdown, outputs=roles_dropdown)
        # then(lambda: gr.update(visible=True), outputs=roles_dropdown)

    def change_role(dropdown):
        global role
        role = dropdown
        print("当前选择角色：" + role)

    roles_dropdown.change(change_role, inputs=roles_dropdown).\
        then(lambda: database.get_introduction(role=role), outputs=introduction_msg).\
            then(lambda: database.get_history(role=role), outputs=chatbot)
        # then(lambda role: gr.update(value=database.get_introduction(role=role)), inputs=roles_dropdown, outputs=introduction_msg).\

    def user(user_message, history):
        return "", history + [[user_message, None]]

    def bot(history):
        MAX_CONVERSATION_ROUND = 3
        initial_message = {
            "role": "system", 
            "content": get_system_prompt(role)
        }
        history_openai_format = []
        for human, assistant in history[-MAX_CONVERSATION_ROUND:]:
            history_openai_format.append({"role": "user", "content": human})
            if assistant != None:
                history_openai_format.append({"role": "assistant", "content": assistant})
        response = llm_client.get_client().chat.completions.create(
            model = llm_client.get_model(),
            messages = [initial_message] + history_openai_format,
            temperature = 1,
            # max_tokens=150,
            stream = True,
        )

        history[-1][1] = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                history[-1][1] += chunk.choices[0].delta.content
                yield history
        database.chat_history[role] = history
        print("------------当前角色对话历史-----------------")
        print(database.chat_history[role])
        print("------------------------------------------")

    def get_first_sentence(text):
        print(text)
        index_of_full_stop = text.find('。')
        if index_of_full_stop != -1:
            return text[:index_of_full_stop+1]
        index_of_question_mark = text.find('?')
        if index_of_question_mark != -1:
            return text[:index_of_question_mark+1]
        index_of_exclamation_mark = text.find('!')
        if index_of_exclamation_mark != -1:
            return text[:index_of_exclamation_mark+1]
        return None

    # async def chatbot_change(chatbot):
    #     print("---------------chatbot_change  start---------------------------")
    #     print(chatbot)
    #     print("---------------chatbot_change  end---------------------------")
    #     last_reply = chatbot[-1][1]
    #     print("last_reply: ", last_reply)
    #     global first_audio_path
    #     if first_audio_path is None:
    #         first_sentence = get_first_sentence(last_reply)
    #         print("first_sentence: " + str(first_sentence))
    #         if first_sentence is not None:
    #             first_audio_path =  await get_audio_path(first_sentence)
    #             # first_audio_play_btn.click(lambda: first_audio_path, outputs=output_audio)
            
    # chatbot.change(fn=chatbot_change, inputs=chatbot).\
    #     then(lambda: first_audio_path, outputs=output_audio)

    def update_summary():
        summary = generate_new_summary(database.get_summary(role=role), database.chat_history.get(role, [])[-1:], current_role=role)
        database.summary[role] = summary


    input_msg.submit(user, inputs=[input_msg, chatbot], outputs=[input_msg, chatbot], queue=False).then(
        bot, inputs=chatbot, outputs=chatbot
    ).then(update_summary)


    def clear_audio(audio):
        return None
    
    input_audio_button.click(fn=action, inputs=input_audio_button, outputs=input_audio_button).\
        then(clear_audio, inputs=input_audio, outputs=input_audio).\
        then(fn=lambda: None, js=click_js())

    async def get_audio_path(text):
        _voice_type = database.get_voice_type(role=role)
        return await tts.speak(text, _voice_type)


    async def speak(history):
        print('-------speak start1-------')
        print(history)
        print('-------speak start2-------')
        text = history[-1][1]
        _voice_type = database.get_voice_type(role=role)
        return await tts.speak(text, _voice_type)

    input_audio.stop_recording(fn=asr.recognize, inputs=input_audio, outputs=input_msg).then(
        user, inputs=[input_msg, chatbot], outputs=[input_msg, chatbot], queue=False
    ).then(
        bot, inputs=chatbot, outputs=chatbot
    ).then(
        speak, inputs=chatbot, outputs=output_audio
    ).then(
        update_summary
    ).then(
        clear_audio, inputs=input_audio, outputs=input_audio
    )


demo = gr.TabbedInterface([childrend_page, gradio_parents_tab.page, gradio_admin_tab.page], ["小朋友语音对话页面", "家长管理页面", "系统管理页面"])
demo.launch(share=False)
