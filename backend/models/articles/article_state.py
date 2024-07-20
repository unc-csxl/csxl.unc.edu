"""Enum for the state of an article."""

from enum import Enum

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class ArticleState(Enum):
    """
    Enum for the state of an article.
    """

    DRAFT = "Draft"
    PUBLISHED = "Published"
    ARCHIVED = "Archived"
