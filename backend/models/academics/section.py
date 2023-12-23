from pydantic import BaseModel
from datetime import datetime
from .section_member import SectionMember
from ..room import Room

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class Section(BaseModel):
    """
    Pydantic model to represent a `Section`.

    This model is based on the `SectionEntity` model, which defines the shape
    of the `Section` database in the PostgreSQL database
    """

    id: int
    course_id: str
    number: str
    term_id: str
    meeting_pattern: str
    staff: list[SectionMember] = []
    lecture_room: Room | None = None
    office_hour_rooms: list[Room] = []
