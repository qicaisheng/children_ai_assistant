import service.rag.rag_story_wangwangdui as rag_story_wangwangdui


def test_dd():
    assert 1==1

def test_answer():
    # rag_story_wangwangdui.build_index()
    result = rag_story_wangwangdui.answer("走失的小野雁", "为什么要走")
    assert result is not None

