from pydantic import BaseModel

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


class UTAApplication(Application):
    """
    Pydantic model to represent a `UTA`.

    This model is based on the `Application` model, which defines the shape
    of the `Application` database in the PostgreSQL database.
    """

    academic_hours: int
    extracurriculars: str
    expected_graduation: str
    program_pursued: str
    other_programs: str
    gpa: float
    comp_gpa: float
    comp_227: str


class NewUTAApplication(UTAApplication):
    """
    Pydantic model to represent a `New UTA`.

    This model is based on the `UTA` model, which defines the shape
    of the `Application` database in the PostgreSQL database.
    """

    intro_video_url: str
    prior_experience: str
    service_experience: str
    additional_experience: str


class Returning_UTA(UTAApplication):
    """
    Pydantic model to represent a `Returning UTA`.

    This model is based on the `UTA` model, which defines the shape
    of the `Application` database in the PostgreSQL database.
    """

    ta_experience: str
    best_moment: str
    desired_improvement: str
