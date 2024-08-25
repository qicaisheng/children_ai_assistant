from core.role import get_role_by_code

def test_get_role_by_code():
    role = get_role_by_code(1)
    assert role.name == "幼儿园老师"
    assert role.voice_name == "通用女声"
    assert role.voice_type == "BV001_streaming"