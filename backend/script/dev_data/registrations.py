"""Sample Registration models to use in the development environment."""

from backend.entities.registration_entity import RegistrationEntity

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


registration1 = RegistrationEntity(
    id=1, 
    user_id=1, 
    event_id=1, 
    status=0
    )

registration2 = RegistrationEntity(
    id=2, 
    user_id=1, 
    event_id=2, 
    status=1
    )

models = [
    registration1, registration2
]