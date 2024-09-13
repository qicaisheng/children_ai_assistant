from typing import Generator
import core.llm_client as llm_client
from core.system_prompt import get_system_prompt_by_role_code
from core.conversation_message import get_conversation_history
from core.text_segmenter import split_text

MAX_CONVERSATION_ROUND = 3
MAX_CONVERSATION_HISTORY_SIZE = 2 * MAX_CONVERSATION_ROUND


def no_stream_answer(user_input: str, role_code: int) -> list[str]:
    completion = llm_client.get_client().chat.completions.create(
        model = llm_client.get_model(),
        messages = build_llm_request_message(user_input, role_code),
    )
    content = completion.choices[0].message.content
    return split_text(content)

def stream_answer(user_input: str, role_code: int) -> Generator[str, None, None]:
    response = llm_client.get_client().chat.completions.create(
        model = llm_client.get_model(),
        messages = build_llm_request_message(user_input, role_code),
        stream=True
    )

    for chunk in response:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


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

# stream_reponse = stream_answer("你好", 1)
# for text in stream_reponse:
#     print(text)