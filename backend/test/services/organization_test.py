import pytest

from sqlalchemy.orm import Session
from ...models import Organization
from ...services import OrganizationService

# Mock Models
org1 = Organization(
    name="test", 
    slug="ABC",
    logo="logo", 
    short_description="description", 
    long_description="description", 
    website="website", 
    email="email", 
    instagram="instagram", 
    linked_in="linkedin", 
    youtube="youtube", 
    heel_life="heellife")

org2 = Organization(
    name="test", 
    slug="CBA",
    logo="logo", 
    short_description="description", 
    long_description="description", 
    website="website", 
    email="email", 
    instagram="instagram", 
    linked_in="linkedin", 
    youtube="youtube", 
    heel_life="heellife")

org1_updated = Organization(
    id=1, 
    name="new org", 
    slug="ABC",
    logo="logo", 
    short_description="description", 
    long_description="description", 
    website="website", 
    email="email", 
    instagram="instagram", 
    linked_in="linkedin", 
    youtube="youtube", 
    heel_life="heellife")

@pytest.fixture()
def organization(test_session: Session):
    return OrganizationService(test_session)

def test_no_organizations(organization: OrganizationService):
    """Tests that the test session initially contains no organizations"""
    assert len(organization.all()) is 0

def test_create_organization_and_get_by_id(organization: OrganizationService):
    """Tests that an organization can be created and retrieved using get_from_id()"""
    org = organization.create(org1)
    assert organization.get_from_id(1).id == org.id

def test_get_all_organizations(organization: OrganizationService):
    """Tests that the all() method returns all created organizations"""
    organization.create(org1)
    assert len(organization.all()) is 1
    organization.create(org2)
    assert len(organization.all()) is 2
    assert organization.all()[1].id is 2

def test_get_by_name(organization: OrganizationService):
    """Tests that an organization can be retrieved by its name using get_from_name()"""
    org = organization.create(org1)
    assert organization.get_from_name("test").email == org.email


def test_delete(organization: OrganizationService):
    """Tests that delete() removes an organization from the table"""
    organization.create(org1)
    assert len(organization.all()) is 1
    organization.delete(1)
    assert len(organization.all()) is 0


def test_update(organization: OrganizationService):
    """Tests that update() changes an existing organization in the table"""
    org = organization.create(org1)
    assert organization.get_from_id(1).name == org.name
    new_org = organization.update(org1_updated)
    assert organization.get_from_id(1).name == new_org.name
