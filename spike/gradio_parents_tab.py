import gradio as gr
import database



with gr.Blocks() as page:
    with gr.Row():
        with gr.Column():
            refresh_btn = gr.Button("刷新对话历史")
            chatbots = {}

            @gr.render(triggers=[refresh_btn.click])
            def render_chatbots():
                if len(database.chat_history) == 0:
                    gr.Markdown("暂时还没有对话记录")
                for _role, _history in database.chat_history.items():
                    chatbots[_role] = gr.Chatbot(value=_history, label=f"小朋友和{_role}的对话记录")

        with gr.Column():
            summary_btn = gr.Button("刷新对话总结")
            summary_msg = gr.Markdown(label="小朋友对话总结")


    def summary():
        if len(database.summary) == 0:
            return "暂时还没有对话记录"
        summary = ""
        for _role, _summary in database.summary.items():
            summary += f"""## 跟{_role}对话总结：
            {_summary}
            """
        return summary

    summary_btn.click(summary, outputs=summary_msg)