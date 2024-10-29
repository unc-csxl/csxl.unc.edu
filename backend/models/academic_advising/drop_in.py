from pydantic import BaseModel
from datetime import datetime

__author__ = "Emmalyn Foster"
__copyright__ = "Copyright 2024"
__license__ = "MIT"

class DropIn(BaseModel):
    """Represents the model used to create new drop-ins."""
    id: int | None = None
    title: str
    start: datetime
    end: datetime
    link: str