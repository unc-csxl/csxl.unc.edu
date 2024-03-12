"""Definition of SQLAlchemy table-backed object mapping entity for Applications."""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.entities.user_entity import UserEntity
from .entity_base import EntityBase
from .section_application_table import section_application_table
from typing import Self
from ..models.application import Application, UTA, New_UTA, Returning_UTA

__authors__ = ["Ben Goulet"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class ApplicationEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Application` table"""

    # Name for the applications table in the PostgreSQL database
    __tablename__ = "application"

    # Unique ID for the application
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # The user associated with the application
    # NOTE: This field establishes a one-to-many relationship between the user and application tables.
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    user: Mapped["UserEntity"] = relationship(back_populates="applications")

    # Set up for single-table inheritance (assign unique polymorphic identity)
    type = Column(String(50))
    __mapper_args__ = {"polymorphic_identity": "application", "polymorphic_on": type}

    @classmethod
    def from_model(cls, model: Application) -> Self:
        """
        Class method that converts an `Application` model into a `ApplicationEntity`

        Parameters:
            - model (Application): Model to convert into an entity
        Returns:
            ApplicationEntity: Entity created from model
        """
        return cls(
            id=model.id,
            user_id=model.user_id,
            user=model.user,
            previous_sections=model.previous_sections,
        )

    def to_model(self) -> Application:
        """
        Converts an `ApplicationEntity` object into an `Application` model object

        Returns:
            Application: `Application` object from the entity
        """
        return Application(
            id=self.id,
            user_id=self.user_id,
            user=self.user,
            previous_sections=self.previous_sections,
        )


class UTAEntity(ApplicationEntity):
    """Serves as the database model schema for applications specific to Undergraduate TA's"""

    # Application properties (columns in the database table) specific to UTA Applications

    # Academic Hours student plans to take
    academic_hours: Mapped[int] = mapped_column(Integer, nullable=False)

    # Extracurriculars student is a part of
    extracurriculars: Mapped[str] = mapped_column(String, nullable=False)

    # Expected graduation
    expected_graduation: Mapped[str] = mapped_column(String, nullable=False)

    # Program pursued
    program_pursued: Mapped[str] = mapped_column(String, nullable=False)

    # Other programs being pursued
    other_programs: Mapped[str] = mapped_column(String, nullable=True)

    # GPA
    gpa: Mapped[str] = mapped_column(String, nullable=True)

    # COMP GPA
    comp_gpa: Mapped[str] = mapped_column(String, nullable=True)

    # Do they want to do this as COMP 227?
    comp_227: Mapped[bool] = mapped_column(Boolean, nullable=False)

    # Open pairing?
    open_pairing: Mapped[bool] = mapped_column(Boolean, nullable=False)

    # Sections student prefers
    preferred_courses: Mapped[list["SectionEntity"]] = relationship(
        secondary=section_application_table, back_populates="preferred_applicants"
    )

    # Sections student is eligible for
    eligible_courses: Mapped[list["SectionEntity"]] = relationship(
        secondary=section_application_table, back_populates="eligible_applicants"
    )

    __mapper_args__ = {
        "polymorphic_identity": "uta",
    }

    @classmethod
    def from_model(cls, model: UTA) -> Self:
        """
        Class method that converts an `Application` model into a `ApplicationEntity`

        Parameters:
            - model (Application): Model to convert into an entity
        Returns:
            ApplicationEntity: Entity created from model
        """
        return cls(
            academic_hours=model.academic_hours,
            extracurriculars=model.extracurriculars,
            expected_graduation=model.expected_graduation,
            program_pursued=model.program_pursued,
            other_programs=model.other_programs,
            gpa=model.gpa,
            comp_gpa=model.comp_gpa,
            comp_227=model.comp_227,
            open_pairing=model.open_pairing,
            preferred_courses=model.preferred_courses,
            eligible_courses=model.eligible_courses,
        )

    def to_model(self) -> UTA:
        """
        Converts an `ApplicationEntity` object into an `Application` model object

        Returns:
            Application: `Application` object from the entity
        """
        return UTA(
            academic_hours=self.academic_hours,
            extracurriculars=self.extracurriculars,
            expected_graduation=self.expected_graduation,
            program_pursued=self.program_pursued,
            other_programs=self.other_programs,
            gpa=self.gpa,
            comp_gpa=self.comp_gpa,
            comp_227=self.comp_227,
            open_pairing=self.open_pairing,
            preferred_courses=self.preferred_courses,
            eligible_courses=self.eligible_courses,
        )


class New_UTA_Entity(UTAEntity):
    """Serves as the database model schema for applications specific to new Undergraduate TA's"""

    # Application properties (columns in the database table) specific to First-Time UTA Applications

    # Intro video explaining why they want to be a TA
    intro_video: Mapped[str] = mapped_column(String, nullable=False)

    # Prior experience in the workforce
    prior_experience: Mapped[str] = mapped_column(String, nullable=False)

    # Service experience such as volunteering/workforce
    service_experience: Mapped[str] = mapped_column(String, nullable=False)

    # Additonal experience that is relevant
    additional_experience: Mapped[str] = mapped_column(
        String, nullable=False
    )  # maybe nullable = true?

    # Set up for single-table inheritance (assign unique polymorphic identity)
    __mapper_args__ = {
        "polymorphic_identity": "new_uta",
    }

    @classmethod
    def from_model(cls, model: New_UTA) -> Self:
        """
        Class method that converts an `Application` model into a `ApplicationEntity`

        Parameters:
            - model (Application): Model to convert into an entity
        Returns:
            ApplicationEntity: Entity created from model
        """
        return cls(
            intro_video=model.intro_video,
            prior_experience=model.prior_experience,
            service_experience=model.service_experience,
            additional_experience=model.additional_experience,
        )

    def to_model(self) -> New_UTA:
        """
        Converts an `ApplicationEntity` object into an `Application` model object

        Returns:
            Application: `Application` object from the entity
        """
        return New_UTA(
            intro_video=self.intro_video,
            prior_experience=self.prior_experience,
            service_experience=self.service_experience,
            additional_experience=self.additional_experience,
        )


class Returning_UTA_Entity(UTAEntity):
    """Serves as the database model schema for applications specific to returning Undergraduate TA's"""

    # Application properties (columns in the database table) specific to Returning UTA Applications

    # TA Experience and what they have gotten out of it
    ta_experience: Mapped[str] = mapped_column(String, nullable=False)

    # Best student interaction/moment
    best_moment: Mapped[str] = mapped_column(String, nullable=False)

    # Desired personal improvement
    desired_improvement: Mapped[str] = mapped_column(String, nullable=False)

    # Set up for single-table inheritance (assign unique polymorphic identity)
    __mapper_args__ = {
        "polymorphic_identity": "returning_uta",
    }

    @classmethod
    def from_model(cls, model: Returning_UTA) -> Self:
        """
        Class method that converts an `Application` model into a `ApplicationEntity`

        Parameters:
            - model (Application): Model to convert into an entity
        Returns:
            ApplicationEntity: Entity created from model
        """
        return cls(
            ta_experience=model.ta_experience,
            best_moment=model.best_moment,
            desired_improvement=model.desired_improvement,
        )

    def to_model(self) -> Returning_UTA:
        """
        Converts an `ApplicationEntity` object into an `Application` model object

        Returns:
            Application: `Application` object from the entity
        """
        return Returning_UTA(
            ta_experience=self.ta_experience,
            best_moment=self.best_moment,
            desired_improvement=self.desired_improvement,
        )
