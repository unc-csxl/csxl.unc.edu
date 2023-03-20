"""Create database in blank development environment.

This script is used in the developer container setup process. Its sole purpose
is to create a postgres database from database connection environment variables.

Usage: python3 -m script.create_database
"""

import sqlalchemy
import sys
from ..env import getenv

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


if getenv("MODE") != "development":
    print("This script can only be run in development mode.", file=sys.stderr)
    print("Add MODE=development to your .env file in workspace's `backend/` directory")
    exit(1)


def _engine_str() -> str:
    """Helper function for reading settings from environment variables to produce connection string."""
    dialect = "postgresql+psycopg2"
    user = getenv("POSTGRES_USER")
    password = getenv("POSTGRES_PASSWORD")
    host = getenv("POSTGRES_HOST")
    port = getenv("POSTGRES_PORT")
    return f"{dialect}://{user}:{password}@{host}:{port}"


engine = sqlalchemy.create_engine(_engine_str(), echo=True)
"""Application-level SQLAlchemy database engine."""


with engine.connect() as connection:
    connection.execute(
        sqlalchemy.text("COMMIT")
    )  # Hack: CREATE DATABASE cannot begin inside a transaction.
    database = getenv("POSTGRES_DATABASE")
    stmt = sqlalchemy.text(f"CREATE DATABASE {database}")
    connection.execute(stmt)
