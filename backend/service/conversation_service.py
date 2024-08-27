import core.llm_client as llm_client
from core.system_prompt import get_system_prompt_by_role_code
from core.conversation_message import get_conversation_history

MAX_CONVERSATION_ROUND = 0
MAX_CONVERSATION_HISTORY_SIZE = 2 * MAX_CONVERSATION_ROUND


def no_stream_answer(user_input: str, role_code: int):
    completion = llm_client.get_client().chat.completions.create(
        model = llm_client.get_model(),
        messages = build_llm_request_message(user_input, role_code),
    )
    content = completion.choices[0].message.content
    return content

def build_llm_request_message(user_input: str, role_code: int) -> list[dict]:
    initial_message = {
        "role": "system", 
        "content": get_system_prompt_by_role_code(role_code)
    }
    history = get_conversation_history(role_code=role_code, round=MAX_CONVERSATION_ROUND)
    history.append([user_input, None])
    history_openai_format = []
    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human})
        if assistant != None:
            history_openai_format.append({"role": "assistant", "content": assistant})
    messages = [initial_message] + history_openai_format
    return messages
