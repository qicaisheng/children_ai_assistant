from contextvars import ContextVar

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from functools import lru_cache
from sqlalchemy import create_engine
from app.system.config import get_db_uri


@lru_cache(maxsize=None)
def get_engine():
    db_string = get_db_uri()
    return create_engine(db_string, pool_pre_ping=True)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
Base = declarative_base()


def yield_postgresql_session():
    session: Session = SessionLocal()
    try:
        yield session
        print("commit session")
        session.commit()
    except Exception:
        print("rollback session")
        session.rollback()
    finally:
        print("close session")
        session.close()


postgresql_session_context: ContextVar[Session] = ContextVar('postgresql_session')


def get_postgresql_session() -> Session:
    return postgresql_session_context.get()


def set_postgresql_session(session: Session):
    postgresql_session_context.set(session)
