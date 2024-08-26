from core.summarization import save_summary, get_summary_by_role_code, Summary, summaries

def test_save_summary():
    summary_data = Summary(role_code=1, summary="Test summary")
    save_summary(summary_data)
    assert summaries[1]["summary"] == "Test summary"

def test_get_summary_by_role_code():
    summary_data = Summary(role_code=2, summary="Another summary")
    save_summary(summary_data)

    result = get_summary_by_role_code(2)

    assert result == "Another summary"

def test_get_summary_by_role_code_not_found():
    result = get_summary_by_role_code(3)

    assert result == ""
