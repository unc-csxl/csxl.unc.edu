from pydantic import BaseModel
from datetime import datetime, date, time

__author__ = "Emmalyn Foster"
__copyright__ = "Copyright 2024"
__license__ = "MIT"

class DropIn(BaseModel):
    """Represents the model used to create new drop-ins."""
    id: int | None = None
    title: str
    date: date
    start: time
    end: time
    link: str