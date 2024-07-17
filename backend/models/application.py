from pydantic import BaseModel

from .comp_227 import Comp227
from .user import User
from .academics.section import CatalogSectionIdentity

__authors__ = ["Ben Goulet"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class Application(BaseModel):
    """
    Pydantic model to represent an `Application`.

    This model is based on the `ApplicationEntity` model, which defines the shape
    of the `Application` database in the PostgreSQL database.
    """

    id: int | None = None
    user_id: int
    term_id: str
    type: str
    academic_hours: int | None = None
    extracurriculars: str | None = None
    expected_graduation: str | None = None
    program_pursued: str | None = None
    other_programs: str | None = None
    gpa: float | None | None = None
    comp_gpa: float | None = None
    comp_227: Comp227 | None = None
    intro_video_url: str | None = None
    prior_experience: str | None = None
    service_experience: str | None = None
    additional_experience: str | None = None
    ta_experience: str | None = None
    best_moment: str | None = None
    desired_improvement: str | None = None
    advisor: str | None = None
    preferred_sections: list[CatalogSectionIdentity]


class ApplicationOverview(BaseModel):
    """
    Pydantic model to represent an `ApplicationOverview`.

    This model is based on the `ApplicationEntity` model, which defines the shape
    of the `Application` database in the PostgreSQL database.
    """

    id: int | None = None
    type: str
    applicant_name: str
    academic_hours: int | None
    extracurriculars: str | None
    expected_graduation: str | None
    program_pursued: str | None
    other_programs: str | None
    gpa: float | None | None
    comp_gpa: float | None
    comp_227: Comp227 | None
    intro_video_url: str | None
    prior_experience: str | None
    service_experience: str | None
    additional_experience: str | None
    ta_experience: str | None
    best_moment: str | None
    desired_improvement: str | None
    advisor: str | None
    preferred_sections: list[CatalogSectionIdentity]
