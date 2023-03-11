"""Reset the database by dropping all tables, creating tables, and inserting demo data."""

from .dev_data import users
import sys
import entities
from env import getenv
from database import engine
from sqlalchemy.orm import Session

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


if getenv("MODE") != "development":
    print("This script can only be run in development mode.", file=sys.stderr)
    print("Add MODE=development to your .env file in workspace's `backend/` directory")
    exit(1)


# Reset Tables
entities.EntityBase.metadata.drop_all(engine)
entities.EntityBase.metadata.create_all(engine)


# Insert Dev Data from `dev_data`

with Session(engine) as session:
    to_entity = entities.UserEntity.from_model
    session.add_all([to_entity(model) for model in users.models])
    session.commit()
