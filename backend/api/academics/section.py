"""Section Course API

This API is used to access course data."""

from fastapi import APIRouter, Depends
from ..authentication import registered_user
from ...services.academics import SectionService
from ...models import User
from ...models.academics import Section, SectionDetails
from ...models.academics.section import EditedSection

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


api = APIRouter(prefix="/api/academics/section")


@api.get("", response_model=list[SectionDetails], tags=["Academics"])
def get_sections(section_service: SectionService = Depends()) -> list[SectionDetails]:
    """
    Get all sections

    Returns:
        list[SectionDetails]: All `Section`s in the `Section` database table
    """
    return section_service.all()


@api.get("/update-enrollments", response_model=None, tags=["Academics"])
def update_enrollments(
    subject: User = Depends(registered_user),
    section_service: SectionService = Depends(),
):
    """
    Updates the enrollment numbers for COMP sections.
    """
    return section_service.update_enrollment_totals(subject)


@api.get("/{id}", response_model=SectionDetails, tags=["Academics"])
def get_section_by_id(
    id: int, section_service: SectionService = Depends()
) -> SectionDetails:
    """
    Gets one section by its id

    Returns:
        SectionDetails: Section with the given ID
    """
    return section_service.get_by_id(id)


@api.get("/term/{term_id}", response_model=list[SectionDetails], tags=["Academics"])
def get_section_by_term_id(
    term_id: str, section_service: SectionService = Depends()
) -> list[SectionDetails]:
    """
    Gets list of sections by term ID

    Returns:
        list[SectionDetails]: Sections with the given term
    """
    return section_service.get_by_term(term_id)


@api.get(
    "/{subject_code}/{course_number}/{section_number}",
    response_model=SectionDetails,
    tags=["Academics"],
)
def get_section_by_subject_code(
    subject_code: str,
    course_number: str,
    section_number: str,
    section_service: SectionService = Depends(),
) -> SectionDetails:
    """
    Gets one section by its properties

    Returns:
        SectionDetails: Course with the given properties
    """
    return section_service.get(subject_code, course_number, section_number)


@api.post("", response_model=SectionDetails, tags=["Academics"])
def new_section(
    section: EditedSection,
    subject: User = Depends(registered_user),
    section_service: SectionService = Depends(),
) -> SectionDetails:
    """
    Adds a new section to the database

    Returns:
        SectionDetails: Section created
    """
    return section_service.create(subject, section)


@api.put("", response_model=SectionDetails, tags=["Academics"])
def update_section(
    section: EditedSection,
    subject: User = Depends(registered_user),
    section_service: SectionService = Depends(),
) -> SectionDetails:
    """
    Updates a section to the database

    Returns:
        SectionDetails: Section updated
    """
    return section_service.update(subject, section)


@api.delete("/{section_id}", response_model=None, tags=["Academics"])
def delete_section(
    section_id: int,
    subject: User = Depends(registered_user),
    section_service: SectionService = Depends(),
):
    """
    Deletes a section from the database
    """
    return section_service.delete(subject, section_id)
