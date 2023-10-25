from pydantic import BaseModel
from .organization import Organization
from .event import Event

__authors__ = ["Ajay Gandecha", "Jade Keegan", "Brianna Ta", "Audrey Toney"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class OrganizationDetails(Organization):
    """
    Pydantic model to represent an `Organization`, including back-populated
    relationship fields.

    This model is based on the `OrganizationEntity` model, which defines the shape
    of the `Organization` database in the PostgreSQL database.
    """

    events: list[Event]
