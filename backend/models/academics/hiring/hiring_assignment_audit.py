from pydantic import BaseModel
from datetime import datetime

__authors__ = ["Christian Lee"]
__copyright__ = "Copyright 2025"
__license__ = "MIT"


class HiringAssignmentAudit(BaseModel):
    """
    Pydantic model to represent a snapshot of changes to a Hiring Assignment.
    """

    id: int | None = None
    hiring_assignment_id: int
    changed_by_user_id: int
    change_timestamp: datetime
    change_details: str
