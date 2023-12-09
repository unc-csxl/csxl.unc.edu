from pydantic import BaseModel
from datetime import datetime

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class Course(BaseModel):
    """
    Pydantic model to represent a `Course`.

    This model is based on the `CourseEntity` model, which defines the shape
    of the `Course` database in the PostgreSQL database
    """

    id: str
    subject_code: str
    number: str
    title: str
    description: str
