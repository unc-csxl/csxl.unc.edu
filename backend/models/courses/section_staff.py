from pydantic import BaseModel
from ...models.user import User
from ...entities.courses.user_section_entity import RosterRole

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class SectionStaff(BaseModel):
    """
    Pydantic model to represent staff members of course sections.
    """

    user_id: int
    role: RosterRole
