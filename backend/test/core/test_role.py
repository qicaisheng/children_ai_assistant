from core.role import get_role_by_code, set_current_role_code, get_current_role

def test_get_role_by_code():
    role = get_role_by_code(1)
    assert role.name == "幼儿园老师"
    assert role.voice_name == "通用女声"
    assert role.voice_type == "BV001_streaming"

def test_set_current_role_code():
    set_current_role_code(None)

    set_current_role_code(1)

    current_role = get_current_role()
    assert current_role is not None
    assert current_role.code == 1
    assert current_role.name == "幼儿园老师"
