from pydantic import BaseModel
from datetime import datetime

__authors__ = ["Ajay Gandecha", "Jade Keegan", "Brianna Ta", "Audrey Toney"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class Event(BaseModel):
    """
    Pydantic model to represent an `Event`.

    This model is based on the `EventEntity` model, which defines the shape
    of the `Event` database in the PostgreSQL database
    """

    id: int | None = None
    name: str
    time: datetime
    location: str
    description: str
    public: bool
    registration_limit: int
    can_register: bool
    organization_id: int
