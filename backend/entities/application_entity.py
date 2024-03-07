"""Definition of SQLAlchemy table-backed object mapping entity for Applications."""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .entity_base import EntityBase
from .section_application_table import section_application_table
from typing import Self
from ..models.application import Application

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

    # Sections TA'd for, reference to section_member
    previous_sections: Mapped[list["SectionEntity"]] = relationship(
        back_populates="tas"
    )

    # Set up for single-table inheritance (assign unique polymorphic identity)
    type = Column(String(50))
    __mapper_args__ = {
        'polymorphic_identity':'application',
        'polymorphic_on':type
    }

    ### Still need to setup models and classmethods.

    @classmethod
    def from_model(cls, model: Application) -> Self:
        """
        Class method that converts an `Application` model into a `ApplicationEntity`

        Parameters:
            - model (Application): Model to convert into an entity
        Returns:
            ApplicationEntity: Entity created from model
        """
        return cls(id=model.id)

    def to_model(self) -> Application:
        """
        Converts an `ApplicationEntity` object into an `Application` model object

        Returns:
            Application: `Application` object from the entity
        """
        return Application(id=self.id)

class UTA(Application):
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


class New_UTA(UTA):
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

class Returning_UTA(UTA):
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
