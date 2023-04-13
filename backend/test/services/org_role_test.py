import pytest

from sqlalchemy.orm import Session
from ...models import OrgRoleSummary, OrganizationSummary, UserSummary
from ...services import OrgRoleService, OrganizationService, UserService


role1 = OrgRoleSummary(
    user_id=1, 
    org_id=1, 
    membership_type = 1
    )

role2 = OrgRoleSummary(
    user_id=1, 
    org_id=1, 
    membership_type = 0
    )

role1_updated = OrgRoleSummary(
    id=1,
    user_id=1, 
    org_id=1, 
    membership_type = 1
    )

org1 = OrganizationSummary(
    name="test", 
    logo="logo", 
    short_description="description", 
    long_description="description", 
    website="website", 
    email="email", 
    instagram="instagram", 
    linked_in="linkedin", 
    youtube="youtube", 
    heel_life="heellife")

root = UserSummary(pid=999999999, onyen='root', first_name="Super", last_name="User",
             email="root@cs.unc.edu", pronouns="they / them")


@pytest.fixture()
def org_role_service(test_session: Session):
    return OrgRoleService(test_session)

@pytest.fixture()
def organization(test_session: Session):
    return OrganizationService(test_session)

@pytest.fixture()
def user(test_session: Session):
    return UserService(test_session)

def test_no_org_roles(org_role_service: OrgRoleService):
    assert len(org_role_service.all()) is 0

def test_create_org_role(org_role_service: OrgRoleService, organization: OrganizationService, user: UserService):
    organization.create(org1)
    user.save(root)
    org_role = org_role_service.create(role1)
    assert org_role.user_id == role1.user_id

def test_get_all_org_roles(org_role_service: OrgRoleService, organization: OrganizationService, user: UserService):
    organization.create(org1)
    user.save(root)
    org_role_service.create(role1)
    assert len(org_role_service.all()) is 1
    org_role_service.create(role2)
    assert len(org_role_service.all()) is 2
    assert org_role_service.all()[1].membership_type is 0

def test_get_from_userid(org_role_service: OrgRoleService, organization: OrganizationService, user: UserService):
    organization.create(org1)
    user.save(root)
    org_role_service.create(role1)
    org_role_service.create(role2)
    assert len(org_role_service.get_from_userid(1)) == 2

def test_get_from_orgid(org_role_service: OrgRoleService, organization: OrganizationService, user: UserService):
    organization.create(org1)
    user.save(root)
    org_role_service.create(role1)
    org_role_service.create(role2)
    assert len(org_role_service.get_from_orgid(1)) == 2


def test_delete(org_role_service: OrgRoleService, organization: OrganizationService, user: UserService):
    organization.create(org1)
    user.save(root)
    org_role_service.create(role1)
    assert len(org_role_service.all()) is 1
    org_role_service.delete(1)
    assert len(org_role_service.all()) is 0


def test_update(org_role_service: OrgRoleService, organization: OrganizationService, user: UserService):
    organization.create(org1)
    user.save(root)
    org_role = org_role_service.create(role1)
    assert org_role_service.get_from_userid(1)[0].membership_type == org_role.membership_type
    new_role = org_role_service.create(role1_updated)
    assert org_role_service.get_from_userid(1)[0].membership_type == new_role.membership_type == role1_updated.membership_type