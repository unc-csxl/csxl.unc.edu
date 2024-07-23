from pydantic import BaseModel
from ..public_user import PublicUser

__authors__ = [
    "Ajay Gandecha",
    "Sadie Amato",
    "Bailey DeSouza",
    "Meghan Sun",
    "Maddy Andrews",
]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class NewCourseSite(BaseModel):
    """
    Pydantic model to represent a new course site.
    """

    title: str
    term_id: str
    section_ids: list[int]


class UpdatedCourseSite(BaseModel):
    """
    Pydantic model to represent a new course site.
    """

    id: int
    title: str
    term_id: str
    section_ids: list[int]
    gtas: list[PublicUser]
    utas: list[PublicUser]


class CourseSite(BaseModel):
    """
    Pydantic model to represent a `CourseSite`.

    This model is based on the `CourseSiteEntity` model, which defines the shape
    of the `OfficeHoursSection` database in the PostgreSQL database.
    """

    id: int
    title: str
    term_id: str
