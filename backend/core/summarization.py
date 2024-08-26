from pydantic import BaseModel
import core.llm_client as llm_client
from core.user import get_current_user
from core.role import get_role_by_code

summaries = {}

class Summary(BaseModel):
    role_code: int
    summary: str

_DEFAULT_SUMMARIZER_TEMPLATE = """基于给定当前总结和新的对话生成新的{user}和{role}的对话总结，其中User代表{user}，Assistant代表{role}。

例子
当前总结:
{user}询问{role}对人工智能的看法。{role}认为人工智能是一种积极的力量。

新的对话：
User: 你为什么认为人工智能是一种积极的力量？
Assistant: 因为人工智能将帮助人类发挥他们的全部潜力。

新的总结：
{user}询问{role}对人工智能的看法。{role}认为人工智能是一种积极的力量，因为它将帮助人类发挥他们的全部潜力。
例子结束。

当前总结:
{summary}

新的对话:
{new_lines}

新的总结:"""


def generate_new_summary(current_summary: str, new_conversation_history: list, role_code: int):
    role = get_role_by_code(role_code)
    new_liens = ""
    for human, assistant in new_conversation_history:
        new_liens += "User: " + human + "\n"
        new_liens += "Assistant: " + assistant + "\n"
    content = _DEFAULT_SUMMARIZER_TEMPLATE.format(summary=current_summary, new_lines=new_liens, role=role.name, user=get_current_user().nickname)
    completion = llm_client.get_client().chat.completions.create(
        model=llm_client.get_model(),
        messages=[
            {"role": "user", "content": content}
        ]    
    )
    new_summary = completion.choices[0].message.content
    print("--------------生成总结 summary request---------------------")
    print("summary request: " + content)
    print("--------------生成总结 summary response---------------------")
    print("summary response: " + new_summary)
    print("----------------------------------------------------------")
    return new_summary

def save_summary(summary: Summary):
    summaries[summary.role_code] = summary.dict()

def get_summary_by_role_code(role_code: int) -> str:
    summary = summaries.get(role_code)
    if summary:
        return summary['summary']
    return ""


# print(generate_new_summary("", [["想听故事", "那我就给你讲一个有趣的故事吧。从前，有一只小猴子，它非常喜欢吃香蕉。有一天，它来到了一个香蕉园，里面有很多很多的香蕉。小猴子高兴极了，它开始疯狂地吃香蕉，一个接着一个，吃得肚子都圆滚滚的。可是，它发现自己吃不完那么多的香蕉，怎么办呢"]], 1))