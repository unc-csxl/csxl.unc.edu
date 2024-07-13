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
from backend.models.application_details import (
    ApplicationDetails,
    NewUTAApplicationDetails,
    UTAApplicationDetails,
)
from backend.models.academics.section import Section

from .entity_base import EntityBase
from typing import Self, Dict
from ..models.application import (
    Application,
    UTAApplication,
    NewUTAApplication,
    ReturningUTAApplication,
)
from ..models.application_details import UTAApplicationDetails

from ..models.comp_227 import Comp227

from ..models.academics.hiring.application_review import ApplicationOverview

__authors__ = ["Ben Goulet, Abdulaziz Al-Shayef"]
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
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["UserEntity"] = relationship(back_populates="applications")

    # Review associated with the application
    # NOTE: This field establishes a one-to-many relationship between the review and application tables.
    reviews: Mapped[list["ApplicationReviewEntity"]] = relationship(
        back_populates="application", cascade="all,delete"
    )

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
        )

    def to_details_model(self) -> ApplicationDetails:
        """
        Converts a `ApplicationEntity` object into a `ApplicationDetails` model object

        Returns:
            ApplicationDetails: `ApplicationDetails` object from the entity
        """
        return ApplicationDetails(
            id=self.id, user_id=self.user_id, user=self.user.to_model()
        )

    def to_overview_model(self) -> ApplicationOverview:
        """
        This method converts an application into an application overview.

        NOTE: This attempts to convert to an overview model that includes fields based
        on child object types. This may cause errors in the future.
        """
        return ApplicationOverview(
            applicant_name=f"{self.user.first_name} {self.user.last_name}",
            academic_hours=(
                self.academic_hours if isinstance(self, UTAApplicationEntity) else None
            ),
            extracurriculars=(
                self.extracurriculars
                if isinstance(self, UTAApplicationEntity)
                else None
            ),
            expected_graduation=(
                self.expected_graduation
                if isinstance(self, UTAApplicationEntity)
                else None
            ),
            program_pursued=(
                self.program_pursued if isinstance(self, UTAApplicationEntity) else None
            ),
            other_programs=(
                self.other_programs if isinstance(self, UTAApplicationEntity) else None
            ),
            gpa=self.gpa if isinstance(self, UTAApplicationEntity) else None,
            comp_gpa=self.comp_gpa if isinstance(self, UTAApplicationEntity) else None,
            comp_227=self.comp_227 if isinstance(self, UTAApplicationEntity) else None,
            intro_video_url=(
                self.intro_video_url
                if isinstance(self, NewUTAApplicationEntity)
                else None
            ),
            prior_experience=(
                self.prior_experience
                if isinstance(self, NewUTAApplicationEntity)
                else None
            ),
            service_experience=(
                self.service_experience
                if isinstance(self, NewUTAApplicationEntity)
                else None
            ),
            additional_experience=(
                self.additional_experience
                if isinstance(self, NewUTAApplicationEntity)
                else None
            ),
        )


