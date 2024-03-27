from pydantic import BaseModel

from ...models.office_hours.section import OfficeHoursSection

from ..room import Room
from .course import Course
from .term import Term
from .section import Section
from .section_member import SectionMember

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class SectionDetails(Section):
    """
    Pydantic model to represent an `Section`, including back-populated
    relationship fields.

    This model is based on the `SectionEntity` model, which defines the shape
    of the `Section` database in the PostgreSQL database.
    """

    course: Course
    term: Term
    office_hours_section: OfficeHoursSection
