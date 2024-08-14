import database

KINDERGARTEN = database.saved_roles_templates["幼儿园老师"] + """基于之前总结的聊天总结和前几次的聊天记录进行回答

当前聊天总结:
{summary}
"""