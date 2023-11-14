from backend.models.event import Event
from backend.models.organization import Organization
from backend.models.event_registration import EventRegistration


class EventDetails(Event):
    """
    Pydantic model to represent an `Event`.

    This model is based on the `EventEntity` model, which defines the shape
    of the `Event` database in the PostgreSQL database.
    """

    organization: Organization
