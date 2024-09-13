from app.core.role import Role
from app.core.system_prompt import get_system_prompt_by_role_code
from app.core.user import User

def test_get_system_prompt_by_role_code(monkeypatch):
    # Mock get_role_by_code
    mock_role = {
        "code": 1,
        "name": "Test Role",
        "prompt": "Test Prompt",
        "voice_name": "Test Voice",
        "voice_type": "Test Voice Type",
        "self_introduction": "Test Introduction",
        "self_introduction_voice": "Test Introduction Voice",
        "retry_voice": "Test Retry Voice",
    }
    monkeypatch.setattr('core.system_prompt.get_role_by_code', lambda code: Role(**mock_role))

    # Mock get_summary_by_role_code
    monkeypatch.setattr('core.system_prompt.get_summary_by_role_code', lambda code: "Test Summary")

    # Mock get_current_user
    mock_user = {
        "device_sn": "Device SN",
        "name": "Test User",
        "nickname": "Tester",
        "gender": "Male",
        "age": 30,
        "description": "A test user for unit testing."
    }
    monkeypatch.setattr('core.system_prompt.get_current_user', lambda: User(**mock_user))

    system_prompt = get_system_prompt_by_role_code(1)
    expected_prompt = (
        "Test Prompt\n当前跟你对话的用户信息如下：\n姓名：Test User \n小名：Tester\n"
        "性别：Male\n年龄：30\n描述：A test user for unit testing.\n\n"
        "基于之前总结的聊天总结和前几次的聊天记录进行回答，注意：如果你不清楚用户的问题，可以先问一下，然后再尝试回答。\n\n"
        "当前聊天总结:\nTest Summary\n\n"
        "要求：用100字内，用第一人称适合口语表达风格的话回答，尽可能用简单词汇通俗易懂有趣的方式介绍。已经说过的话不用多次说\n"
    )
    
    assert system_prompt == expected_prompt
    