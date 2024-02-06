from pydantic import BaseModel
from .user import User

__authors__ = ["Matt Vu"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class FeedbackIdentity(BaseModel):
    """
    Pydantic model to represent how `Feedback Ticket`s are identified in the system.

    This model is based on the `FeedbackEntity` model, which defines the shape
    of the `Feedback` database in the PostgreSQL database.
    """

    id: int | None


class Feedback(FeedbackIdentity, BaseModel):
    """
    Pydantic model to represent a `Feedback Ticket`.

    This model is based on the `FeedbackEntity` model, which defines the shape
    of the `Feedback Ticket` database in the PostgreSQL database
    """

    id: int
    user_id: int
    user: User
    description: str
    has_resolved: bool


class FeedbackForm(BaseModel):
    """
    Pydantic model to represent fields for a form when creating a Feedback Ticket
    on the frontend

    This model is based on the `FeedbackEntity` model, which defines the shape
    of the `Feedback` database in the PostgreSQL database
    """

    id: int
    user_id: int
    user: User
    description: str
    has_resolved: bool
