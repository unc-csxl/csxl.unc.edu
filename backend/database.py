"""SQLAlchemy DB Engine and Session niceties for FastAPI dependency injection."""

import sqlalchemy
from sqlalchemy.orm import Session
from .env import getenv

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


def _engine_str(database: str = getenv("POSTGRES_DATABASE")) -> str:
    """Helper function for reading settings from environment variables to produce connection string."""
    dialect = "postgresql+psycopg2"
    user = getenv("POSTGRES_USER")
    password = getenv("POSTGRES_PASSWORD")
    host = getenv("POSTGRES_HOST")
    port = getenv("POSTGRES_PORT")
    return f"{dialect}://{user}:{password}@{host}:{port}/{database}"


def _in_production() -> bool:
    """Helper function for reading settings from environment variables to determine verbosity of SQL output."""
    return getenv("MODE") == "production"


engine = sqlalchemy.create_engine(_engine_str(), echo=not _in_production())
"""Application-level SQLAlchemy database engine."""


def db_session():
    """Generator function offering dependency injection of SQLAlchemy Sessions."""
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
