"""
Service for hiring.
"""

from itertools import groupby
from operator import attrgetter
from fastapi import Depends
from sqlalchemy import String, func, or_, select, update
from sqlalchemy.orm import Session, joinedload, with_polymorphic, selectinload
from datetime import datetime

from backend.models.pagination import Paginated, PaginationParams
from ...database import db_session
from ..permission import PermissionService
from ...models.user import User
from ...models.academics.section_member import RosterRole
from ...entities import UserEntity
from ...models.application import ApplicationUnderReview, ApplicationOverview
from ...models.academics.hiring.conflict_check import ApplicationPriority, ConflictCheck
from ...entities.academics import SectionEntity, TermEntity
from ...entities.academics.course_entity import CourseEntity
from ...entities.office_hours import CourseSiteEntity
from ...entities.academics.section_member_entity import SectionMemberEntity
from ...entities.application_entity import ApplicationEntity
from ...entities.academics.hiring.application_review_entity import (
    ApplicationReviewEntity,
)
from ...entities.section_application_table import section_application_table
from ...entities.academics.hiring.hiring_level_entity import HiringLevelEntity
from ...entities.academics.hiring.hiring_assignment_entity import HiringAssignmentEntity

from ..exceptions import CoursePermissionException, ResourceNotFoundException
from ...services import PermissionService
from ...models.academics.hiring.application_review import (
    HiringStatus,
    ApplicationReview,
    ApplicationReviewOverview,
    ApplicationReviewStatus,
    ApplicationReviewCsvRow,
)
from ...models.academics.hiring.phd_application import PhDApplicationReview
from ...models.academics.hiring.hiring_assignment import *
from ...models.academics.hiring.hiring_level import *

