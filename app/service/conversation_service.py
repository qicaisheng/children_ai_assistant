from typing import Generator, Optional
import app.core.llm_client as llm_client
from app.core.system_prompt import get_system_prompt_by_role_code
from app.core.conversation_message import MessageType
from app.core.text_segmenter import split_text
from app.repository.message import get_message_repository, LatestMessagesFilter
from app.core.user import get_current_user


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


def get_conversation_history(role_code: int, round: int) -> list[list[Optional[str]]]:
    _user_id = get_current_user().id
    _number = 2 * round + 1
    message_filter = LatestMessagesFilter(user_id=_user_id, role_code=role_code, number=_number)
    messages = get_message_repository().get_latest_by(message_filter)

    conversation_history = []

    for message in messages:
        if message.message_type == MessageType.USER_MESSAGE:
            conversation_history.append([message.content, None])
        elif message.message_type == MessageType.ASSISTANT_MESSAGE:
            if conversation_history and conversation_history[-1][1] is None:
                conversation_history[-1][1] = message.content

    if conversation_history and conversation_history[-1][1] is None:
        return conversation_history[-(round + 1):-1]
    else:
        return conversation_history[-round:]

# stream_reponse = stream_answer("你好", 1)
# for text in stream_reponse:
#     print(text)