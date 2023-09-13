# This script inserts the demo data into the SQLAlchemy database.
# This script is meant to add the demo data into production.

import sys
from sqlalchemy import text
from sqlalchemy.orm import Session
from ..database import engine
from ..env import getenv
from .. import entities

from ..test.services import role_data, user_data, permission_data
from ..test.services.organization import organization_demo_data

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

if getenv("MODE") != "development":
    print("This script can only be run in development mode.", file=sys.stderr)
    print("Add MODE=development to your .env file in workspace's `backend/` directory")
    exit(1)

with Session(engine) as session:
    organization_demo_data.insert_fake_data(session)
    session.commit()