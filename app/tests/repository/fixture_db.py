import logging

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer


@pytest.fixture(scope="module")
def db_session():
    with PostgresContainer("postgres:latest", driver="psycopg") as postgres:
        engine = create_engine(postgres.get_connection_url())

        alembic_cfg = Config("../../alembic.ini")
        alembic_cfg.set_main_option('script_location', "../../alembic")
        alembic_cfg.set_main_option('sqlalchemy.url', postgres.get_connection_url())

        print("Running Alembic migrations")
        print(f"Running on DB: {postgres.get_connection_url()}")
        try:
            command.upgrade(alembic_cfg, "head")
        except Exception as e:
            print(f"Migration failed: {e}")
        print("Alembic migrations completed")

        inspector = inspect(engine)
        print(f"Existing tables: {inspector.get_table_names()}")

        Session = sessionmaker(bind=engine)
        session = Session()
        yield session

        session.close()
