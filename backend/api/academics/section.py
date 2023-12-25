"""Section Course API

This API is used to access course data."""

from fastapi import APIRouter, Depends
from ..authentication import registered_user
from ...services.academics import SectionService
from ...models import User
from ...models.academics import Section, SectionDetails

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


@api.get("/subject/{subject}", response_model=list[SectionDetails], tags=["Academics"])
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
    section: Section,
    subject: User = Depends(registered_user),
    section_service: SectionService = Depends(),
) -> SectionDetails:
    """
    Adds a new section to the database

    Returns:
        SectionDetails: Section created
    """
    created_section = section_service.create(subject, section)

    # This function is needed to ensure that the lecture room passed into the
    # API from the SectionModel is properly added into the database when converted
    # to entities. This stems from the fact that our `SectionModel` splits up `rooms`
    # into two properties -- `lecture_room` and `office_hour_rooms`. So, when we try
    # and POST a section model, we cannot post directly into the section entity.
    #
    # The solution relies on section being created *first* (so that its ID field is
    # populated), then connecting it to a room in the `academics__section_room`
    # table via `section_service.add_lecture_room_to_section()`.
    section_service.add_lecture_room_to_section(
        subject, created_section, section.lecture_room
    )

    # Then, we want to re-get the section now that the correct lecture room relation
    # has been added to the database. Since ID is possibly a null value, we need to
    # unwrap it in an if-statement. If for some reason ID does not exist, we can
    # default to returning the `created_section` entity created earlier. Otherwise, we
    # will return the entity that has the `lecture_room` field populated correctly.
    return (
        section_service.get_by_id(created_section.id)
        if created_section.id
        else created_section
    )


@api.put("", response_model=SectionDetails, tags=["Academics"])
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