class UTAApplicationEntity(ApplicationEntity):
    """Serves as the database model schema for applications specific to Undergraduate TA's"""

    # Application properties (columns in the database table) specific to UTA Applications

    # Academic Hours student plans to take
    academic_hours: Mapped[int] = mapped_column(Integer, nullable=False)

    # Extracurriculars student is a part of
    extracurriculars: Mapped[str] = mapped_column(String, nullable=True)

    # Expected graduation
    expected_graduation: Mapped[str] = mapped_column(String, nullable=False)

    # Program pursued
    program_pursued: Mapped[str] = mapped_column(String, nullable=False)

    # Other programs being pursued
    other_programs: Mapped[str] = mapped_column(String, nullable=True)

    # GPA
    gpa: Mapped[float] = mapped_column(Float, nullable=False)

    # COMP GPA
    comp_gpa: Mapped[float] = mapped_column(Float, nullable=True)

    # Do they want to do this as COMP 227?
    comp_227: Mapped[Comp227] = mapped_column(SQLAlchemyEnum(Comp227), nullable=True)

    # Sections student prefers
    preferred_sections: Mapped[list["SectionEntity"]] = relationship(
        "SectionEntity",
        secondary=section_application_table,
        back_populates="preferred_applicants",
    )

    # Any row in the main Application table that is an instance of UTAApplicationEntity will override
    # the polymorephic_identity to "uta"
    __mapper_args__ = {
        "polymorphic_identity": "uta",
    }

    @classmethod
    def from_model(cls, model: UTAApplicationDetails) -> Self:
        """
        Class method that converts a `UTA` model into a `UTAEntity`

        Parameters:
            - model (UTA): Model to convert into an entity
            - session (Session): Database session for querying existing sections
        Returns:
            UTAEntity: Entity created from model
        """

        entity = super().from_model(model)
        entity.academic_hours = model.academic_hours
        entity.extracurriculars = model.extracurriculars
        entity.expected_graduation = model.expected_graduation
        entity.program_pursued = model.program_pursued
        entity.other_programs = model.other_programs
        entity.gpa = model.gpa
        entity.comp_gpa = model.comp_gpa
        entity.comp_227 = model.comp_227
        entity.preferred_sections = [
            SectionEntity.from_model(section) for section in model.preferred_sections
        ]

        return entity

    def to_model(self) -> UTAApplication:
        """
        Converts an `ApplicationEntity` object into an `Application` model object

        Returns:
            Application: `Application` object from the entity
        """

        parent_model = super().to_model().model_dump()
        return UTAApplication(
            **parent_model,
            academic_hours=self.academic_hours,
            extracurriculars=self.extracurriculars,
            expected_graduation=self.expected_graduation,
            program_pursued=self.program_pursued,
            other_programs=self.other_programs,
            gpa=self.gpa,
            comp_gpa=self.comp_gpa,
            comp_227=self.comp_227,
        )

    def to_details_model(self) -> UTAApplicationDetails:
        """
        Converts a `ApplicationEntity` object into a `ApplicationDetails` model object

        Returns:
            ApplicationDetails: `ApplicationDetails` object from the entity
        """

        parent_model = super().to_details_model().model_dump()

        return UTAApplicationDetails(
            **parent_model,
            academic_hours=self.academic_hours,
            extracurriculars=self.extracurriculars,
            expected_graduation=self.expected_graduation,
            program_pursued=self.program_pursued,
            other_programs=self.other_programs,
            gpa=self.gpa,
            comp_gpa=self.comp_gpa,
            comp_227=self.comp_227,
            preferred_sections=[
                section.to_model() for section in self.preferred_sections
            ],
        )

    def update(
        self, model: UTAApplicationDetails, sections: list[SectionEntity]
    ) -> None:
        """
        Update an ApplciationEntity from a UTA model.

        Args:
            model (UTA): The model to update the entity from.

        Returns:
            None
        """
        self.academic_hours = model.academic_hours
        self.extracurriculars = model.extracurriculars
        self.expected_graduation = model.expected_graduation
        self.program_pursued = model.program_pursued
        self.other_programs = model.other_programs
        self.gpa = model.gpa
        self.comp_gpa = model.comp_gpa
        self.comp_227 = model.comp_227
        self.preferred_sections = sections


