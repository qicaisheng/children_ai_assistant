import os
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from app.service.rag.chroma import get_collection

embedding_func = OpenAIEmbeddings(model="embedding-3", base_url="https://open.bigmodel.cn/api/paas/v4/", api_key=os.environ.get("ZHIPU_API_KEY"))

def build_index():
    clear_index()
    story = "走失的小野雁"
    raw_documents = TextLoader(f'./story/{story}.txt').load()
    text_splitter = CharacterTextSplitter(chunk_size=400, chunk_overlap=50, separator="\n")
    documents = text_splitter.split_documents(raw_documents)
    for doc in documents:
        doc.metadata["story_name"] = story
    Chroma.from_documents(documents, embedding_func, collection_name="story_wangwangdui", persist_directory="./chroma")

def clear_index():
    story = "走失的小野雁"
    get_collection().delete(where={"story_name": story})






