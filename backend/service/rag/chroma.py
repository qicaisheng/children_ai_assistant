import chromadb
import chromadb.utils.embedding_functions as embedding_functions
import os


def get_collection():
    _openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=os.environ.get("ZHIPU_API_KEY"),
                api_base="https://open.bigmodel.cn/api/paas/v4/",
                model_name="embedding-3"
            )

    _chroma_client = chromadb.PersistentClient()
    _collection = _chroma_client.get_or_create_collection("story_wangwangdui", embedding_function=_openai_ef)
    return _collection
