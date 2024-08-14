from enum import Enum
from openai import OpenAI
import os

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

class LLM_MODEL(Enum):
    DOUBAO = "DOUBAO"
    ZHIPU = "ZHIPU"
    DEEPSEEK = "DEEPSEEK"

_mapping = {
    str(LLM_MODEL.DOUBAO): {"client": doubao_client, "model": os.environ.get("MODEL_ENDPOINT_ID")},
    str(LLM_MODEL.ZHIPU): {"client": zhipu_client, "model": "GLM-4-AirX"},
    str(LLM_MODEL.DEEPSEEK): {"client": deepseek_client, "model": "deepseek-chat"},
}

selected_llm = LLM_MODEL.DEEPSEEK

def get_client() -> OpenAI:
    _client = _mapping.get(str(selected_llm)).get('client')
    print(f"LLM: {selected_llm}")
    return _client;


def get_model():
    return _mapping.get(str(selected_llm)).get('model');