class NewUTAApplicationEntity(UTAApplicationEntity):
    """Serves as the database model schema for applications specific to new Undergraduate TA's"""

    # Application properties (columns in the database table) specific to First-Time UTA Applications

    # Intro video explaining why they want to be a TA
    intro_video_url: Mapped[str] = mapped_column(String, nullable=True)

    # Prior experience in the workforce
    prior_experience: Mapped[str] = mapped_column(String, nullable=True)

    # Service experience such as volunteering/workforce
    service_experience: Mapped[str] = mapped_column(String, nullable=True)

    # Additonal experience that is relevant
    additional_experience: Mapped[str] = mapped_column(String, nullable=True)

    # Any row in the main Application table that is an instance of NewUTAApplicationEntity will override
    # the polymorephic_identity to "new_uta"
    __mapper_args__ = {
        "polymorphic_identity": "new_uta",
    }

    @classmethod
    def from_model(cls, model: NewUTAApplicationDetails) -> Self:
        """
        Class method that converts an `Application` model into a `ApplicationEntity`

        Parameters:
            - model (Application): Model to convert into an entity
        Returns:
            ApplicationEntity: Entity created from model
        """

        entity = super().from_model(model)
        entity.intro_video_url = model.intro_video_url
        entity.prior_experience = model.prior_experience
        entity.service_experience = model.service_experience
        entity.additional_experience = model.additional_experience

        return entity

    def to_model(self) -> NewUTAApplication:
        """
        Converts an `ApplicationEntity` object into an `Application` model object

        Returns:
            Application: `Application` object from the entity
        """

        parent_model = super().to_details_model().model_dump()
        return NewUTAApplication(
            **parent_model,
            intro_video_url=self.intro_video_url,
            prior_experience=self.prior_experience,
            service_experience=self.service_experience,
            additional_experience=self.additional_experience,
        )

    def to_details_model(self) -> NewUTAApplicationDetails:
        """
        Converts a `ApplicationEntity` object into a `ApplicationDetails` model object

        Returns:
            ApplicationDetails: `ApplicationDetails` object from the entity
        """

        parent_model = super().to_details_model().model_dump()
        return NewUTAApplicationDetails(
            **parent_model,
            intro_video_url=self.intro_video_url,
            prior_experience=self.prior_experience,
            service_experience=self.service_experience,
            additional_experience=self.additional_experience,
        )

    def update(self, model: NewUTAApplicationDetails, sections: list[Section]) -> None:
        """
        Update an ApplicationEntity from a New_UTA model.

        Args:
            model (New_UTA): The model to update the entity from.

        Returns:
            None
        """

        super().update(model, sections)
        self.intro_video_url = model.intro_video_url
        self.prior_experience = model.prior_experience
        self.service_experience = model.service_experience
        self.additional_experience = model.additional_experience

    def map_application_to_detail_model(
        self, section_preferences: Dict[int, SectionEntity]
    ) -> NewUTAApplicationDetails:
        """Returns the correctly mapped application for a specific user

        Returns:
            New_UTADetails: Object that represents an application for a new UTA
        """
        return NewUTAApplicationDetails(
            id=self.id,
            user_id=self.user_id,
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
            user=self.user.to_model(),
            preferred_sections=[section for section in section_preferences.values()],
        )


class ReturningUTAApplicationEntity(UTAApplicationEntity):
    """Serves as the database model schema for applications specific to returning Undergraduate TA's"""

    # Application properties (columns in the database table) specific to Returning UTA Applications

    # TA Experience and what they have gotten out of it
    ta_experience: Mapped[str] = mapped_column(String, nullable=True)

    # Best student interaction/moment
    best_moment: Mapped[str] = mapped_column(String, nullable=True)

    # Desired personal improvement
    desired_improvement: Mapped[str] = mapped_column(String, nullable=True)

    # Any row in the main Application table that is an instance of ReturningUTAApplicationEntity will override
    # the polymorephic_identity to "returning_uta"
    __mapper_args__ = {
        "polymorphic_identity": "returning_uta",
    }

    @classmethod
    def from_model(cls, model: ReturningUTAApplication) -> Self:
        """
        Class method that converts an `Application` model into a `ApplicationEntity`

        Parameters:
            - model (Application): Model to convert into an entity
        Returns:
            ApplicationEntity: Entity created from model
        """

        entity = super().from_model(model)
        entity.ta_experience = model.ta_experience
        entity.best_moment = model.best_moment
        entity.desired_improvement = model.desired_improvement

        return entity

    def to_model(self) -> ReturningUTAApplication:
        """
        Converts an `ApplicationEntity` object into an `Application` model object

        Returns:
            Application: `Application` object from the entity
        """

        parent_model = super().to_model().model_dump()
        return ReturningUTAApplication(
            **parent_model,
            ta_experience=self.ta_experience,
            best_moment=self.best_moment,
            desired_improvement=self.desired_improvement,
        )
