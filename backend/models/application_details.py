from pydantic import BaseModel

from typing import Dict

from backend.models.academics.section import Section
from backend.models.application import (
    Application,
    UTAApplication,
    NewUTAApplication,
    Returning_UTA,
)

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


class UTAApplicationDetails(UTAApplication, ApplicationDetails):
    """
    Pydantic model to represent a `UTA Application`.

    This model is based on the `UTA` model, which defines the shape
    of the `Application` database in the PostgreSQL database.
    """

    preferred_sections: list[Section]


class NewUTAApplicationDetails(NewUTAApplication, UTAApplicationDetails):
    """
    Pydantic model to represent a `UTA Application`.

    This model is based on the `UTA` model, which defines the shape
    of the `Application` database in the PostgreSQL database.
    """


class ReturningUTAApplicationDetails(Returning_UTA):
    """
    Pydantic model to represent a `UTA Application`.

    This model is based on the `UTA` model, which defines the shape
    of the `Application` database in the PostgreSQL database.
    """


class UserApplication(BaseModel):
    """
    Pydantic model to represent a users 'Application'

    This model is based on the 'Application' model and it will
    be used to return an application with a dictionary of a
    students preferences.
    """

    application: NewUTAApplicationDetails
