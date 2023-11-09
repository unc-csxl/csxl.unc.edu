"""Join table of membership between User and Role entities.""" ""

from sqlalchemy import Table, Column, ForeignKey
from .entity_base import EntityBase

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

# Define the user_role table to be used as a join table to persist a
# many-to-many relationship between the users and roles table.
user_role_table = Table(
    "user_role",
    EntityBase.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("role_id", ForeignKey("role.id"), primary_key=True),
)
