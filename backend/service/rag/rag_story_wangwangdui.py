from core.llm_client import get_client, get_model
import chromadb
import chromadb.utils.embedding_functions as embedding_functions
import os

RAG_PROMPT = """
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.\nQuestion: {question} \nContext: {context} \nAnswer:
"""

def get_collection():
    _openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=os.environ.get("ZHIPU_API_KEY"),
                api_base="https://open.bigmodel.cn/api/paas/v4/",
                model_name="embedding-3"
            )

    _chroma_client = chromadb.PersistentClient()
    _collection = _chroma_client.get_or_create_collection("story_wangwangdui", embedding_function=_openai_ef)
    return _collection

def answer(story: str, question: str) -> str:

    embedding_response = get_collection().query(
        query_texts=[question],
        n_results=4,
        where={"story_name": story}
    )
    context = "\n\n".join(doc for doc in embedding_response['documents'][0])
    user_message = RAG_PROMPT.format(context=context, question=question)

    print(f"RAG llm user_message: {user_message}")
    completion = get_client().chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "user", "content": user_message}
        ]
    )
    print(f"RAG llm response: {completion}")
    return completion.choices[0].message.content