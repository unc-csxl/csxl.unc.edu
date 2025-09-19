"""Tests for the OrganizationService class."""

# PyTest
import pytest
from unittest.mock import create_autospec

from backend.services.exceptions import (
    UserPermissionException,
    ResourceNotFoundException,
    ResourceExistsException,
    OrganizationPermissionException,
)

# Tested Dependencies
from ....models import Organization, User
from ....models.organization_membership import (
    OrganizationMembership,
    OrganizationMembershipRegistration,
    OrganizationPermissionLevel,
    OrganizationMembershipStatus,
)
from ....services import OrganizationService

# Injected Service Fixtures
from ..fixtures import organization_svc_integration

# Explicitly import Data Fixture to load entities in database
from ..core_data import setup_insert_data_fixture

# Data Models for Fake Data Inserted in Setup
from .organization_test_data import (
    organizations,
    to_add,
    cads,
    appteam,
    queerhack,
    new_cads,
    to_add_conflicting_id,
)
from .organization_membership_test_data import (
    member_to_add,
    non_member,
    member_1,
    member_2,
    roster,
    edit_member_2,
    bad_membership,
)
from ..user_data import root, user
from ..academics.term_data import current_term

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

# Test Functions

# Test `OrganizationService.all()`


def test_get_all(organization_svc_integration: OrganizationService):
    """Test that all organizations can be retrieved."""
    fetched_organizations = organization_svc_integration.all()
    assert fetched_organizations is not None
    assert len(fetched_organizations) == len(organizations)
    assert isinstance(fetched_organizations[0], Organization)


# Test `OrganizationService.get_by_id()`


def test_get_by_slug(organization_svc_integration: OrganizationService):
    """Test that organizations can be retrieved based on their ID."""
    fetched_organization = organization_svc_integration.get_by_slug(cads.slug)
    assert fetched_organization is not None
    assert isinstance(fetched_organization, Organization)
    assert fetched_organization.slug == cads.slug


# Test `OrganizationService.create()`


def test_create_enforces_permission(organization_svc_integration: OrganizationService):
    """Test that the service enforces permissions when attempting to create an organization."""

    # Setup to test permission enforcement on the PermissionService.
    organization_svc_integration._permission = create_autospec(
        organization_svc_integration._permission
    )

    # Test permissions with root user (admin permission)
    organization_svc_integration.create(root, to_add)
    organization_svc_integration._permission.enforce.assert_called_with(
        root, "organization.create", "organization"
    )


def test_create_organization_as_root(organization_svc_integration: OrganizationService):
    """Test that the root user is able to create new organizations."""
    created_organization = organization_svc_integration.create(root, to_add)
    assert created_organization is not None
    assert created_organization.id is not None


def test_create_organization_id_already_exists(
    organization_svc_integration: OrganizationService,
):
    """Test that the root user is able to create new organizations when an extraneous ID is provided."""
    created_organization = organization_svc_integration.create(
        root, to_add_conflicting_id
    )
    assert created_organization is not None
    assert created_organization.id is not None


def test_create_organization_as_user(organization_svc_integration: OrganizationService):
    """Test that any user is *unable* to create new organizations."""
    with pytest.raises(UserPermissionException):
        organization_svc_integration.create(user, to_add)
        pytest.fail()  # Fail test if no error was thrown above


# Test Organization Management (roster) begin


def test_add_default_membership_to_open_org(
    organization_svc_integration: OrganizationService,
):
    """Test that a user can add themselves to an open organization only with default values (title/is_admin)"""
    added_member = organization_svc_integration.add_membership(
        user, cads.slug, member_to_add
    )
    assert added_member is not None
    assert added_member.id is not None
    assert added_member.title == "Member"
    assert added_member.permission_level == OrganizationPermissionLevel.MEMBER
    assert added_member.status == OrganizationMembershipStatus.ACTIVE


def test_add_custom_membership_to_open_org(
    organization_svc_integration: OrganizationService,
):
    """Test that an organization admin can add custom memberships to an open organization"""
    added_member = organization_svc_integration.add_membership(
        member_1, cads.slug, member_to_add
    )
    assert added_member is not None
    assert added_member.id is not None
    assert added_member.title == "Non-default title"
    assert added_member.permission_level == OrganizationPermissionLevel.ADMIN
    assert added_member.status == OrganizationMembershipStatus.ACTIVE


def test_add_default_membership_to_apply_org(
    organization_svc_integration: OrganizationService,
):
    """Test that a user can add themselves to an apply organization only with default values (title/is_admin)"""
    member_to_add.organization_id = appteam.id
    added_member = organization_svc_integration.add_membership(
        user, appteam.slug, member_to_add
    )
    assert added_member is not None
    assert added_member.id is not None
    assert added_member.title == "Member"
    assert added_member.permission_level == OrganizationPermissionLevel.MEMBER
    assert added_member.status == OrganizationMembershipStatus.PENDING


def test_add_membership_to_closed_org(
    organization_svc_integration: OrganizationService,
):
    """Test that a non-admin user cannot join a closed organization"""
    member_to_add.organization_id = queerhack.id
    with pytest.raises(Exception):
        organization_svc_integration.add_membership(user, queerhack.slug, member_to_add)


def test_add_member_to_nonexistent_organization(
    organization_svc_integration: OrganizationService,
):
    """Test that member cannot be added to nonexistent organization"""
    with pytest.raises(ResourceNotFoundException):
        organization_svc_integration.add_membership(root, "fakeslug", non_member)


def test_add_existing_member_to_organization(
    organization_svc_integration: OrganizationService,
):
    """Test that member cannot be added to an organization multiple times"""
    with pytest.raises(ResourceExistsException):
        organization_svc_integration.add_membership(root, cads.slug, member_1)


