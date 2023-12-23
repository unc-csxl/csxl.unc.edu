"""
Bootstrapping niceties for working in the REPL.

To use this script, from project root PWD, in a terminal:

python3 -i backend/script/repl.py
"""

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

import sys

# Establish PYTHONPATH to be project root. This is necessary
# for package/module imports to work as expected.
sys.path.append("/workspace")

from sqlalchemy import select, join
from sqlalchemy.orm import joinedload, aliased
from backend.database import db_session
from backend.services import PermissionService, UserService

print("=== CSXL Development Repl ===\n")

print("The following globals are initialized:\n")

from backend.entities import *
from backend.entities.coworking import *
from backend.entities.academics import *

print(" - all entities in backend/entities/__init__.py")
print(" - all entities in backend/entities/coworking/__init__.py")
print(" - all entities in backend/entities/courses/__init__.py")

from backend.models import *
from backend.models.coworking import *

print(" - all models in backend/models/__init__.py")
print(" - all models in backend/models/coworking/__init__.py")

session = next(db_session())
print(" - session: a SQLAlchemy ORM Session")

permission_svc = PermissionService(session)
print(" - permission_svc: a PermissionService")

user_svc = UserService(session, permission_svc)
print(" - user_svc: a UserService")

print("\n=============================\n")
