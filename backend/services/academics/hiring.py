"""
Service for hiring.
"""

from fastapi import Depends
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, joinedload, with_polymorphic, selectinload

from backend.models.pagination import Paginated, PaginationParams
from ...database import db_session
from ...models.user import User
from ...models.academics.section_member import RosterRole
from ...entities import UserEntity
from ...entities.academics import SectionEntity, TermEntity
from ...entities.office_hours import CourseSiteEntity
from ...entities.academics.section_member_entity import SectionMemberEntity
from ...entities.application_entity import ApplicationEntity
from ...entities.academics.hiring.application_review_entity import (
    ApplicationReviewEntity,
)
from ...entities.academics.hiring.hiring_level_entity import HiringLevelEntity
from ...entities.academics.hiring.hiring_assignment_entity import HiringAssignmentEntity

from ..exceptions import CoursePermissionException, ResourceNotFoundException
from ...services import PermissionService
from ...models.academics.hiring.application_review import (
    HiringStatus,
    ApplicationReview,
    ApplicationReviewOverview,
    ApplicationReviewStatus,
)
from ...models.academics.hiring.hiring_assignment import *
from ...models.academics.hiring.hiring_level import *

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
        permission: PermissionService = Depends(),
    ):
        """
        Initializes the database session.
        """
        self._session = session
        self._permission = permission

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
                .joinedload(ApplicationEntity.user),
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

    # Hiring Admin Features

    def _calculate_coverage(
        self, enrollment: int, assignments: list[HiringAssignmentEntity]
    ) -> float:
        assignment_count_non_ior = len(
            [
                assignment
                for assignment in assignments
                if assignment.hiring_level.classification
                != HiringLevelClassification.IOR
            ]
        )
        coverage = (float(enrollment) / 60.0) - (float(assignment_count_non_ior) / 4.0)
        return coverage

    def get_hiring_admin_overview(
        self, subject: User, term_id: str
    ) -> HiringAdminOverview:
        """Get the overview for hiring during a given term for the site admin."""
        # 1. Check for hiring permissions.
        self._permission.enforce(subject, "hiring.admin", "*")
        # 2. Find the hiring information based on course sites for a given term
        course_site_query = (
            select(CourseSiteEntity)
            .join(CourseSiteEntity.term)
            .where(TermEntity.id == term_id)
            .options(
                joinedload(CourseSiteEntity.sections)
                .joinedload(SectionEntity.staff)
                .joinedload(SectionMemberEntity.user),
                joinedload(CourseSiteEntity.application_reviews)
                .joinedload(ApplicationReviewEntity.application)
                .joinedload(ApplicationEntity.user),
                joinedload(CourseSiteEntity.hiring_assignments),
            )
        )
        course_site_entities = self._session.scalars(course_site_query).unique().all()

        # 3. Assemble the overview models
        hiring_course_site_overviews: list[HiringCourseSiteOverview] = []
        for course_site_entity in course_site_entities:
            # Find all of the data for a course site overview
            section_entites = course_site_entity.sections
            sections = [
                section.to_catalog_identity_model() for section in section_entites
            ]
            instructors: list[PublicUser] = []
            total_enrollment = 0
            for section_entity in section_entites:
                instructors += [
                    staff.user.to_public_model()
                    for staff in section_entity.staff
                    if staff.member_role == RosterRole.INSTRUCTOR
                ]
                total_enrollment += section_entity.enrolled
            preferred_review_entities = sorted(
                [
                    review
                    for review in course_site_entity.application_reviews
                    if review.status == ApplicationReviewStatus.PREFERRED
                ],
                key=lambda x: x.preference,
            )
            reviews = [
                application_review.to_overview_model()
                for application_review in preferred_review_entities
            ]
            instructor_preferences = [
                application_review.application.user.to_public_model()
                for application_review in preferred_review_entities
            ]
            assignments = sorted(
                [
                    assignment.to_overview_model()
                    for assignment in course_site_entity.hiring_assignments
                ],
                key=lambda x: x.user.last_name,
            )
            total_cost = sum([assignment.level.salary for assignment in assignments])
            coverage = self._calculate_coverage(
                total_enrollment, course_site_entity.hiring_assignments
            )

            # Create overview with found data
            course_site_overview = HiringCourseSiteOverview(
                course_site_id=course_site_entity.id,
                sections=sections,
                instructors=list(set(instructors)),
                total_enrollment=total_enrollment,
                total_cost=total_cost,
                coverage=coverage,
                assignments=assignments,
                reviews=reviews,
                instructor_preferences=instructor_preferences,
            )

            # Add overview to the list
            hiring_course_site_overviews.append(course_site_overview)

        # 4. Return hiring adming overview object
        return HiringAdminOverview(sites=hiring_course_site_overviews)

    def create_hiring_assignment(
        self, subject: User, assignment: HiringAssignmentDraft
    ) -> HiringAssignmentOverview:
        """Creates a new hiring assignment."""
        # 1. Check user permissions
        self._permission.enforce(subject, "hiring.admin", "*")
        # 2. Create the entity and persist.
        assignment_entity = HiringAssignmentEntity.from_draft_model(assignment)
        self._session.add(assignment_entity)
        self._session.commit()

        return assignment_entity.to_overview_model()

    def update_hiring_assignment(
        self, subject: User, assignment: HiringAssignmentDraft
    ) -> HiringAssignmentOverview:
        """Updates an existing hiring assignment."""
        # 1. Check user permissions
        self._permission.enforce(subject, "hiring.admin", "*")
        # 2. Try to fetch the assignment from the database
        assignment_entity = self._session.get(HiringAssignmentEntity, assignment.id)
        if assignment_entity is None:
            raise ResourceNotFoundException(
                f"No hiring assignment with ID: {assignment.id}"
            )
        # 3. Update the data and commit
        assignment_entity.hiring_level_id = assignment.level.id
        assignment_entity.status = assignment.status
        assignment_entity.position_number = assignment.position_number
        assignment_entity.epar = assignment.epar
        assignment_entity.i9 = assignment.i9
        assignment_entity.notes = assignment.notes
        assignment_entity.modified = datetime.now()

        self._session.commit()

        return assignment_entity.to_overview_model()

    def delete_hiring_assignment(
        self, subject: User, assignment_id: int
    ) -> HiringAssignmentOverview:
        """Deletes an existing hiring assignment."""
        # 1. Check user permissions
        self._permission.enforce(subject, "hiring.admin", "*")

        # 2. Try to fetch the assignment from the database
        assignment_entity = self._session.get(HiringAssignmentEntity, assignment_id)
        if assignment_entity is None:
            raise ResourceNotFoundException(
                f"No hiring assignment with ID: {assignment_id}"
            )
        model = assignment_entity.to_overview_model()
        # 3. Delete and save
        self._session.delete(assignment_entity)
        self._session.commit()
        return model

    def get_hiring_levels(self, subject: User) -> list[HiringLevel]:
        """Retrieves all of the hiring levels."""
        # 1. Check user permissions
        self._permission.enforce(subject, "hiring.admin", "*")
        # 2. Fetch all
        hiring_levels_query = select(HiringLevelEntity)
        hiring_levels_entities = self._session.scalars(hiring_levels_query).all()
        # 3. Return
        return [level.to_model() for level in hiring_levels_entities]

    def create_hiring_level(self, subject: User, level: HiringLevel) -> HiringLevel:
        """Creates a new hiring level."""
        # 1. Check user permissions
        self._permission.enforce(subject, "hiring.admin", "*")
        # 2. Create and persist
        level_entity = HiringLevelEntity.from_model(level)
        self._session.add(level_entity)
        self._session.commit()

        return level_entity.to_model()

    def update_hiring_level(self, subject: User, level: HiringLevel) -> HiringLevel:
        """Updates an existing hiring level."""
        # 1. Check user permissions
        self._permission.enforce(subject, "hiring.admin", "*")
        # 2. Try to fetch the level from the database
        level_entity = self._session.get(HiringLevelEntity, level.id)
        if level_entity is None:
            raise ResourceNotFoundException(f"No hiring level with ID: {level.id}")
        # 3. Update
        level_entity.id = level.id
        level_entity.title = level.title
        level_entity.salary = level.salary
        level_entity.load = level.load
        level_entity.classification = level.classification
        level_entity.is_active = level.is_active

        self._session.commit()

        return level_entity.to_model()

    def get_hiring_summary_overview(
        self, subject: User, term_id: str, pagination_params: PaginationParams
    ) -> Paginated[HiringAssignmentSummaryOverview]:
        """Returns the hires to show on a summary page for a given term."""
        # 1. Check for hiring permissions.
        self._permission.enforce(subject, "hiring.summary", "*")
        # 2. Build query
        assignment_query = (
            select(HiringAssignmentEntity)
            .where(HiringAssignmentEntity.term_id == term_id)
            .where(
                HiringAssignmentEntity.status.in_(
                    [HiringAssignmentStatus.COMMIT, HiringAssignmentStatus.FINAL]
                )
            )
            .join(HiringAssignmentEntity.user)
            .options(
                joinedload(HiringAssignmentEntity.course_site)
                .joinedload(CourseSiteEntity.sections)
                .joinedload(SectionEntity.staff)
            )
        )
        # Count the number of rows before applying pagination and filter
        count_query = select(func.count()).select_from(
            assignment_query.distinct(HiringAssignmentEntity.id).subquery()
        )

        # Filter based on search entry
        if pagination_params.filter != "":
            query = pagination_params.filter
            criteria = or_(
                HiringAssignmentEntity.user.first_name.ilike(f"%{query}%"),
                HiringAssignmentEntity.user.last_name.ilike(f"%{query}%"),
                HiringAssignmentEntity.user.onyen.ilike(f"%{query}%"),
                HiringAssignmentEntity.user.pid.ilike(f"%{query}%"),
            )
            assignment_query = assignment_query.where(criteria)
            count_query = count_query.where(criteria)

        # Calculate offset and limit for pagination
        offset = pagination_params.page * pagination_params.page_size
        limit = pagination_params.page_size
        assignment_query = (
            assignment_query.offset(offset).limit(limit).order_by(UserEntity.last_name)
        )

        # 3. Fetch data and build summary model
        length = self._session.scalar(count_query)
        assignment_entities = self._session.scalars(assignment_query).unique().all()

        return Paginated(
            items=[
                assignment.to_summary_overview_model()
                for assignment in assignment_entities
            ],
            length=length,
            params=pagination_params,
        )

    def get_hiring_summary_for_csv(
        self, subject: User, term_id: str
    ) -> list[HiringAssignmentCsvRow]:
        """Returns the hires to show on a summary page for a given term."""
        # 1. Check for hiring permissions.
        self._permission.enforce(subject, "hiring.summary", "*")
        # 2. Build query
        assignment_query = (
            select(HiringAssignmentEntity)
            .where(HiringAssignmentEntity.term_id == term_id)
            .where(
                HiringAssignmentEntity.status.in_(
                    [HiringAssignmentStatus.COMMIT, HiringAssignmentStatus.FINAL]
                )
            )
        )
        # 3. Return items
        assignment_entities = self._session.scalars(assignment_query).all()
        return [
            assignment_entity.to_csv_row() for assignment_entity in assignment_entities
        ]
