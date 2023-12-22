"""Definition of SQLAlchemy table-backed object mapping entity for Course Sections."""

from typing import Self
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.room_assignment_type import RoomAssignmentType

from ..entity_base import EntityBase
from datetime import datetime
from ...models.courses import Section
from ...models.courses import SectionDetails
from ...models.courses.section_member import SectionMember
from ...models.roster_role import RosterRole

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class SectionEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Section` table"""

    # Name for the course section table in the PostgreSQL database
    __tablename__ = "courses__section"

    # Section properties (columns in the database table)

    # Unique ID for the section
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Course the section is for
    # NOTE: This defines a one-to-many relationship between the course and sections tables.
    course_id: Mapped[str] = mapped_column(ForeignKey("courses__course.id"))
    course: Mapped["CourseEntity"] = relationship(back_populates="sections")

    # Number of the section (for example, COMP 100-003's code would be "003")
    number: Mapped[str] = mapped_column(String, default="")

    # Term the section is in
    # NOTE: This defines a one-to-many relationship between the term and sections tables.
    term_id: Mapped[str] = mapped_column(ForeignKey("courses__term.id"))
    term: Mapped["TermEntity"] = relationship(back_populates="course_sections")

    # Meeting pattern of the course
    # For example, MWF 4:40PM - 5:30PM.
    meeting_pattern: Mapped[str] = mapped_column(String, default="")

    # Term the section is in
    # NOTE: This defines a one-to-many relationship between the term and sections tables.
    rooms: Mapped[list["SectionRoomEntity"]] = relationship(back_populates="section")

    # Members of the course
    members: Mapped[list["SectionMemberEntity"]] = relationship(
        back_populates="section"
    )

    @classmethod
    def from_model(cls, model: Section) -> Self:
        """
        Class method that converts a `Section` model into a `SectionEntity`

        Parameters:
            - model (Section): Model to convert into an entity
        Returns:
            SectionEntity: Entity created from model
        """
        return cls(
            id=model.id,
            course_id=model.course_id,
            number=model.number,
            term_id=model.term_id,
            meeting_pattern=model.meeting_pattern,
        )

    def to_model(self) -> Section:
        """
        Converts a `SectionEntity` object into a `Section` model object

        Returns:
            Section: `Section` object from the entity
        """
        lecture_rooms = [
            room.room.to_model()
            for room in self.rooms
            if room.assignment_type == RoomAssignmentType.LECTURE_ROOM
        ]
        office_hour_rooms = [
            room.room.to_model()
            for room in self.rooms
            if room.assignment_type == RoomAssignmentType.OFFICE_HOURS
        ]
        staff = [
            members.to_flat_model()
            for members in self.members
            if members.member_role != RosterRole.STUDENT
        ]

        return Section(
            id=self.id,
            course_id=self.course_id,
            number=self.number,
            term_id=self.term_id,
            meeting_pattern=self.meeting_pattern,
            lecture_room=(lecture_rooms[0] if len(lecture_rooms) > 0 else None),
            office_hour_rooms=office_hour_rooms,
            staff=[
                members.to_flat_model()
                for members in self.members
                if members.member_role != RosterRole.STUDENT
            ],
        )

    def to_details_model(self) -> SectionDetails:
        """
        Converts a `SectionEntity` object into a `SectionDetails` model object

        Returns:
            SectionDetails: `SectionDetails` object from the entity
        """
        lecture_rooms = [
            room.room.to_model()
            for room in self.rooms
            if room.assignment_type == RoomAssignmentType.LECTURE_ROOM
        ]
        office_hour_rooms = [
            room.room.to_model()
            for room in self.rooms
            if room.assignment_type == RoomAssignmentType.OFFICE_HOURS
        ]
        staff = [
            members.to_flat_model()
            for members in self.members
            if members.member_role != RosterRole.STUDENT
        ]

        return SectionDetails(
            id=self.id,
            course_id=self.course_id,
            course=self.course.to_model(),
            number=self.number,
            term_id=self.term_id,
            term=self.term.to_model(),
            meeting_pattern=self.meeting_pattern,
            lecture_room=(lecture_rooms[0] if len(lecture_rooms) > 0 else None),
            office_hour_rooms=office_hour_rooms,
            staff=staff,
        )