"""Definition of SQLAlchemy table-backed object mapping entity for hiring assignments."""

from sqlalchemy import Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLAlchemyEnum
from typing import Self
from datetime import datetime

from ...entity_base import EntityBase
from ....models import PublicUser
from ....models.roster_role import RosterRole
from ....models.academics.hiring.hiring_assignment import (
    HiringAssignmentStatus,
    HiringAssignmentOverview,
    HiringAssignmentDraft,
    HiringAssignmentSummaryOverview,
    HiringAssignmentCsvRow,
)

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class HiringAssignmentEntity(EntityBase):
    """Serves as the database model schema defining the shape of the hiring assignment table"""

    # Name for the review table in the PostgreSQL database
    __tablename__ = "academics__hiring__assignment"

    # Properties (columns in the database table)

    # Unique ID
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Term the section is in
    # NOTE: This defines a one-to-many relationship between the term and sections tables.
    term_id: Mapped[str] = mapped_column(
        ForeignKey("academics__term.id"), nullable=False
    )
    term: Mapped["TermEntity"] = relationship(back_populates="hiring_assignments")

    # Course site this assignment is for
    # NOTE: This defines a one-to-many relationship between the assignment and course site tables.
    course_site_id: Mapped[int] = mapped_column(
        ForeignKey("course_site.id"), nullable=False
    )
    course_site: Mapped["CourseSiteEntity"] = relationship(
        back_populates="hiring_assignments"
    )

    # User (the student that the assignment is for)
    # NOTE: This defines a one-to-many relationship between the user and assignments tables.
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user: Mapped["UserEntity"] = relationship(back_populates="hiring_assignments")

    # Optional ID for an application review.
    # NOTE: This defines a one-to-many relationship between the user and assignments tables.
    application_review_id: Mapped[int] = mapped_column(
        ForeignKey("academics__hiring__application_review.id"), nullable=True
    )

    # Hiring level for the assignment
    # NOTE: This defines a one-to-many relationship between the assignment and level tables.
    hiring_level_id: Mapped[int] = mapped_column(
        ForeignKey("academics__hiring__level.id"), nullable=False
    )
    hiring_level: Mapped["HiringLevelEntity"] = relationship(
        back_populates="hiring_assignments"
    )

    # Status (Draft, Commit, Final)
    status: Mapped[HiringAssignmentStatus] = mapped_column(
        SQLAlchemyEnum(HiringAssignmentStatus),
        nullable=False,
    )

    # Position number (listed in ConnectCarolina, used for hiring purposes)
    position_number: Mapped[str] = mapped_column(String, nullable=True)

    # Epar (used for hiring purposes)
    epar: Mapped[str] = mapped_column(String, nullable=True)

    # Whether or not the user has submitted an I9
    i9: Mapped[bool] = mapped_column(Boolean, nullable=True)

    # Additional notes left by the assigner about this assignment.
    notes: Mapped[str] = mapped_column(String, nullable=True)

    # Stores the timestamp for the creation of the assignment.
    created: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # Stores the timestamp for the last time the assignment was updated.
    modified: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    @classmethod
    def from_draft_model(cls, overview: HiringAssignmentDraft) -> Self:
        return cls(
            id=overview.id,
            user_id=overview.user_id,
            term_id=overview.term_id,
            course_site_id=overview.course_site_id,
            application_review_id=overview.application_review_id,
            hiring_level_id=overview.level.id,
            status=overview.status,
            position_number=overview.position_number,
            epar=overview.epar,
            i9=overview.i9,
            notes=overview.notes,
            created=overview.created,
            modified=overview.modified,
        )

    def to_overview_model(self) -> HiringAssignmentOverview:
        return HiringAssignmentOverview(
            id=self.id,
            user=self.user.to_public_model(),
            level=self.hiring_level.to_model(),
            status=self.status,
            position_number=self.position_number,
            epar=self.epar,
            i9=self.i9,
            notes=self.notes,
        )

    def to_summary_overview_model(self) -> HiringAssignmentSummaryOverview:
        sections = self.course_site.sections
        instructors: list[str] = []
        for section in sections:
            instructors += [
                staff.user.first_name + " " + staff.user.last_name
                for staff in section.staff
                if staff.member_role == RosterRole.INSTRUCTOR
            ]

        return HiringAssignmentSummaryOverview(
            id=self.id,
            application_review_id=self.application_review_id,
            course_site_id=self.course_site_id,
            user=self.user.to_public_model(),
            instructors=", ".join(map(str, list(set(instructors)))),
            level=self.hiring_level.to_model(),
            status=self.status,
            position_number=self.position_number,
            epar=self.epar,
            i9=self.i9,
            notes=self.notes,
        )

    def to_csv_row(self) -> HiringAssignmentCsvRow:
        sections = self.course_site.sections
        instructors: list[str] = []
        for section in sections:
            instructors += [
                staff.user.first_name + " " + staff.user.last_name
                for staff in section.staff
                if staff.member_role == RosterRole.INSTRUCTOR
            ]

        return HiringAssignmentCsvRow(
            first_name=self.user.first_name,
            last_name=self.user.last_name,
            onyen=self.user.onyen,
            pid=str(self.user.pid),
            email=self.user.email,
            instructors=", ".join(map(str, list(set(instructors)))),
            epar=self.epar,
            position_number=self.position_number,
            i9=self.i9,
            notes=self.notes,
            status=self.status,
            level_title=self.hiring_level.title,
            level_load=str(self.hiring_level.load),
            level_salary=str(self.hiring_level.salary),
        )
