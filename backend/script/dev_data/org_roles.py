"""Sample Organization Role models to use in the development environment."""

from ...models import OrgRole

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


role1 = OrgRole(
    id=1, 
    user_id=1, 
    org_id=1, 
    membership_type = 1
    )

role2 = OrgRole(
    id=2, 
    user_id=2, 
    org_id=1, 
    membership_type = 0
    )

models = [
    role1, role2
]