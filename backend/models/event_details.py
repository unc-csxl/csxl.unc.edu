from backend.models.event import Event
from backend.models.event_registration import EventRegistration
from backend.models.organization import Organization


class EventDetails(Event):
    """
    Pydantic model to represent an `Event`.

    This model is based on the `EventEntity` model, which defines the shape
    of the `Event` database in the PostgreSQL database.
    """

    organization: Organization
    registrations: list[EventRegistration]


class UserEvent(EventDetails):
    """
    Pydantic model to represent a `UserEvent`.

    This model contains an extra "is registered" field denoting whether the
    currently logged in user is registered for an event or not.
    """

    registration_count: int = 0
    is_registered: bool = False
    is_organizer: bool = False
