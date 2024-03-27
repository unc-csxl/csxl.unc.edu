"""Definition of SQLAlchemy table-backed object mapping entity for Course Sections."""

from typing import Self
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


from ..entity_base import EntityBase
from ...models.academics import Section
from ...models.academics import SectionDetails

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class SectionEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Section` table"""

    # Name for the course section table in the PostgreSQL database
    __tablename__ = "academics__section"

    # Section properties (columns in the database table)

    # Unique ID for the section
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Course the section is for
    # NOTE: This defines a one-to-many relationship between the course and sections tables.
    course_id: Mapped[str] = mapped_column(ForeignKey("academics__course.id"))
    course: Mapped["CourseEntity"] = relationship(back_populates="sections")

    # Number of the section (for example, COMP 100-003's code would be "003")
    number: Mapped[str] = mapped_column(String, default="")

    # Term the section is in
    # NOTE: This defines a one-to-many relationship between the term and sections tables.
    term_id: Mapped[str] = mapped_column(ForeignKey("academics__term.id"))
    term: Mapped["TermEntity"] = relationship(back_populates="course_sections")

    # Meeting pattern of the course
    # For example, MWF 4:40PM - 5:30PM.
    meeting_pattern: Mapped[str] = mapped_column(String, default="")

    # Override fields for specific sections, such as COMP 590: Special Topics
    override_title: Mapped[str] = mapped_column(String, default="")
    override_description: Mapped[str] = mapped_column(String, default="")

    # Room the section is in
    # NOTE: This defines a one-to-many relationship between the room and sections tables.
    rooms: Mapped[list["SectionRoomEntity"]] = relationship(
        back_populates="section", cascade="delete"
    )

    lecture_rooms: Mapped[list["SectionRoomEntity"]] = relationship(
        back_populates="section",
        viewonly=True,
        primaryjoin="and_(SectionEntity.id==SectionRoomEntity.section_id, SectionRoomEntity.assignment_type=='LECTURE_ROOM')",
    )

    office_hour_rooms: Mapped[list["SectionRoomEntity"]] = relationship(
        back_populates="section",
        viewonly=True,
        primaryjoin="and_(SectionEntity.id==SectionRoomEntity.section_id, SectionRoomEntity.assignment_type=='OFFICE_HOURS')",
    )

    # Members of the course
    members: Mapped[list["SectionMemberEntity"]] = relationship(
        back_populates="section",
    )

    # Relationship subset of members queries for non-students
    staff: Mapped[list["SectionMemberEntity"]] = relationship(
        back_populates="section",
        viewonly=True,
        primaryjoin="and_(SectionEntity.id==SectionMemberEntity.section_id, SectionMemberEntity.member_role!='STUDENT')",
    )

    # Optional office hours section ID
    office_hours_id: Mapped[int] = mapped_column(
        ForeignKey("office_hours__section.id"), nullable=True
    )
    office_hours_section: Mapped["OfficeHoursSectionEntity"] = relationship(
        back_populates="sections"
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
            override_title=model.override_title,
            override_description=model.override_description,
        )

    def to_model(self) -> Section:
        """
        Converts a `SectionEntity` object into a `Section` model object

        Returns:
            Section: `Section` object from the entity
        """

        return Section(
            id=self.id,
            course_id=self.course_id,
            number=self.number,
            term_id=self.term_id,
            meeting_pattern=self.meeting_pattern,
            lecture_room=(
                self.lecture_rooms[0].room.to_model()
                if len(self.lecture_rooms) > 0
                else None
            ),
            office_hour_rooms=[room.to_model() for room in self.office_hour_rooms],
            staff=[members.to_flat_model() for members in self.staff],
            override_title=self.override_title,
            override_description=self.override_description,
        )

    def to_details_model(self) -> SectionDetails:
        """
        Converts a `SectionEntity` object into a `SectionDetails` model object

        Returns:
            SectionDetails: `SectionDetails` object from the entity
        """

        section = self.to_model()

        return SectionDetails(
            id=self.id,
            course_id=self.course_id,
            course=self.course.to_model(),
            number=self.number,
            term_id=self.term_id,
            term=self.term.to_model(),
            meeting_pattern=self.meeting_pattern,
            lecture_room=section.lecture_room,
            office_hour_rooms=section.office_hour_rooms,
            staff=section.staff,
            override_title=self.override_title,
            override_description=self.override_description,
            office_hours_section=self.office_hours_section.to_model(),
        )
