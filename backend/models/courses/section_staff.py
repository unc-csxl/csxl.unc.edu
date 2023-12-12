from pydantic import BaseModel

# from backend.entities.courses.roster_role import RosterRole

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class SectionStaff(BaseModel):
    """
    Pydantic model to represent staff members of course sections.
    """

    user_id: int
    # role: RosterRole
