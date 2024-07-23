"""Join table of membership between Article and User entities.""" ""

from sqlalchemy import Table, Column, ForeignKey
from .entity_base import EntityBase

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

article_author_table = Table(
    "article_author",
    EntityBase.metadata,
    Column("article_id", ForeignKey("article.id"), primary_key=True),
    Column("user_id", ForeignKey("user.id"), primary_key=True),
)
