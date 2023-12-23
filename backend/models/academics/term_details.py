from pydantic import BaseModel
from .section import Section
from .term import Term

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class TermDetails(Term):
    """
    Pydantic model to represent an `Term`, including back-populated
    relationship fields.

    This model is based on the `TermEntity` model, which defines the shape
    of the `Term` database in the PostgreSQL database.
    """

    course_sections: list[Section]