def test_add_different_user_to_organization(
    organization_svc_integration: OrganizationService,
):
    """Test that member cannot be added to an organization by non-admin member"""
    with pytest.raises(OrganizationPermissionException):
        organization_svc_integration.add_membership(member_2, cads.slug, non_member)


def test_add_nonexistent_user_to_organization(
    organization_svc_integration: OrganizationService,
):
    """Test that nonexistent user cannot be added to an organization"""
    fake_user = User(id=100)
    member_to_add = OrganizationMembershipRegistration(
        user_id=fake_user.id, organization_id=cads.id
    )
    with pytest.raises(ResourceNotFoundException):
        organization_svc_integration.add_membership(root, cads.slug, member_to_add)


def test_get_roster_by_slug(organization_svc_integration: OrganizationService):
    """Test retrieve roster for an organization by slug"""
    fetched_members = organization_svc_integration.get_roster(cads.slug)
    assert fetched_members is not None
    assert len(fetched_members) == len(roster)
    assert isinstance(fetched_members[0], OrganizationMembership)


def test_get_nonexistent_roster(organization_svc_integration: OrganizationService):
    """Test retrieving roster for a nonexistent organization"""
    with pytest.raises(ResourceNotFoundException):
        organization_svc_integration.get_roster("fakeslug")


def test_delete_membership(organization_svc_integration: OrganizationService):
    """Test that member can be removed from database"""
    organization_svc_integration.delete_membership(root, cads.slug, member_1.id)

    updated_roster = organization_svc_integration.get_roster(cads.slug)

    assert len(updated_roster) == len(roster) - 1


def test_delete_nonexistent_membership(
    organization_svc_integration: OrganizationService,
):
    """Test that a nonexistent member cannot be removed from database"""
    with pytest.raises(ResourceNotFoundException):
        organization_svc_integration.delete_membership(root, cads.slug, non_member.id)


def test_delete_membership_as_subject(
    organization_svc_integration: OrganizationService,
):
    """Test that a user without admin permissions can remove their own membership"""
    organization_svc_integration.delete_membership(member_2, cads.slug, member_2.id)

    updated_roster = organization_svc_integration.get_roster(cads.slug)

    assert len(updated_roster) == len(roster) - 1


def test_delete_membership_as_user(
    organization_svc_integration: OrganizationService,
):
    """Test that a user without admin permissions cannot remove other members"""
    with pytest.raises(OrganizationPermissionException):
        organization_svc_integration.delete_membership(member_2, cads.slug, member_1.id)


def test_update_existing_membership(organization_svc_integration: OrganizationService):
    """Test an existing member can have their role updated in database"""
    membership = organization_svc_integration.update_membership(
        root, cads.slug, edit_member_2
    )
    assert membership.title == "Treasurer"
    assert membership.permission_level == OrganizationPermissionLevel.ADMIN


def test_update_nonexistent_membership(
    organization_svc_integration: OrganizationService,
):
    """Test that a nonexistent membership cannot be updated"""
    with pytest.raises(ResourceNotFoundException):
        organization_svc_integration.update_membership(
            root,
            cads.slug,
            bad_membership,
        )


def test_update_membership_as_user(
    organization_svc_integration: OrganizationService,
):
    """Test that a user without adminstrative permissions cannot update memberships"""
    with pytest.raises(OrganizationPermissionException):
        organization_svc_integration.update_membership(
            user,
            cads.slug,
            edit_member_2,
        )


# Test Organization Management (roster) end


# Test `OrganizationService.update()`
def test_update_organization_as_root(
    organization_svc_integration: OrganizationService,
):
    """Test that the root user is able to update organizations.
    Note: Test data's website field is updated
    """
    organization_svc_integration.update(root, new_cads)
    assert (
        organization_svc_integration.get_by_slug("cads").website
        == "https://cads.cs.unc.edu/"
    )


def test_update_organization_as_user(organization_svc_integration: OrganizationService):
    """Test that any user is *unable* to update new organizations."""
    with pytest.raises(UserPermissionException):
        organization_svc_integration.update(user, new_cads)


def test_update_organization_does_not_exist(
    organization_svc_integration: OrganizationService,
):
    """Test updating an organization that does not exist."""
    with pytest.raises(ResourceNotFoundException):
        organization_svc_integration.update(root, to_add)


def test_delete_enforces_permission(organization_svc_integration: OrganizationService):
    """Test that the service enforces permissions when attempting to delete an organization."""

    # Setup to test permission enforcement on the PermissionService.
    organization_svc_integration._permission = create_autospec(
        organization_svc_integration._permission
    )

    # Test permissions with root user (admin permission)
    organization_svc_integration.delete(root, cads.slug)
    organization_svc_integration._permission.enforce.assert_called_with(
        root, "organization.delete", "organization"
    )


def test_delete_organization_as_root(organization_svc_integration: OrganizationService):
    """Test that the root user is able to delete organizations."""
    organization_svc_integration.delete(root, cads.slug)
    with pytest.raises(ResourceNotFoundException):
        organization_svc_integration.get_by_slug(cads.slug)


def test_delete_organization_as_user(organization_svc_integration: OrganizationService):
    """Test that any user is *unable* to delete organizations."""
    with pytest.raises(UserPermissionException):
        organization_svc_integration.delete(user, cads.slug)


def test_delete_organization_does_not_exist(
    organization_svc_integration: OrganizationService,
):
    """Test deleting an organization that does not exist."""
    with pytest.raises(ResourceNotFoundException):
        organization_svc_integration.delete(root, to_add.slug)
