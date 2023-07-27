from pydantic import BaseModel
from datetime import datetime

__authors__ = ['Ajay Gandecha', 'Jade Keegan', 'Brianna Ta', 'Audrey Toney']
__copyright__ = 'Copyright 2023'
__license__ = 'MIT'

class Event(BaseModel):
    """
    Model to represent an `Event` object in a relationship

    This model is based on the `EventEntity` model, which defines the shape
    of the `Event` database in the PostgreSQL database
    """

    id: int | None=None
    name: str
    time: datetime
    location: str
    description: str
    public: bool
    org_id: int
