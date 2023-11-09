from pydantic import BaseModel
from .user import User

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class Log(BaseModel):
    """
    Pydantic model to represent a `Log`.

    This model is based on the `LogEntity` model, which defines the shape
    of the `Log` database in the PostgreSQL database.
    """

    id: int | None = None
    description: str
    user_id: int


class LogDetails(Log):
    """
    Pydantic model to represent a `log`, including back-populated
    relationship fields.

    This model is based on the `LogEntity` model, which defines the shape
    of the `Log` database in the PostgreSQL database.
    """

    user: User
