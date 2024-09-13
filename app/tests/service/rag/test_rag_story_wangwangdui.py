import app.service.rag.rag_story_wangwangdui as rag_story_wangwangdui


def test_answer():
    result = rag_story_wangwangdui.answer("走失的小野雁", "为什么要走")
    assert result is not None

