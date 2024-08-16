import gradio as gr
import pandas as pd
from database import saved_roles_templates
import database


person_list = []

def save_prompt(name, prompt):
    if name is None:
        raise gr.Error("Name cannot be empty")
    else:
        saved_roles_templates[name] = prompt
        print(saved_roles_templates)
        return saved_roles_templates[name]

def create_prompt(
    char_name, char_gender, char_species, char_birthday, char_job, char_residence,
    char_nickname, char_zodiac, char_constellation, char_hobbies, char_dislikes,
    char_speech_style, char_self_proclaim, char_experience, char_description, char_opening_line,
    user_name, user_nickname, user_description, user_attitude
):
    prompt = f"""
    任务：你现在正在进行一个角色扮演任务，你需要根据角色的基础信息，生成一个角色的对话。
    ### 角色基础信息
    姓名: {char_name}
    性别: {char_gender}
    物种: {char_species}
    生日 : {char_birthday}
    工作: {char_job}
    居住地: {char_residence}
    昵称: {char_nickname}
    生肖: {char_zodiac}
    星座: {char_constellation}
    爱好: {char_hobbies}
    厌恶: {char_dislikes}
    说话风格: {char_speech_style}
    自称: {char_self_proclaim}
    经历: {char_experience}
    性格描述: {char_description}
    开场白: {char_opening_line}
    注意和你进行对话的用户，他的身份是，你要根据他的身份，选择适合的对话风格和内容
    #### 用户身份
    姓名: {user_name}
    昵称: {user_nickname}
    描述: {user_description}
    态度: {user_attitude}
    """
    relation_prompt = "以下人物是你的社会关系，是你熟知的人。注意当谈及其他人物要考虑人物所处的时代。"
    for person in person_list:
        relation_prompt = relation_prompt + f"姓名： {person['姓名']} 性别： {person['性别']} 物种： {person['物种']} 经历 {person['经历']} "
    return char_name, prompt + relation_prompt


def add_person(name, gender, species, experience):
    global person_list
    person_list.append({"姓名": name, "性别": gender, "物种": species, "经历": experience})
    return pd.DataFrame(person_list)

def clear_inputs():
    global person_list
    person_list = []
    return "", "", "", "", pd.DataFrame(person_list)

with gr.Blocks() as page:
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 角色基础信息")
            with gr.Row():
                name = gr.Textbox(label="姓名", value="")
                gender = gr.Textbox(label="性别", value="")
                species = gr.Textbox(label="物种", value="")
            with gr.Row():
                birthday = gr.Textbox(label="生日 (YYYY-MM-DD)", value="")
                job = gr.Textbox(label="工作", value="")
                residence = gr.Textbox(label="居住地", value="")
            with gr.Row():
                nickname = gr.Textbox(label="昵称", value="")
                zodiac = gr.Textbox(label="生肖", value="")
                constellation = gr.Textbox(label="星座", value="")
           
            hobbies = gr.Textbox(label="爱好", value="")
            dislikes = gr.Textbox(label="厌恶", value="")
            speech_style = gr.Textbox(label="说话风格", value="")
            self_proclaim = gr.Textbox(label="自称", value="")
            experience = gr.Textbox(label="经历", value="")
            character_description = gr.Textbox(label="性格描述", value="")
            opening_line = gr.Textbox(label="开场白", value="")

            gr.Markdown("#### 社会关系")
            with gr.Accordion("添加关联人", open=False):
                with gr.Column():
                    rel_name = gr.Textbox(label="姓名", value="")
                    rel_gender = gr.Textbox(label="性别", value="")
                    rel_species = gr.Textbox(label="物种", value="")
                    rel_experience = gr.Textbox(label="经历", value="")
                    with gr.Row():
                        add_button = gr.Button("添加")
                        clear_button = gr.Button("全部清除")

                    rel_output = gr.DataFrame(headers=["姓名", "性别", "物种", "经历"], row_count=(1, "dynamic"))

                    add_button.click(
                        add_person, 
                        inputs=[rel_name, rel_gender, rel_species, rel_experience], 
                        outputs=rel_output
                    )

                    clear_button.click(
                        clear_inputs, 
                        inputs=[], 
                        outputs=[name, gender, species, experience, rel_output]
                    )

            generate_button = gr.Button("创建人物")
        with gr.Column():
            with gr.Accordion("Prompt 信息", open=False):
                with gr.Row():
                    prompt_name = gr.Textbox(placeholder="你创建的角色名称")
                    query_button = gr.Button("查询Prompt")
                prompt_output = gr.Textbox("### propmt 详情显示区域", lines=10)
                save_button = gr.Button("保存Prompt")
                alert_success = gr.Markdown(visible=True)    
                
            with gr.Accordion("角色配音", open=False):
                refresh_roles_btn = gr.Button("刷新角色")
                roles_dropdown = gr.Dropdown(
                    choices=database.get_saved_roles(), label="选择角色", info="选择对应的角色进行配音", interactive=True,
                    value=database.get_saved_roles()[0]
                )
                voices_dropdown = gr.Dropdown(
                    choices=database.get_supported_voices(), label="选择声音", info="选择对应的声音进行配音", interactive=True,
                    value=database.get_voice_name(roles_dropdown.value)
                )
                def refresh_roles_ropdown():
                    return gr.Dropdown(choices=database.get_saved_roles(), interactive=True)
                
                refresh_roles_btn.click(refresh_roles_ropdown, outputs=roles_dropdown)

                roles_dropdown.change(lambda role: database.get_voice_name(role=role), inputs=roles_dropdown, outputs=voices_dropdown)
                save_role_voice_btn = gr.Button("保存角色配音")

                def save_role_voice_mapping(role, voice_type):
                    print("save_role_voice_mapping, role: " + role + " voice_type, " + voice_type)
                    database.role_voice_mapping[role] = voice_type

                save_role_voice_btn.click(fn=save_role_voice_mapping, inputs=[roles_dropdown, voices_dropdown])
        
            
        generate_button.click(
            create_prompt, 
            inputs=[
                name, gender, species, birthday, job, residence,
                nickname, zodiac, constellation, hobbies, dislikes,
                speech_style, self_proclaim, experience, character_description, opening_line,
                user_name, user_nickname, user_description, user_attitude,
            ], 
            outputs=[prompt_name, prompt_output]
        )


    def query_prompt(name):
        return saved_roles_templates.get(name, "No prompt found for this name")


    save_button.click(
        save_prompt, 
        inputs=[prompt_name, prompt_output], 
        outputs= alert_success
    )

    query_button.click(
        query_prompt, 
        inputs=prompt_name, 
        outputs=prompt_output
    )

