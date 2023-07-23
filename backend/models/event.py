from pydantic import BaseModel
from datetime import datetime

class Event(BaseModel):
    """
    Model to represent an `EventDetail` object in a relationship

    This model is based on the `EventDetail` model, which defines the shape
    of the `EventDetail` database in the PostgreSQL database

    This model exists to prevent infinite recursion with bidirectional
    relationship mapping.
    """

    id: int | None=None
    name: str
    time: datetime
    location: str
    description: str
    public: bool
    org_id: int
