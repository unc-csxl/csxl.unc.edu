"""Role is the data object for groups of related access controls users can be added to."""

from pydantic import BaseModel


__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class Role(BaseModel):
    """
    Pydantic model to represent a `Role`.

    This model is based on the `RoleEntity` model, which defines the shape
    of the `Role` database in the PostgreSQL database.
    """

    id: int | None = None
    name: str
