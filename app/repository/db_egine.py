from functools import lru_cache
from sqlalchemy import create_engine
from app.system.config import get_db_uri


@lru_cache(maxsize=None)
def get_engine():
    db_string = get_db_uri()
    return create_engine(db_string, pool_pre_ping=True)