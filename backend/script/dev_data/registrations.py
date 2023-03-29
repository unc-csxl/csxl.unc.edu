"""Sample Registration models to use in the development environment."""

from ...models import Registration

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


registration1 = Registration(
    id=1, 
    user_id=1, 
    event_id=1, 
    status=0
    )

registration2 = Registration(
    id=2, 
    user_id=1, 
    event_id=2, 
    status=1
    )

models = [
    registration1, registration2
]