import database

SYSTEM_PROMPT_TEMPLATE_PREFIX = "要求：用100个以内的字进行回答。"

SYSTEM_PROMPT_TEMPLATE_SUFFIX = """基于之前总结的聊天总结和前几次的聊天记录进行回答

当前聊天总结:
{summary}
"""

def get_system_prompt(role):
    system_prompt = SYSTEM_PROMPT_TEMPLATE_PREFIX + database.get_saved_role_template(role=role) + SYSTEM_PROMPT_TEMPLATE_SUFFIX.format(summary=database.get_summary(role=role))
    print("system_prompt: " + system_prompt)
    return system_prompt