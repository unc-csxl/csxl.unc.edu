"""Definition of SQLAlchemy table-backed object mapping entity for Application Reviews."""

from sqlalchemy import Integer, String, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Self
from sqlalchemy import Enum as SQLAlchemyEnum
from itertools import groupby

from ...entity_base import EntityBase
from ....models.academics.hiring.application_review import (
    ApplicationReviewStatus,
    ApplicationReview,
    ApplicationReviewOverview,
)

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class ApplicationReviewEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `ApplicationReview` table"""

    # Name for the review table in the PostgreSQL database
    __tablename__ = "academics__hiring__application_review"

    __table_args__ = (
        Index(
            "academics__hiring__application_review_course_idx",
            "course_site_id",
            "status",
            "preference",
        ),
    )

    # Properties (columns in the database table)

    # Unique ID
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Application
    application_id: Mapped[int] = mapped_column(ForeignKey("application.id"))
    application: Mapped["ApplicationEntity"] = relationship(back_populates="reviews")
    # Application
    course_site_id: Mapped[int] = mapped_column(ForeignKey("course_site.id"))
    course_site: Mapped["CourseSiteEntity"] = relationship(
        back_populates="application_reviews"
    )

    # Status
    status: Mapped[ApplicationReviewStatus] = mapped_column(
        SQLAlchemyEnum(ApplicationReviewStatus),
        default=ApplicationReviewStatus.NOT_PROCESSED,
        nullable=False,
    )
    # Preference
    preference: Mapped[int] = mapped_column(Integer)
    # Notes
    notes: Mapped[str] = mapped_column(String)

    @classmethod
    def from_model(cls, model: ApplicationReview) -> Self:
        """
        Class method that converts an `ApplicationReview` model into a `ApplicationReviewEntity`

        Parameters:
            - model (ApplicationReview): Model to convert into an entity
        Returns:
            ApplicationReviewEntity: Entity created from model
        """
        return cls(
            id=model.id,
            application_id=model.application_id,
            course_site_id=model.course_site_id,
            status=model.status,
            preference=model.preference,
            notes=model.notes,
        )

    def to_overview_model(self) -> ApplicationReviewOverview:
        """
        Converts a `CourseSiteEntity` object into a `ApplicationReviewOverview` model object

        Returns:
            ApplicationReviewOverview: `ApplicationReviewOverview` object from the entity
        """
        # Determine the ranking of the applicant for a given course
        # 1. Find all of the applicant's preferred sections
        applicant_section_preferences = self.application.preferred_sections
        # 2. Find the course sites that the applicant's preferred sections are attached to.
        preferences_course_site_ids = [
            section.course_site_id for section in applicant_section_preferences
        ]
        # 3. Remove duplicates in the list above while preserving an ordering.
        #    (i.e., keep only the first occurrence of each ID)
        #    Note: Cannot just use a set since sets are unordered.
        found_course_site_ids = set()
        preferences_course_site_ids_no_duplicates = []
        for course_site_id in preferences_course_site_ids:
            if course_site_id not in found_course_site_ids:
                preferences_course_site_ids_no_duplicates.append(course_site_id)
                found_course_site_ids.add(course_site_id)

        # 3. Find the applicant's preference for the sections included in the course site by
        #    determining the first index where the course site ID occurs in the list above.
        #    Example:
        #    Assume a student applied to 110-001 --> 110-002 --> 210-001 --> 210-002 --> 301-001 --> 110-003
        #    Assume that the all COMP 110 sections are in course site ID #8, 210 in #7, and 301 in #6.
        #    Then, preferences_course_site_ids = [8, 8, 8, 7, 7, 6, 8]
        #    So, preferences_course_site_ids_no_duplicates = [8, 7, 6]
        #    Therefore, this is the user's preference order:
        #    1. Sections in course site 8 (COMP 110s)
        #    2. Sections in course site 7 (COMP 210s)
        #    3. Sections in course site 6 (COMP 301)
        applicant_preference_for_course = (
            preferences_course_site_ids_no_duplicates.index(
                self.course_site_id
            )  # Find the min index.
            # This case should never be reached, but it prevents an error if so.
            if self.course_site_id in preferences_course_site_ids_no_duplicates
            else -1
        )

        return ApplicationReviewOverview(
            id=self.id,
            application_id=self.application_id,
            course_site_id=self.course_site_id,
            status=self.status,
            preference=self.preference,
            notes=self.notes,
            application=self.application.to_overview_model(),
            applicant_course_ranking=applicant_preference_for_course,
        )
