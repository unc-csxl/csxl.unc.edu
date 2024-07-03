"""
Service for hiring.
"""

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from ..database import db_session
from ..models.user import User
from ..models.academics.section_member import RosterRole
from ..entities.academics.section_entity import SectionEntity
from ..entities.office_hours import CourseSiteEntity
from ..entities.application_entity import UTAApplicationEntity
from ..entities.academics.section_member_entity import SectionMemberEntity
from ..entities.application_review_entity import ApplicationReviewEntity
from .exceptions import CoursePermissionException, ResourceNotFoundException

from ..models.application_review import (
    HiringStatus,
    ApplicationReview,
    ApplicationReviewOverview,
    ApplicationReviewStatus,
)

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class HiringService:
    """
    Service that performs all actions for hiring.
    """

    def __init__(self, session: Session = Depends(db_session)):
        """
        Initializes the database session.
        """
        self._session = session

    def get_status(self, subject: User, course_site_id: int) -> HiringStatus:
        """
        Loads the applications and the current state of hiring for a course site,
        separated into columns.

        Returns:
            HiringStatus
        """
        # Step 1: Ensure that a user can access a course site's hiring.
        site_entity = self._load_instructor_course_site(subject, course_site_id)

        # Step 2: Find all applicants for sections in a given course site.
        applications: list[UTAApplicationEntity] = []
        for section in site_entity.sections:
            applications += section.preferred_applicants

        # Step 3: Process reviews.
        not_preferred_applications: list[ApplicationReviewEntity] = []
        not_processed_applications: list[ApplicationReviewEntity] = []
        preferred_applications: list[ApplicationReviewEntity] = []

        for review in site_entity.application_reviews:
            if review.status == ApplicationReviewStatus.NOT_PREFERRED:
                not_preferred_applications.append(review)
            if review.status == ApplicationReviewStatus.NOT_PROCESSED:
                not_processed_applications.append(review)
            if review.status == ApplicationReviewStatus.PREFERRED:
                preferred_applications.append(review)

        # Step 4: Find applications with no reviews.
        applications_missing_review: list[UTAApplicationEntity] = []

        for application in applications:
            # Check if the application is missing reviews
            if len(application.reviews) == 0:
                applications_missing_review.append(application)

        # Step 4: Create reviews for applications missing reviews, if any.
        preference_to_use = (
            (max([review.preference for review in not_processed_applications]) + 1)
            if len(not_processed_applications) > 0
            else 0
        )

        for application in applications_missing_review:
            review = ApplicationReview(
                application_id=application.id,
                course_site_id=course_site_id,
                preference=preference_to_use,
                notes="",
            )
            review_entity = ApplicationReviewEntity.from_model(review)
            self._session.add(review_entity)
            preference_to_use += 1
            not_processed_applications.append(review_entity)

        self._session.commit()

        # Step 5: Create review overview objects
        not_preferred_overviews: list[ApplicationReviewOverview] = [
            review.to_overview_model() for review in not_preferred_applications
        ]
        not_processed_overviews: list[ApplicationReviewOverview] = [
            review.to_overview_model() for review in not_processed_applications
        ]
        preferred_overviews: list[ApplicationReviewOverview] = [
            review.to_overview_model() for review in preferred_applications
        ]

        # Step 6: Create hiring status object and return
        hiring_status = HiringStatus(
            not_preferred=not_preferred_overviews,
            not_processed=not_processed_overviews,
            preferred=preferred_overviews,
        )

        # Step 7: Return
        return hiring_status

    def _load_instructor_course_site(
        self, subject: User, course_site_id: int
    ) -> CourseSiteEntity:
        """
        Loads a course site given a subject and course site ID.
        Ensures that a subject is an instructor for all of the courses in a course site.

        Throws:
          CoursePermissionException

        Returns:
            CourseSiteEntity
        """
        site_query = (
            select(CourseSiteEntity)
            .where(CourseSiteEntity.id == course_site_id)
            .options(
                joinedload(CourseSiteEntity.sections)
                .joinedload(SectionEntity.preferred_applicants)
                .joinedload(UTAApplicationEntity.user),
                joinedload(CourseSiteEntity.application_reviews),
            )
        )

        # Attempt to load a site.
        site_entity = self._session.scalars(site_query).unique().one_or_none()

        # Throw error if the site is not retrieved
        if site_entity is None:
            raise ResourceNotFoundException(
                f"No course site exists for id: {course_site_id}"
            )

        # Check permissions
        for section in site_entity.sections:
            roles = [
                member
                for member in section.members
                if member.user_id == subject.id
                and member.member_role == RosterRole.INSTRUCTOR
            ]
            if len(roles) < 1:
                raise CoursePermissionException(
                    f"You are not the instructor for a course site with ID: {course_site_id}"
                )

        # Return the site
        return site_entity
