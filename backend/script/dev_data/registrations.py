"""Sample RegistrationDetail models to use in the development environment."""

from backend.entities.registration_entity import RegistrationEntity

__authors__ = ['Ajay Gandecha', 'Jade Keegan', 'Brianna Ta', 'Audrey Toney']
__copyright__ = 'Copyright 2023'
__license__ = 'MIT'

registration1 = RegistrationEntity( 
    user_id=1, 
    event_id=1, 
    status=0
    )

registration2 = RegistrationEntity(
    user_id=1, 
    event_id=2, 
    status=1
    )

registration3 = RegistrationEntity(
    user_id=1, 
    event_id=3, 
    status=1
    )

registration4 = RegistrationEntity(
    user_id=1, 
    event_id=4, 
    status=0
    )

models = [
    registration1, registration2, registration3, registration4
]