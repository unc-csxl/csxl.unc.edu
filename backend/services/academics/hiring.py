"""
Service for hiring.
"""

from itertools import groupby
from operator import attrgetter
from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.orm import Session, joinedload, with_polymorphic, selectinload
from ...database import db_session
from ..permission import PermissionService
from ...models.user import User
from ...models.academics.section_member import RosterRole
from ...models.application import ApplicationUnderReview
from ...entities.user_entity import UserEntity
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

        # Step 3: Load all reviews for the course site.
        review_models: list[ApplicationReviewOverview] = self._to_review_models(
            site_entity
        )

        # Step 4: Return the hiring status model
        return self._hiring_status_model(review_models)

    def update_status(
        self, subject: User, course_site_id: int, hiring_status: HiringStatus
    ) -> HiringStatus:
        """
        Updates the status of hiring for a course site based on the object passed in.

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

    def _load_application_reviews(
        self, course_site: CourseSiteEntity
    ) -> list[ApplicationReviewEntity]:
        """
        Loads all application reviews for a given course site.

        Args:
            course_site (CourseSiteEntity): The course site to check against.

        Returns:
            list[ApplicationReviewEntity]: A list of application reviews for the course site.
        """
        reviews_query = select(ApplicationReviewEntity).where(
            ApplicationReviewEntity.course_site_id == course_site.id
        )
        return list(self._session.scalars(reviews_query).all())

    def _load_applications(
        self, reviews: list[ApplicationReviewEntity]
    ) -> dict[int, ApplicationEntity]:
        """
        Loads all applications for a given course site.

        Args:
            course_site (CourseSiteEntity): The course site to check against.

        Returns:
            list[ApplicationEntity]: A list of applications for the course site.
        """
        applications_query = select(ApplicationEntity).where(
            ApplicationEntity.id.in_([review.application_id for review in reviews])
        )
        # Use a dict comprehension to map application IDs to application entities.
        return {app.id: app for app in self._session.scalars(applications_query).all()}

    def _load_applicants(
        self, applications: dict[int, ApplicationEntity]
    ) -> dict[int, UserEntity]:
        """
        Loads all applicants for a given course site.

        Args:
            applications (dict[int, ApplicationEntity]): A dictionary of application IDs to application entities.

        Returns:
            dict[int, User]: A dictionary of applicant IDs to applicant entities.
        """
        applicant_ids = {app.user_id for app in applications.values()}
        applicants_query = select(UserEntity).where(UserEntity.id.in_(applicant_ids))
        # Use a dict comprehension to map applicant IDs to applicant entities.
        return {
            applicant.id: applicant
            for applicant in self._session.scalars(applicants_query).all()
        }

    def _load_application_preferences(
        self, site: CourseSiteEntity, applications: dict[int, ApplicationEntity]
    ) -> dict[int, int]:
        """
        Loads all application preferences for a given course site.

        Args:
            applications (dict[int, ApplicationEntity]): A dictionary of application IDs to application entities.

        Returns:
            dict[int, int]: A dictionary of application IDs to application preferences.
        """
        preferences_query = (
            select(
                section_application_table.c.application_id,
                func.min(section_application_table.c.preference),
            )
            .where(section_application_table.c.application_id.in_(applications.keys()))
            .where(
                section_application_table.c.section_id.in_(
                    [section.id for section in site.sections]
                )
            )
            .group_by(section_application_table.c.application_id)
        )
        result = self._session.execute(preferences_query)
        return {row[0]: row[1] + 1 for row in result}

    def _to_review_models(
        self,
        site_entity: CourseSiteEntity,
    ) -> list[ApplicationReviewOverview]:
        """
        Converts a list of application reviews into a list of review models.

        Args:
            reviews (list[ApplicationReviewEntity]): A list of application reviews.
            applications (dict[int, ApplicationEntity]): A dictionary of application IDs to application entities.
            applicants (dict[int, UserEntity]): A dictionary of applicant IDs to applicant entities.
            applicant_preferences (dict[int, int]): A dictionary of application IDs to application preferences.

        Returns:
            list[ApplicationReviewOverview]: A list of review models.
        """
        application_reviews = self._load_application_reviews(site_entity)
        applications = self._load_applications(application_reviews)
        applicants = self._load_applicants(applications)
        applicant_preferences = self._load_application_preferences(
            site_entity, applications
        )
        return [
            ApplicationReviewOverview(
                id=review.id,
                course_site_id=review.course_site_id,
                application_id=review.application_id,
                application=self._application_model(
                    applications[review.application_id],
                    applicants[applications[review.application_id].user_id],
                ),
                status=review.status,
                preference=review.preference,
                notes=review.notes,
                applicant_course_ranking=applicant_preferences.get(
                    review.application_id, 999
                ),
            )
            for review in application_reviews
        ]

    def _application_model(
        self, application: ApplicationEntity, applicant: UserEntity
    ) -> ApplicationUnderReview:
        """
        Converts an application entity into an application model.

        Args:
            application (ApplicationEntity): The application entity to convert.
            applicant (UserEntity): The applicant entity to convert.

        Returns:
            ApplicationUnderReview: The application model.
        """
        return ApplicationUnderReview(
            id=application.id,
            type=str(application.type),
            applicant=applicant.to_public_model(),
            applicant_name=applicant.first_name + " " + applicant.last_name,
            academic_hours=application.academic_hours,
            extracurriculars=application.extracurriculars,
            expected_graduation=application.expected_graduation,
            program_pursued=application.program_pursued,
            other_programs=application.other_programs,
            gpa=application.gpa,
            comp_gpa=application.comp_gpa,
            comp_227=application.comp_227,
            intro_video_url=application.intro_video_url,
            prior_experience=application.prior_experience,
            service_experience=application.service_experience,
            additional_experience=application.additional_experience,
            ta_experience=application.ta_experience,
            best_moment=application.best_moment,
            desired_improvement=application.desired_improvement,
            advisor=application.advisor,
        )

    def _hiring_status_model(
        self, review_models: list[ApplicationReviewOverview]
    ) -> HiringStatus:
        """
        Converts a list of review models into a hiring status model.

        Args:
            review_models (list[ApplicationReviewOverview]): A list of review models.

        Returns:
            HiringStatus: The hiring status model.
        """
        # Group by status
        review_models.sort(key=lambda review: str(review.status))
        status_groups = groupby(review_models, key=attrgetter("status"))
        grouped_items = {key: list(group) for key, group in status_groups}

        # Sort by preference
        for status in [
            ApplicationReviewStatus.NOT_PREFERRED,
            ApplicationReviewStatus.PREFERRED,
            ApplicationReviewStatus.NOT_PROCESSED,
        ]:
            if status not in grouped_items:
                grouped_items[status] = []
            else:
                grouped_items[status].sort(key=attrgetter("preference"))

        # Return Grouped
        return HiringStatus(
            not_preferred=grouped_items[ApplicationReviewStatus.NOT_PREFERRED],
            not_processed=grouped_items[ApplicationReviewStatus.NOT_PROCESSED],
            preferred=grouped_items[ApplicationReviewStatus.PREFERRED],
        )
