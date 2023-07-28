from .event import Event
from .organization import Organization
from .user import User
from .registration import Registration

__authors__ = ['Ajay Gandecha', 'Jade Keegan', 'Brianna Ta', 'Audrey Toney']
__copyright__ = 'Copyright 2023'
__license__ = 'MIT'

class EventDetail(Event):
    """Represent an Event, but also include its organization object, registered users, and registration objects."""
    organization: Organization
    users: list[User] = []
    user_associations: list[Registration] = []