from pydantic import BaseModel

from backend.models.academics.section_member import SectionMember
from backend.models.room import Room
from ..public_user import PublicUser

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class Section(BaseModel):
    """
    Pydantic model to represent a `Section`.

    This model is based on the `SectionEntity` model, which defines the shape
    of the `Section` database in the PostgreSQL database
    """

    id: int | None = None
    course_id: str
    number: str
    term_id: str
    meeting_pattern: str
    lecture_room: Room | None = None
    staff: list[SectionMember] = []
    office_hour_rooms: list[Room] = []
    override_title: str
    override_description: str
    enrolled: int
    total_seats: int


class EditedSection(BaseModel):
    """
    Pydantic model to represent a `EditedSection`.

    This model is based on the `SectionEntity` model, which defines the shape
    of the `Section` database in the PostgreSQL database
    """

    id: int | None = None
    course_id: str
    number: str
    term_id: str
    meeting_pattern: str
    lecture_room: Room | None = None
    override_title: str
    override_description: str
    enrolled: int
    total_seats: int
    instructors: list[PublicUser]


class CatalogSectionIdentity(BaseModel):
    id: int | None = None
    subject_code: str
    course_number: str
    section_number: str
    course_title: str


class CatalogSection(CatalogSectionIdentity):
    """
    Pydantic model that represents a section for the catalog page.
    """

    title: str
    meeting_pattern: str
    description: str
    lecture_room: Room | None = None
    instructors: list[PublicUser]
    enrolled: int
    total_seats: int
