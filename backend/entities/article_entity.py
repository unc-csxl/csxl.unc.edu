"""Definition of SQLAlchemy table-backed object mapping entity for news articles."""

from datetime import datetime
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .entity_base import EntityBase
from typing import Self
from ..models.articles import ArticleState
from sqlalchemy import Enum as SQLAlchemyEnum
from .article_author_entity import article_author_table

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class ArticleEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Article` table"""

    # Name for the article table in the PostgreSQL database
    __tablename__ = "article"

    # Article properties (columns in the database table)

    # Unique ID for the article
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Slug to more coloquially identify the article
    slug: Mapped[int] = mapped_column(String, unique=True)
    # State of the article
    state: Mapped[ArticleState] = mapped_column(
        SQLAlchemyEnum(ArticleState), nullable=False
    )
    # Title of the article
    title: Mapped[str] = mapped_column(String, nullable=False, default="")
    # Synopsis of the article (to show on the article page)
    synopsis: Mapped[str] = mapped_column(String, nullable=False, default="")
    # Image URL for the article (to show on the article page)
    image_url: Mapped[str] = mapped_column(String, nullable=False, default="")
    # Time when the article was initially published
    published: Mapped[datetime] = mapped_column(DateTime, nullable=False, default="")
    # Time when the article was last modified
    published: Mapped[str] = mapped_column(String, nullable=False, default="")
    # Whether or not the article should be treated as an announcement
    is_announcement: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )

    # Organization connected to this article.
    # NOTE: This defines a one-to-many relationship between the organization and articles tables.
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"))
    organization: Mapped["OrganizationEntity"] = relationship(back_populates="articles")

    # All of the authors for this article.
    # NOTE: This field establishes a many-to-many relationship between the users and article table.
    #       and uses the "article_author" table as the join table.
    authors: Mapped[list["UserEntity"]] = relationship(
        secondary=article_author_table, back_populates="articles"
    )