__authors__ = ["Ajay Gandecha", "Kris Jordan"]
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
        # Step 0: Load a Course Site
        site_entity = self._load_course_site(course_site_id)

        # Step 1: Ensure that a user can access a course site's hiring.
        if not self._is_instructor(subject, site_entity):
            self._permission.enforce(
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
            self._permission.enforce(
                subject, "hiring.get_status", f"course_site/{course_site_id}"
            )

        # Step 2: Update the values for all reviews.

        # Retrieve all reviews, indexed by ID for efficient searching.
        hiring_status_reviews_by_id: dict[int, ApplicationReviewOverview] = {}
        for pool in (
            hiring_status.not_preferred,
            hiring_status.not_processed,
            hiring_status.preferred,
        ):
            for review_overview in pool:
                assert review_overview.id is not None
                hiring_status_reviews_by_id[review_overview.id] = review_overview

        # Update every application associated with the site.
        updates: list[dict] = []
        for persisted in site_entity.application_reviews:
            request = hiring_status_reviews_by_id[persisted.id]
            if (
                persisted.status != request.status
                or persisted.preference != request.preference
                or persisted.notes != request.notes
            ):
                updates.append(
                    {
                        "id": persisted.id,
                        "status": request.status,
                        "preference": request.preference,
                        "notes": request.notes,
                    }
                )

        # Bulk update
        if len(updates) > 0:
            self._session.execute(update(ApplicationReviewEntity), updates)
            self._session.commit()

        # Reload the data and return the hiring status.
        return self.get_status(subject, course_site_id)

    def create_missing_course_sites_for_term(self, subject: User, term_id: str) -> bool:
        """
        Creates missing course sites for a given term.
        """
        self._permission.enforce(
            subject,
            "hiring.create_missing_course_sites_for_term",
            f"course_sites/term:{term_id}",
        )

        # Get a list of all sections that are not associated with course sites
        section_query = select(SectionEntity).where(
            SectionEntity.term_id == term_id, SectionEntity.course_site_id.is_(None)
        )
        joint: dict[tuple[str, str], list[SectionEntity]] = {}
        for section in self._session.scalars(section_query).all():
            instructors = [
                section_member.user.full_name()
                for section_member in section.members
                if section_member.member_role == RosterRole.INSTRUCTOR
            ]
            key = (f"{section.course_id}", str(instructors))
            if key not in joint:
                joint[key] = []
            joint[key].append(section)

        # Create a course site for each group of sections
        for key, sections in joint.items():
            course_site = CourseSiteEntity(
                term_id=term_id,
                title=sections[0].get_title(),
            )
            for section in sections:
                section.course_site = course_site
            self._session.add(course_site)

        self._session.commit()
        return True

    def get_phd_applicants(
        self, subject: User, term_id: str
    ) -> list[PhDApplicationReview]:
        self._permission.enforce(
            subject, "hiring.get_phd_applicants", f"course_sites/term:{term_id}"
        )

        query = select(ApplicationEntity).where(
            ApplicationEntity.term_id == term_id,
            ApplicationEntity.type == "gta",
            ApplicationEntity.program_pursued.in_({"PhD", "PhD (ABD)", "MS", "BS/MS"}),
        )
        all = self._session.scalars(query).all()

        # Create the models
        phd_applications = {}
        for application in all:
            phd_application = PhDApplicationReview(
                id=application.id,
                applicant=application.user.to_model(),
                applicant_name=application.user.full_name(),
                advisor=application.advisor,
                program_pursued=application.program_pursued,
                intro_video_url=application.intro_video_url,
                student_preferences=[],
                instructor_preferences=[],
            )
            phd_applications[application.id] = phd_application

        sections_query = select(SectionEntity).where(SectionEntity.term_id == term_id)
        sections = {
            section.id: section
            for section in self._session.scalars(sections_query).all()
        }

        # Grab student preferences of sections
        application_ids = list(phd_applications.keys())
        section_application_query = (
            select(section_application_table)
            .where(section_application_table.c.application_id.in_(application_ids))
            .order_by(section_application_table.c.preference)
        )
        for section_application in self._session.execute(section_application_query):
            _, section_id, application_id = section_application
            phd_applications[application_id].student_preferences.append(
                f"{sections[section_id].course_id}.{sections[section_id].number}"
            )

        # Grab instructor preferences of applications
        instructor_review_query = (
            select(ApplicationReviewEntity)
            .where(ApplicationReviewEntity.application_id.in_(application_ids))
            .where(ApplicationReviewEntity.status == ApplicationReviewStatus.PREFERRED)
            .order_by(ApplicationReviewEntity.preference)
            .options(joinedload(ApplicationReviewEntity.course_site))
        )
        instructor_preferences = self._session.scalars(instructor_review_query).all()
        for review in instructor_preferences:
            phd_applications[review.application_id].instructor_preferences.append(
                f"({review.preference}) {review.course_site.sections[0].course_id}.{review.course_site.sections[0].number}"
            )

        return list(phd_applications.values())

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
                review = ApplicationReviewEntity(
                    application_id=application_id,
                    course_site_id=site.id,
                    status=ApplicationReviewStatus.NOT_PROCESSED,
                    preference=preference,
                    notes="",
                )
                preference += 1
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
        return self._session.scalar(count_unprocessed) or 1

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
        return list(self._session.scalars(application_ids).unique().all())

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
                applicant_id=applications[review.application_id].user_id,
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

    # Hiring Admin Features

    def _calculate_coverage(
        self, enrollment: int, assignments: list[HiringAssignmentEntity]
    ) -> float:
        coverage: float = 0.0
        for assignment in assignments:
            if assignment.hiring_level.classification in {
                HiringLevelClassification.MS,
                HiringLevelClassification.PHD,
            }:
                coverage += assignment.hiring_level.load
            elif assignment.hiring_level.classification == HiringLevelClassification.UG:
                coverage += assignment.hiring_level.load * 0.25
            else:
                # IOR
                coverage += 0

        return (float(enrollment) / 60.0) - coverage

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
                joinedload(CourseSiteEntity.sections),
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
            )

            # Add overview to the list
            hiring_course_site_overviews.append(course_site_overview)

        # 4. Return hiring adming overview object
        return HiringAdminOverview(sites=hiring_course_site_overviews)

    def get_hiring_admin_course_overview(
        self, subject: User, course_site_id: int
    ) -> HiringAdminCourseOverview:
        self._permission.enforce(subject, "hiring.admin", "*")
        course_site_entity = self._session.get(CourseSiteEntity, course_site_id)
        if course_site_entity is None:
            raise ResourceNotFoundException()

        preferred_review_query = (
            select(ApplicationReviewEntity)
            .where(
                ApplicationReviewEntity.course_site_id == course_site_entity.id,
                ApplicationReviewEntity.status == ApplicationReviewStatus.PREFERRED,
            )
            .order_by(ApplicationReviewEntity.preference)
            .options(
                joinedload(ApplicationReviewEntity.application).joinedload(
                    ApplicationEntity.user
                )
            )
        )
        preferred_review_entities = self._session.scalars(preferred_review_query).all()

        def to_overview(review: ApplicationReviewEntity) -> ApplicationReviewOverview:
            return ApplicationReviewOverview(
                id=review.id,
                application_id=review.application_id,
                course_site_id=course_site_entity.id,
                status=review.status,
                preference=review.preference,
                notes=review.notes,
                application=review.application.to_review_overview_model(),
                applicant_id=review.application.user_id,
                applicant_course_ranking=0,
            )

        reviews = [
            to_overview(application_review)
            for application_review in preferred_review_entities
        ]

        instructor_preferences = [review.application.applicant for review in reviews]

        assignments_query = (
            select(HiringAssignmentEntity)
            .where(HiringAssignmentEntity.course_site_id == course_site_id)
            .options(joinedload(HiringAssignmentEntity.user))
        )
        assignment_entities = self._session.scalars(assignments_query).all()
        assignments = [
            assignment.to_overview_model() for assignment in assignment_entities
        ]

        return HiringAdminCourseOverview(
            assignments=assignments,
            reviews=reviews,
            instructor_preferences=instructor_preferences,
        )

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
        assert assignment.level.id is not None
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
        assert level.id is not None
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
        """
        Returns the hires to show on a summary page for a given term.

        Args:
            subject: The user making the request
            term_id: The term to get assignments for
            pagination_params: Parameters for pagination and filtering

        Raises:
            ValueError: If pagination parameters are invalid
            PermissionError: If user lacks required permissions
        """
        # 1. Validate inputs
        if pagination_params.page < 0 or pagination_params.page_size <= 0:
            raise ValueError("Invalid pagination parameters")

        # 2. Check for hiring permissions
        self._permission.enforce(subject, "hiring.summary", "*")

        # 3. Build base query with consistent joins and ordering
        SUMMARY_STATUSES = [HiringAssignmentStatus.COMMIT, HiringAssignmentStatus.FINAL]
        base_query = (
            select(HiringAssignmentEntity)
            .join(HiringAssignmentEntity.user)
            .where(HiringAssignmentEntity.term_id == term_id)
            .where(HiringAssignmentEntity.status.in_(SUMMARY_STATUSES))
            .order_by(
                UserEntity.last_name, UserEntity.first_name
            )  # Secondary sort for stability
        )

        # 4. Apply search filter if present
        search_query = pagination_params.filter.strip()
        if search_query:
            # Use parameter binding for safety
            search_pattern = f"%{search_query.lower()}%"
            criteria = or_(
                func.lower(UserEntity.first_name).like(search_pattern),
                func.lower(UserEntity.last_name).like(search_pattern),
            )
            base_query = base_query.where(criteria)

        # 5. Create count query from base query
        count_query = select(func.count()).select_from(base_query.subquery())

        # 6. Create assignment query with eager loading
        assignment_query = base_query.options(
            joinedload(HiringAssignmentEntity.course_site)
            .joinedload(CourseSiteEntity.sections)
            .joinedload(SectionEntity.staff),
        )

        # 7. Apply pagination
        offset = pagination_params.page * pagination_params.page_size
        limit = pagination_params.page_size
        assignment_query = assignment_query.offset(offset).limit(limit)

        # 8. Execute queries
        length = self._session.scalar(count_query) or 0
        assignment_entities = self._session.scalars(assignment_query).unique().all()

        # 9. Build and return response
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
            .join(HiringAssignmentEntity.user)
            .where(HiringAssignmentEntity.term_id == term_id)
            .where(
                HiringAssignmentEntity.status.in_(
                    [HiringAssignmentStatus.COMMIT, HiringAssignmentStatus.FINAL]
                )
            )
            .order_by(UserEntity.last_name, UserEntity.first_name)
        )
        # 3. Return items
        assignment_entities = self._session.scalars(assignment_query).all()
        return [
            assignment_entity.to_csv_row() for assignment_entity in assignment_entities
        ]

    def get_course_site_hiring_status_csv(
        self, subject: User, course_site_id: int
    ) -> list[ApplicationReviewCsvRow]:
        """Retrieves the applications to a course for a CSV export."""
        # Step 0: Load a Course Site
        site_entity = self._load_course_site(course_site_id)

        # Step 1: Ensure that a user can access a course site's hiring.
        if not self._is_instructor(subject, site_entity):
            self._permission.enforce(
                subject, "hiring.get_status", f"course_site/{course_site_id}"
            )

        # Step 2: Convert all applicants to rows and return
        return [
            application.to_csv_row() for application in site_entity.application_reviews
        ]

    def get_hiring_assignments_for_course_site(
        self, subject: User, course_site_id: int, pagination_params: PaginationParams
    ) -> Paginated[HiringAssignmentOverview]:
        """Gets the committed hiring assignments for one course site."""
        # Step 1: Check permissions
        course_site = self._load_course_site(course_site_id)
        if not self._is_instructor(subject, course_site):
            self._permission.enforce(
                subject, "hiring.get_assignments", f"course_site/{course_site_id}"
            )

        # Step 2: Create query
        assignments_query = (
            select(HiringAssignmentEntity)
            .where(HiringAssignmentEntity.course_site_id == course_site_id)
            .where(HiringAssignmentEntity.status == HiringAssignmentStatus.FINAL)
            .join(HiringAssignmentEntity.user)
            .join(HiringAssignmentEntity.hiring_level)
        )
        # Count the number of rows before applying pagination and filter
        count_query = select(func.count()).select_from(
            assignments_query.distinct(HiringAssignmentEntity.id).subquery()
        )

        # Filter based on search entry
        if pagination_params.filter != "":
            query = pagination_params.filter
            criteria = or_(
                UserEntity.first_name.ilike(f"%{query}%"),
                UserEntity.last_name.ilike(f"%{query}%"),
                UserEntity.onyen.ilike(f"%{query}%"),
                UserEntity.email.ilike(f"%{query}%"),
                HiringLevelEntity.title.ilike(f"%{query}%"),
            )
            assignments_query = assignments_query.where(criteria)
            count_query = count_query.where(criteria)

        # Calculate offset and limit for pagination
        offset = pagination_params.page * pagination_params.page_size
        limit = pagination_params.page_size
        assignments_query = (
            assignments_query.offset(offset)
            .limit(limit)
            .order_by(HiringLevelEntity.salary.desc(), UserEntity.last_name)
        )

        # Step 3: Load and return data
        assignment_entities = self._session.scalars(assignments_query).all()
        length = self._session.scalar(count_query) or 0
        return Paginated(
            items=[
                assignment.to_overview_model() for assignment in assignment_entities
            ],
            length=length,
            params=pagination_params,
        )

    def get_assignment_summary_for_instructors_csv(
        self, subject: User, course_site_id: int
    ) -> list[HiringAssignmentSummaryCsvRow]:
        """Returns the hires to show for a course site as a CSV."""
        # 1. Check for hiring permissions.
        course_site = self._load_course_site(course_site_id)
        if not self._is_instructor(subject, course_site):
            self._permission.enforce(
                subject, "hiring.get_assignments", f"course_site/{course_site_id}"
            )

        # 2. Build query
        assignments_query = (
            select(HiringAssignmentEntity)
            .where(HiringAssignmentEntity.course_site_id == course_site_id)
            .where(
                HiringAssignmentEntity.status.in_(
                    [HiringAssignmentStatus.COMMIT, HiringAssignmentStatus.FINAL]
                )
            )
        )

        # 3. Return items
        assignment_entities = self._session.scalars(assignments_query).all()
        return [
            assignment_entity.to_summary_csv_row()
            for assignment_entity in assignment_entities
        ]

    def conflict_check(self, subject: User, application_id: int) -> ConflictCheck:
        self._permission.enforce(subject, "hiring.conflict_check", "*")
        from sqlalchemy import func, and_

        student_priority = func.min(section_application_table.c.preference).label(
            "student_priority"
        )
        query = (
            select(
                student_priority,
                func.min(ApplicationReviewEntity.preference).label(
                    "instructor_priority"
                ),
                CourseSiteEntity.id,
                CourseSiteEntity.title,
            )
            .join(
                CourseSiteEntity,
                ApplicationReviewEntity.course_site_id == CourseSiteEntity.id,
                isouter=True,
            )
            .join(
                SectionEntity,
                SectionEntity.course_site_id == CourseSiteEntity.id,
                isouter=True,
            )
            .join(
                ApplicationEntity,
                ApplicationReviewEntity.application_id == ApplicationEntity.id,
                isouter=True,
            )
            .join(
                section_application_table,
                and_(
                    section_application_table.c.section_id == SectionEntity.id,
                    section_application_table.c.application_id == ApplicationEntity.id,
                ),
                isouter=True,
            )
            .where(
                ApplicationEntity.id == application_id,
                ApplicationReviewEntity.status == ApplicationReviewStatus.PREFERRED,
                section_application_table.c.preference.isnot(None),
            )
            .group_by(CourseSiteEntity.id)
            .order_by(student_priority.asc())
        )
        preferences = self._session.execute(query).all()
        priorities: list[ApplicationPriority] = []
        for student_pri, instructor_pri, course_site_id, title in preferences:
            priorities.append(
                ApplicationPriority(
                    student_priority=student_pri,
                    instructor_priority=instructor_pri,
                    course_site_id=course_site_id,
                    course_title=title,
                )
            )

        assignments_query = (
            select(HiringAssignmentEntity)
            .join(ApplicationReviewEntity)
            .join(ApplicationEntity)
            .where(ApplicationEntity.id == application_id)
        )

        return ConflictCheck(
            application_id=application_id,
            assignments=[
                a.to_summary_overview_model()
                for a in self._session.scalars(assignments_query).all()
            ],
            priorities=priorities,
        )

    # New: Generate applicant CSV rows for a term with minimal memory use
    def iter_applicants_for_term_csv(self, subject: User, term_id: str):
        """
        Yields dict rows for all applicants in a term. Designed to minimize memory usage by
        iterating over applications and issuing small, targeted queries per applicant.
        """
        # Permissions: admin-level export
        self._permission.enforce(subject, "hiring.admin", "*")

        # Get application IDs for the term (avoid loading whole objects at once)
        app_ids = self._session.scalars(
            select(ApplicationEntity.id).where(ApplicationEntity.term_id == term_id)
        ).all()

        for app_id in app_ids:
            application = self._session.get(ApplicationEntity, app_id)
            if application is None:
                continue
            user = application.user

            # Assignments for this applicant in this term (by user_id + term), include sections and course
            assignment_q = (
                select(HiringAssignmentEntity)
                .where(
                    HiringAssignmentEntity.user_id == user.id,
                    HiringAssignmentEntity.term_id == application.term_id,
                )
                .options(
                    joinedload(HiringAssignmentEntity.hiring_level),
                    joinedload(HiringAssignmentEntity.course_site)
                    .joinedload(CourseSiteEntity.sections)
                    .joinedload(SectionEntity.course),
                    joinedload(HiringAssignmentEntity.course_site)
                    .joinedload(CourseSiteEntity.sections)
                    .joinedload(SectionEntity.staff)
                    .joinedload(SectionMemberEntity.user),
                )
            )
            assignment_rows = self._session.scalars(assignment_q).unique().all()
            assignments_parts: list[str] = []
            for a in assignment_rows:
                section = (
                    a.course_site.sections[0]
                    if len(a.course_site.sections) > 0
                    else None
                )
                if section is None:
                    continue
                course = section.course
                course_code = f"{course.subject_code}{course.number}-{section.number}"
                instructors = [
                    sm.user.last_name
                    for sm in getattr(section, "staff", [])
                    if sm.member_role == RosterRole.INSTRUCTOR
                ]
                instructors_text = (
                    ", ".join(sorted(set(instructors))) if instructors else ""
                )
                part = f"{a.hiring_level.title} ({a.hiring_level.load}) {course_code}"
                if instructors_text:
                    part += f" ({instructors_text})"
                assignments_parts.append(part)
            assignments_field = ", ".join(assignments_parts)

            # Preferred sections (ordered by preference ascending)
            pref_q = (
                select(
                    section_application_table.c.preference,
                    SectionEntity.number.label("section_number"),
                    CourseEntity.subject_code,
                    CourseEntity.number.label("course_number"),
                )
                .join(
                    SectionEntity,
                    SectionEntity.id == section_application_table.c.section_id,
                )
                .join(CourseEntity, CourseEntity.id == SectionEntity.course_id)
                .where(section_application_table.c.application_id == app_id)
                .order_by(section_application_table.c.preference.asc())
            )
            preferences = self._session.execute(pref_q).all()
            # Build mapping course_id -> min preference for ordering instructor selections later
            course_min_pref: dict[str, int] = {}
            preferred_sections_list: list[str] = []
            for pref, section_number, subj, course_num in preferences:
                preferred_sections_list.append(f"{subj}{course_num}-{section_number}")
                course_key = f"{subj}{course_num}"
                if (
                    course_key not in course_min_pref
                    or pref < course_min_pref[course_key]
                ):
                    course_min_pref[course_key] = pref

            # Instructor selections (PREFERRED reviews) ordered by student's section preference
            reviews_q = select(ApplicationReviewEntity).where(
                ApplicationReviewEntity.application_id == app_id,
                ApplicationReviewEntity.status == ApplicationReviewStatus.PREFERRED,
            )
            review_entities = self._session.scalars(reviews_q).all()
            # For each review, find a representative course (subject+number) from its course_site (first section)
            selected_courses: set[str] = set()
            for rev in review_entities:
                if rev.course_site_id is None:
                    continue
                course_row = self._session.execute(
                    select(CourseEntity.subject_code, CourseEntity.number)
                    .join(SectionEntity, SectionEntity.course_id == CourseEntity.id)
                    .where(SectionEntity.course_site_id == rev.course_site_id)
                    .limit(1)
                ).first()
                if course_row is not None:
                    subj, num = course_row
                    selected_courses.add(f"{subj}{num}")

            # Sort selected courses by student's min preference for that course
            ordered_courses = sorted(
                list(selected_courses), key=lambda cid: course_min_pref.get(cid, 10**9)
            )
            instructor_selections_field = ", ".join(ordered_courses)

            yield {
                "type": application.type,
                "assignments": assignments_field,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "pid": str(user.pid),
                "email": user.email,
                "pronouns": user.pronouns,
                "program_pursued": application.program_pursued or "",
                "comp_227": (
                    application.comp_227.value
                    if application.comp_227 is not None
                    else ""
                ),
                "intro_video_url": application.intro_video_url or "",
                "prior_experience": application.prior_experience or "",
                "advisor": application.advisor or "",
                "preferred_sections": ", ".join(preferred_sections_list),
                "instructor_selections": instructor_selections_field,
            }
