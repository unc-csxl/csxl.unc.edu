from pydantic import BaseModel
from ..roster_role import RosterRole


__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class SectionMember(BaseModel):
    """
    Pydantic model to represent the information about a user who is a
    staff of a section of a course.

    This model is based on the `UserEntity` model, which defines the shape
    of the `User` database in the PostgreSQL database
    """

    id: int | None = None
    first_name: str
    last_name: str
    pronouns: str
    member_role: RosterRole
