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
    token = postgresql_session_context.set(session)
    try:
        yield session
        try:
            print("commit session")
            session.commit()
        except Exception as commit_error:
            print(f"commit failed, exception: {commit_error}")
            session.rollback()
            raise
    except Exception as e:
        print(f"rollback session, exception: {e}")
        try:
            session.rollback()
        except Exception as rollback_error:
            print(f"rollback failed, exception: {rollback_error}")
        raise
    finally:
        print("close session")
        try:
            session.close()
        except Exception as close_error:
            print(f"session close failed, exception: {close_error}")
        finally:
            postgresql_session_context.reset(token)


postgresql_session_context: ContextVar[Session] = ContextVar('postgresql_session')


def get_postgresql_session() -> Session:
    return postgresql_session_context.get()


def set_postgresql_session(session: Session):
    postgresql_session_context.set(session)
