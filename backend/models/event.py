from pydantic import BaseModel
from datetime import datetime

class Event(BaseModel):
    """
    Pydantic model to represent an `Event`.
    
    This model is based on the `EventEntity` model, which defines the shape
    of the `Event` database in the PostgreSQL database
    """
    
    id: int | None=None
    name: str
    time: datetime
    location: str
    description: str
    public: bool