from pydantic import BaseModel
from datetime import datetime
from ..coworking.time_range import TimeRange

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class Term(TimeRange, BaseModel):
    """
    Pydantic model to represent a `Term`.

    This model is based on the `TermEntity` model, which defines the shape
    of the `Term` database in the PostgreSQL database
    """

    id: str
    name: str
    applications_open: datetime | None = None
    applications_close: datetime | None = None
