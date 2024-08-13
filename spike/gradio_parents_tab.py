import gradio as gr
import database



with gr.Blocks() as page:
    refresh_btm = gr.Button("刷新")
    
    chatbot2 = gr.Chatbot(value=database.chat_history, label="小朋友对话记录")

    summary_btm = gr.Button("查看对话总结")
    summary_msg = gr.Textbox(label="小朋友对话总结")


    refresh_btm.click(lambda: database.chat_history, outputs=chatbot2)

    def summary():
        return database.summary

    summary_btm.click(summary, outputs=summary_msg)