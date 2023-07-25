"""Sample OrganizationDetail Role models to use in the development environment."""

from backend.entities.org_role_entity import OrgRoleEntity

__authors__ = ['Ajay Gandecha', 'Jade Keegan', 'Brianna Ta', 'Audrey Toney']
__copyright__ = 'Copyright 2023'
__license__ = 'MIT'

role1 = OrgRoleEntity(
    user_id=1, 
    org_id=1, 
    membership_type = 1
    )

role2 = OrgRoleEntity(
    user_id=2, 
    org_id=1, 
    membership_type = 0
    )

models = [
    role1, role2
]