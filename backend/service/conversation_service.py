import core.llm_client as llm_client
from core.system_prompt import get_system_prompt_by_role_code

MAX_CONVERSATION_ROUND = 2
MAX_CONVERSATION_HISTORY_SIZE = 2 * MAX_CONVERSATION_ROUND


def no_stream_answer(user_input: str, role_code: int):
    global conversation_history 
    conversation_history = conversation_history[-MAX_CONVERSATION_HISTORY_SIZE:]
    conversation_history.append({"role": "user", "content": user_input})
    initial_message = {
        "role": "system", 
        "content": get_system_prompt_by_role_code(role_code)
    }    
    completion = llm_client.get_client().chat.completions.create(
        model=llm_client.get_model,
        messages=[initial_message] + conversation_history,
    )
    content = completion.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": content})
    return content
