import service.rag.etl as rag_etl
import service.rag.rag_story_wangwangdui as rag_story_wangwangdui

def test_build_index():
    rag_etl.build_index()
    
    collection = rag_story_wangwangdui.get_collection()

    count = collection.count()
    assert count != 0