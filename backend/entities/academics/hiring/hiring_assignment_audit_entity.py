from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from ...entity_base import EntityBase

__authors__ = ["Christian Lee"]
__copyright__ = "Copyright 2025"
__license__ = "MIT"


class HiringAssignmentAuditEntity(EntityBase):
    """Schema for the `academics__hiring__assignment_audit` table."""

    __tablename__ = "academics__hiring__assignment_audit"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # The assignment being modified
    hiring_assignment_id: Mapped[int] = mapped_column(
        ForeignKey("academics__hiring__assignment.id")
    )

    # Who made the change
    changed_by_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    changed_by_user: Mapped["UserEntity"] = relationship("UserEntity")

    # When it happened
    change_timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # What changed (e.g. "Status: Draft -> Commit")
    change_details: Mapped[str] = mapped_column(String)
