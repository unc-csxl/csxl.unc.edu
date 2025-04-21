from pydantic import BaseModel

from ...models.office_hours.course_site import CourseSite

__authors__ = ["Jade Keegan"]
__copyright__ = "Copyright 2025"
__license__ = "MIT"


class NewOfficeHoursTicketTag(BaseModel):
    """
    Pydantic model to represent a new ticket tag.

    This model is based on the `OfficeHoursTicketTagEntity` model, which defines the shape
    of the `OfficeHoursTicketTag` database in the PostgreSQL database.
    """

    name: str
    course_site_id: int


class OfficeHoursTicketTag(NewOfficeHoursTicketTag):
    """
    Pydantic model to represent an `OfficeHoursTicketTag`.

    This model is based on the `OfficeHoursTicketTagEntity` model, which defines the shape
    of the `OfficeHoursTicketTag` database in the PostgreSQL database.
    """

    id: int

class OfficeHoursTicketTagDetails(OfficeHoursTicketTag):
    """
    Pydantic model to represent an `OfficeHoursTicketTag` with details.

    This model is based on the `OfficeHoursTicketTagEntity` model, which defines the shape
    of the `OfficeHoursTicketTag` database in the PostgreSQL database.
    """

    course_site: CourseSite