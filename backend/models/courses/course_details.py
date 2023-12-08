from pydantic import BaseModel
from .section import Section
from .course import Course

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class CourseDetails(Course):
    """
    Pydantic model to represent a `Course`, including back-populated
    relationship fields.

    This model is based on the `CourseEntity` model, which defines the shape
    of the `Course` database in the PostgreSQL database.
    """

    sections: list[Section]
