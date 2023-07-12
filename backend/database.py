"""SQLAlchemy DB Engine/Session niceties for FastAPI dependency injection."""

import sqlalchemy
from sqlalchemy.orm import Session
from .env import getenv

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


def _engine_str(database=getenv("POSTGRES_DATABASE")) -> str:
    """Helper function for to produce connection strings from env vars."""
    dialect = "postgresql+psycopg2"
    user = getenv("POSTGRES_USER")
    password = getenv("POSTGRES_PASSWORD")
    host = getenv("POSTGRES_HOST")
    port = getenv("POSTGRES_PORT")
    return f"{dialect}://{user}:{password}@{host}:{port}/{database}"


engine = sqlalchemy.create_engine(_engine_str(), echo=True)
"""Application-level SQLAlchemy database engine."""


def db_session():
    """Dependency injection for SQLAlchemy Sessions."""
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
