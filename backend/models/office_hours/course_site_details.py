from ..academics.section import Section
from .office_hours import OfficeHours
from .course_site import CourseSite

__authors__ = ["Sadie Amato, Bailey DeSouza, Meghan Sun, Maddy Andrews"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class CourseSiteDetails(CourseSite):
    """
    Pydantic model to represent an `CourseSite`, including back-populated
    relationship fields.

    This model is based on the `CourseSiteEntity` model, which defines the shape
    of the `CourseSite` database in the PostgreSQL database.
    """

    sections: list[Section]
    office_hours: list[OfficeHours]
