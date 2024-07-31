"""
Service for hiring.
"""

from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.orm import Session, joinedload, with_polymorphic, selectinload
from ...database import db_session
from ..permission import PermissionService
from ...models.user import User
from ...models.academics.section_member import RosterRole
from ...entities.academics.section_entity import SectionEntity
from ...entities.office_hours import CourseSiteEntity
from ...entities.academics.section_member_entity import SectionMemberEntity
from ...entities.application_entity import ApplicationEntity
from ...entities.academics.hiring.application_review_entity import (
    ApplicationReviewEntity,
)
from ...entities.section_application_table import section_application_table
from ..exceptions import CoursePermissionException, ResourceNotFoundException

from ...models.academics.hiring.application_review import (
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

    def __init__(
        self,
        session: Session = Depends(db_session),
        permission_svc: PermissionService = Depends(),
    ):
        """
        Initializes the database session.
        """
        self._session = session
        self._permission_svc = permission_svc

    def get_status(self, subject: User, course_site_id: int) -> HiringStatus:
        """
        Loads the applications and the current state of hiring for a course site,
        separated into columns.

        Returns:
            HiringStatus
        """
        # Step 0: Load a Course Site
        site_entity = self._load_course_site(course_site_id)

        # Step 1: Ensure that a user can access a course site's hiring.
        if not self._is_instructor(subject, site_entity):
            self._permission_svc.enforce(
                subject, "hiring.get_status", f"course_site/{course_site_id}"
            )

        # Step 2: Ensure all applications have an application_review entity.
        self._create_missing_reviews(site_entity)

        # Step 2: Find all applicants for sections in a given course site.
        applications: list[ApplicationEntity] = []
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
        applications_missing_review: list[ApplicationEntity] = []

        for application in applications:
            # Check if the application is missing reviews
            reviews_course_site_ids = [
                review.course_site_id for review in application.reviews
            ]
            if course_site_id not in reviews_course_site_ids:
                applications_missing_review.append(application)

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
            not_preferred=sorted(not_preferred_overviews, key=lambda o: o.preference),
            not_processed=sorted(not_processed_overviews, key=lambda o: o.preference),
            preferred=sorted(preferred_overviews, key=lambda o: o.preference),
        )

        # Step 7: Return
        return hiring_status

    def update_status(
        self, subject: User, course_site_id: int, hiring_status: HiringStatus
    ) -> HiringStatus:
        """
        Updates the status of hiring for a course site based on the object passed in.

        Returns:
            HiringStatus
        """
        # Step 1: Ensure that a user can access a course site's hiring.
        site_entity = self._load_instructor_course_site(subject, course_site_id)

        # Step 2: Update the values for all reviews.

        # Retrieve all reviews, indexed by ID for efficient searching.
        hiring_status_reviews_by_id: dict[int, ApplicationReviewOverview] = {}
        for review_overview in hiring_status.not_preferred:
            hiring_status_reviews_by_id[review_overview.id] = review_overview
        for review_overview in hiring_status.not_processed:
            hiring_status_reviews_by_id[review_overview.id] = review_overview
        for review_overview in hiring_status.preferred:
            hiring_status_reviews_by_id[review_overview.id] = review_overview

        # Update every application associated with the site.
        for review in site_entity.application_reviews:
            new_review = hiring_status_reviews_by_id[review.id]
            review.status = new_review.status
            review.preference = new_review.preference
            review.notes = new_review.notes

        self._session.commit()

        # Reload the data and return the hiring status.
        return self.get_status(subject, course_site_id)

    def _load_course_site(self, course_site_id: int) -> CourseSiteEntity:
        """
        Loads a course site given a subject and course site ID.

        Returns:
            CourseSiteEntity | None

        Raises:
            ResourceNotFoundException when the course site does not exist.
        """
        site_query = select(CourseSiteEntity).where(
            CourseSiteEntity.id == course_site_id
        )
        site_entity: CourseSiteEntity | None = self._session.scalar(site_query)

        if site_entity is None:
            raise ResourceNotFoundException(
                f"No course site exists for id: {course_site_id}"
            )

        # Return the site
        return site_entity

    def _is_instructor(self, subject: User, course_site: CourseSiteEntity) -> bool:
        """
        Checks if the given user is an instructor for the specified course site.

        Args:
            subject (User): The user to check.
            course_site (CourseSiteEntity): The course site to check against.

        Returns:
            bool: True if the user is an instructor, False otherwise.

        """
        membership_query = (
            select(SectionMemberEntity)
            .where(SectionMemberEntity.user_id == subject.id)
            .where(
                SectionMemberEntity.section_id.in_(
                    select(SectionEntity.id).where(
                        SectionEntity.course_site_id == course_site.id
                    )
                )
            )
            .where(SectionMemberEntity.member_role == RosterRole.INSTRUCTOR)
        )
        return self._session.scalars(membership_query).first() is not None

    def _create_missing_reviews(self, site: CourseSiteEntity) -> None:
        need_review: list[int] = self._select_application_ids_without_reviews(site)

        preference: int = self._count_unprocessed(site)
        if len(need_review) > 0:
            for application_id in need_review:
                preference += 1
                review = ApplicationReviewEntity(
                    application_id=application_id,
                    course_site_id=site.id,
                    status=ApplicationReviewStatus.NOT_PROCESSED,
                    preference=preference,
                    notes="",
                )
                self._session.add(review)
            self._session.commit()

    def _count_unprocessed(self, course_site: CourseSiteEntity) -> int:
        """
        Returns the maximum preference value for unprocessed applications.

        Args:
            course_site (CourseSiteEntity): The course site to check against.

        Returns:
            int: The maximum preference value for unprocessed applications.
        """
        count_unprocessed = (
            select(func.count(ApplicationReviewEntity.preference))
            .where(ApplicationReviewEntity.course_site_id == course_site.id)
            .where(
                ApplicationReviewEntity.status == ApplicationReviewStatus.NOT_PROCESSED
            )
        )
        return self._session.scalar(count_unprocessed) or 0

    def _select_application_ids_without_reviews(
        self, course_site: CourseSiteEntity
    ) -> list[int]:
        """
        Returns a list of application IDs that do not have a review for a given course site.

        Args:
            course_site (CourseSiteEntity): The course site to check against.

        Returns:
            list[int]: A list of application IDs that do not have a review for the course site.
        """
        application_ids = (
            select(section_application_table.c.application_id)
            .where(
                section_application_table.c.section_id.in_(
                    select(SectionEntity.id).where(
                        SectionEntity.course_site_id == course_site.id
                    )
                )
            )
            .where(
                section_application_table.c.application_id.notin_(
                    select(ApplicationReviewEntity.application_id).where(
                        ApplicationReviewEntity.course_site_id == course_site.id
                    )
                )
            )
        )
        return list(self._session.scalars(application_ids).all())
