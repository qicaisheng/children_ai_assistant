

from enum import Enum
from core.llm_client import get_client, get_model

class Story(Enum):
    DAYOULUN = "挽救大游轮"
    XIAOYEYAN = "走失的小野雁"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


