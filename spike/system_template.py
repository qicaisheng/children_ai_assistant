import database

SYSTEM_PROMPT_TEMPLATE_PREFIX = "要求：用150字内，用第一人称适合口语表达风格的话回答。"

SYSTEM_PROMPT_TEMPLATE_SUFFIX = """
当前跟你对话的用户信息如下：
姓名：{user.name} 
小名：{user.nickname}
性别：{user.gender}
年龄：{user.age}
描述：{user.description}
基于之前总结的聊天总结和前几次的聊天记录进行回答

当前聊天总结:
{summary}
"""

def get_system_prompt(role):
    system_prompt = SYSTEM_PROMPT_TEMPLATE_PREFIX + database.get_saved_role_template(role=role) + \
        SYSTEM_PROMPT_TEMPLATE_SUFFIX.format(summary=database.get_summary(role=role), user=database.user)
    print("system_prompt: " + system_prompt)
    return system_prompt