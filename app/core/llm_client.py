from enum import Enum
from openai import OpenAI
import os
import config
from core.llm_model import LLM_MODEL

openai_client = OpenAI()

doubao_client = OpenAI(
    api_key=os.environ.get("ARK_API_KEY"),
    base_url="https://ark.cn-beijing.volces.com/api/v3",
)

zhipu_client = OpenAI(
    api_key=os.environ.get("ZHIPU_API_KEY"),
    base_url="https://open.bigmodel.cn/api/paas/v4/",
)

deepseek_client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)



_mapping = {
    str(LLM_MODEL.DOUBAO): {"client": doubao_client, "model": os.environ.get("MODEL_ENDPOINT_ID")},
    str(LLM_MODEL.ZHIPU): {"client": zhipu_client, "model": "GLM-4-AirX"},
    str(LLM_MODEL.DEEPSEEK): {"client": deepseek_client, "model": "deepseek-chat"},
    str(LLM_MODEL.OPENAI): {"client": openai_client, "model": "gpt-4o"},
}

selected_llm = config.llm

def get_client() -> OpenAI:
    _client = _mapping.get(str(selected_llm)).get('client')
    print(f"LLM: {selected_llm}")
    return _client;


def get_model():
    return _mapping.get(str(selected_llm)).get('model');

def get_embedding_client() -> OpenAI:
    return zhipu_client;

def get_embedding_model():
    zhipu_embedding_model = "embedding-3"
    return zhipu_embedding_model
