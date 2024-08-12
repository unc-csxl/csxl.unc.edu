from pydantic import BaseModel
from ...public_user import PublicUser
from ..section import CatalogSectionIdentity


class PhDApplicationReview(BaseModel):
    id: int
    applicant: PublicUser
    applicant_name: str
    advisor: str | None
    program_pursued: str
    intro_video_url: str
    student_preferences: list[str]
    instructor_preferences: list[str]
