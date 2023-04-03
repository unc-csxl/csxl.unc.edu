import pytest

from sqlalchemy.orm import Session
from ...models import Organization
from ...entities import OrganizationEntity
from ...services import OrganizationService

# Mock Models
root = Organization(
    id=1, 
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

updated = Organization(
    id=1, 
    name="new org", 
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
    assert len(organization.all()) is 0

def test_create_organization_and_get_by_id(organization: OrganizationService):
    org = organization.create(root)
    assert organization.get_from_id(1).id == org.id


def test_get_by_name(organization: OrganizationService):
    org = organization.create(root)
    assert organization.get_from_name("test").email == org.email


def test_delete(organization: OrganizationService):
    organization.create(root)
    assert len(organization.all()) is 1
    organization.delete(1)
    assert len(organization.all()) is 0


def test_update(organization: OrganizationService):
    org = organization.create(root)
    assert organization.get_from_id(1).name == org.name
    new_org = organization.update(updated)
    assert organization.get_from_id(1).name == new_org.name
