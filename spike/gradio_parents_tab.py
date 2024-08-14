import gradio as gr
import database



with gr.Blocks() as page:
    refresh_btm = gr.Button("刷新")
    chatbots = {}

    for _role, _history in database.chat_history.items():
        chatbots[_role] = gr.Chatbot(value=_history, label=f"小朋友和{_role}的对话记录")


    def refresh_chatbots():
        print(database.chat_history)

    summary_btm = gr.Button("查看对话总结")
    summary_msg = gr.Markdown(label="小朋友对话总结")


    # refresh_btm.click(lambda : refresh_chatbots())

    def summary():
        summary = ""
        for _role, _summary in database.summary.items():
            summary += f"""## 跟{_role}对话总结：
            {_summary}
            """
        return summary

    summary_btm.click(summary, outputs=summary_msg)