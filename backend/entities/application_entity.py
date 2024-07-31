"""Definition of SQLAlchemy table-backed object mapping entity for Applications."""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    Enum as SQLAlchemyEnum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.entities.section_application_table import section_application_table
from backend.entities.user_entity import UserEntity
from backend.entities.academics.section_entity import SectionEntity
from backend.models.academics.section import Section

from .entity_base import EntityBase
from typing import Self, Dict
from ..models.application import Application
from ..models.comp_227 import Comp227

from ..models.application import ApplicationOverview

__authors__ = ["Ben Goulet, Abdulaziz Al-Shayef", "Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class ApplicationEntity(EntityBase):
    """Serves as the database model schema for the shape of the `Application` table"""

    # Name for the applications table
    __tablename__ = "application"

    # Unique ID for the application
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # The user associated with the application
    # NOTE: This field establishes a one-to-many relationship between the user and application tables.
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["UserEntity"] = relationship(back_populates="applications")

    # The term associated with the application
    # NOTE: This field establishes a one-to-many relationship between the term and application tables.
    term_id: Mapped[str] = mapped_column(ForeignKey("academics__term.id"))
    term: Mapped["TermEntity"] = relationship(back_populates="applications")

    # Review associated with the application
    # NOTE: This field establishes a one-to-many relationship between the review and application tables.
    reviews: Mapped[list["ApplicationReviewEntity"]] = relationship(
        back_populates="application", cascade="all,delete"
    )

    # Application properties (columns in the database table) specific to UTA Applications

    # Academic Hours student plans to take
    academic_hours: Mapped[int] = mapped_column(Integer, nullable=True)

    # Extracurriculars student is a part of
    extracurriculars: Mapped[str] = mapped_column(String, nullable=True)

    # Expected graduation
    expected_graduation: Mapped[str] = mapped_column(String, nullable=True)

    # Program pursued
    program_pursued: Mapped[str] = mapped_column(String, nullable=True)

    # Other programs being pursued
    other_programs: Mapped[str] = mapped_column(String, nullable=True)

    # GPA
    gpa: Mapped[float] = mapped_column(Float, nullable=True)

    # COMP GPA
    comp_gpa: Mapped[float] = mapped_column(Float, nullable=True)

    # Do they want to do this as COMP 227?
    comp_227: Mapped[Comp227] = mapped_column(SQLAlchemyEnum(Comp227), nullable=True)

    # Application properties (columns in the database table) specific to First-Time UTA Applications

    # Intro video explaining why they want to be a TA
    intro_video_url: Mapped[str] = mapped_column(String, nullable=True)

    # Prior experience in the workforce
    prior_experience: Mapped[str] = mapped_column(String, nullable=True)

    # Service experience such as volunteering/workforce
    service_experience: Mapped[str] = mapped_column(String, nullable=True)

    # Additonal experience that is relevant
    additional_experience: Mapped[str] = mapped_column(String, nullable=True)

    # TA Experience and what they have gotten out of it
    ta_experience: Mapped[str] = mapped_column(String, nullable=True)

    # Best student interaction/moment
    best_moment: Mapped[str] = mapped_column(String, nullable=True)

    # Desired personal improvement
    desired_improvement: Mapped[str] = mapped_column(String, nullable=True)

    # Application properties specific to GTA Applications

    # Desired personal improvement
    advisor: Mapped[str] = mapped_column(String, nullable=True)

    type = Column(String(50))

    # Sections student prefers
    preferred_sections: Mapped[list["SectionEntity"]] = relationship(
        "SectionEntity",
        secondary=section_application_table,
        back_populates="preferred_applicants",
        order_by=section_application_table.c.preference,
    )

    @classmethod
    def from_model(cls, model: Application) -> Self:
        """
        This method creates an application entity from the application model.
        """
        return cls(
            id=model.id,
            user_id=model.user_id,
            term_id=model.term_id,
            type=model.type,
            academic_hours=model.academic_hours,
            extracurriculars=model.extracurriculars,
            expected_graduation=model.expected_graduation,
            program_pursued=model.program_pursued,
            other_programs=model.other_programs,
            gpa=model.gpa,
            comp_gpa=model.comp_gpa,
            comp_227=model.comp_227,
            intro_video_url=model.intro_video_url,
            prior_experience=model.prior_experience,
            service_experience=model.service_experience,
            additional_experience=model.additional_experience,
            ta_experience=model.ta_experience,
            best_moment=model.best_moment,
            desired_improvement=model.desired_improvement,
            advisor=model.advisor,
        )

    def to_model(self) -> Application:
        """
        This method converts an application into an application.
        """
        return Application(
            id=self.id,
            user_id=self.user_id,
            term_id=self.term_id,
            type=self.type,
            academic_hours=self.academic_hours,
            extracurriculars=self.extracurriculars,
            expected_graduation=self.expected_graduation,
            program_pursued=self.program_pursued,
            other_programs=self.other_programs,
            gpa=self.gpa,
            comp_gpa=self.comp_gpa,
            comp_227=self.comp_227,
            intro_video_url=self.intro_video_url,
            prior_experience=self.prior_experience,
            service_experience=self.service_experience,
            additional_experience=self.additional_experience,
            ta_experience=self.ta_experience,
            best_moment=self.best_moment,
            desired_improvement=self.desired_improvement,
            advisor=self.advisor,
            preferred_sections=[
                section.to_catalog_identity_model()
                for section in self.preferred_sections
            ],
        )

    def to_overview_model(self) -> ApplicationOverview:
        """
        This method converts an application into an application overview.
        """
        return ApplicationOverview(
            applicant_name=f"{self.user.first_name} {self.user.last_name}",
            type=self.type,
            academic_hours=self.academic_hours,
            extracurriculars=self.extracurriculars,
            expected_graduation=self.expected_graduation,
            program_pursued=self.program_pursued,
            other_programs=self.other_programs,
            gpa=self.gpa,
            comp_gpa=self.comp_gpa,
            comp_227=self.comp_227,
            intro_video_url=self.intro_video_url,
            prior_experience=self.prior_experience,
            service_experience=self.service_experience,
            additional_experience=self.additional_experience,
            ta_experience=self.ta_experience,
            best_moment=self.best_moment,
            desired_improvement=self.desired_improvement,
            advisor=self.advisor,
            preferred_sections=[
                section.to_catalog_identity_model()
                for section in self.preferred_sections
            ],
        )
