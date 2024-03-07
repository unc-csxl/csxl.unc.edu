"""Join table of membership between User and Role entities.""" ""

from sqlalchemy import Table, Column, ForeignKey
from .entity_base import EntityBase

__authors__ = ["Abdulaziz Al-Shayef, Ben Goulet"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

# Define the section_application table to be used as a join table to persist a
# many-to-many relationship between the section and application table.
section_application_table = Table(
    "section_application",
    EntityBase.metadata,
    Column("section_id", ForeignKey("section.id"), primary_key=True),
    Column("application_id", ForeignKey("application.id"), primary_key=True),
)
