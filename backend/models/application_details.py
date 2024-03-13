from pydantic import BaseModel

from backend.models.academics.section import Section
from backend.models.application import Application, UTA, New_UTA, Returning_UTA

from backend.models.user import User

__authors__ = ["Ben Goulet"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class ApplicationDetails(Application):
    """
    Pydantic model to represent an `Application`.

    This model is based on the `ApplicationEntity` model, which defines the shape
    of the `Application` database in the PostgreSQL database.
    """

    user: User


class UTADetails(UTA):
    """
    Pydantic model to represent a `UTA Application`.

    This model is based on the `UTA` model, which defines the shape
    of the `Application` database in the PostgreSQL database.
    """

    preferred_courses: list[Section] = []
    eligible_courses: list[Section] = []


class New_UTADetails(New_UTA):
    """
    Pydantic model to represent a `UTA Application`.

    This model is based on the `UTA` model, which defines the shape
    of the `Application` database in the PostgreSQL database.
    """

    user: User


class Returning_UTADetails(Returning_UTA):
    """
    Pydantic model to represent a `UTA Application`.

    This model is based on the `UTA` model, which defines the shape
    of the `Application` database in the PostgreSQL database.
    """
