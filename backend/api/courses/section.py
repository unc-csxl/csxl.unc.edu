"""Section Course API

This API is used to access course data."""

from fastapi import APIRouter, Depends
from ..authentication import registered_user
from ...services.courses import SectionService
from ...models import User
from ...models.courses import Section, SectionDetails

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


api = APIRouter(prefix="/api/courses/section")


@api.get("", response_model=list[SectionDetails], tags=["Courses"])
def get_sections(section_service: SectionService = Depends()) -> list[SectionDetails]:
    """
    Get all sections

    Returns:
        list[SectionDetails]: All `Section`s in the `Section` database table
    """
    return section_service.all()


@api.get("/{id}", response_model=SectionDetails, tags=["Courses"])
def get_section_by_id(
    id: int, section_service: SectionService = Depends()
) -> SectionDetails:
    """
    Gets one section by its id

    Returns:
        SectionDetails: Section with the given ID
    """
    return section_service.get_by_id(id)


@api.get("/term/{term_id}", response_model=list[SectionDetails], tags=["Courses"])
def get_section_by_term_id(
    term_id: str, section_service: SectionService = Depends()
) -> list[SectionDetails]:
    """
    Gets list of sections by term ID

    Returns:
        list[SectionDetails]: Sections with the given term
    """
    return section_service.get_by_term(term_id)


@api.get("/subject/{subject}", response_model=list[SectionDetails], tags=["Courses"])
def get_section_by_subject(
    subject: str, section_service: SectionService = Depends()
) -> list[SectionDetails]:
    """
    Gets a list of sections by a subject

    Returns:
        list[SectionDetails]: Sections with the given section
    """
    return section_service.get_by_subject(subject)


@api.get(
    "/{subject_code}/{course_number}/{section_number}",
    response_model=SectionDetails,
    tags=["Courses"],
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


@api.post("", response_model=SectionDetails, tags=["Courses"])
def new_section(
    section: Section,
    subject: User = Depends(registered_user),
    section_service: SectionService = Depends(),
) -> SectionDetails:
    """
    Adds a new section to the database

    Returns:
        SectionDetails: Section created
    """
    return section_service.create(subject, section)


@api.put("", response_model=SectionDetails, tags=["Courses"])
def update_section(
    section: Section,
    subject: User = Depends(registered_user),
    section_service: SectionService = Depends(),
) -> SectionDetails:
    """
    Updates a section to the database

    Returns:
        SectionDetails: Section updated
    """
    return section_service.update(subject, section)


@api.delete("", response_model=None, tags=["Courses"])
def delete_section(
    section: Section,
    subject: User = Depends(registered_user),
    section_service: SectionService = Depends(),
):
    """
    Deletes a section from the database
    """
    return section_service.delete(subject, section)
