"""Tests for `update_oh_section_member_role()` in Office Hours Section Service."""

import pytest

from backend.models.academics.section_member import SectionMember, SectionMemberPartial
from backend.models.roster_role import RosterRole
from backend.services.academics.section_member import SectionMemberService

from .....models.office_hours.section_details import OfficeHoursSectionDetails

from .....services.office_hours.section import OfficeHoursSectionService

# Imported fixtures provide dependencies injected for the tests as parameters.
from ..fixtures import permission_svc, oh_section_svc
from ...academics.fixtures import section_member_svc

# Import the setup_teardown fixture explicitly to load entities in database
from ...core_data import setup_insert_data_fixture as insert_order_0
from ...room_data import fake_data_fixture as insert_order_1
from ...academics.term_data import fake_data_fixture as insert_order_2
from ...academics.course_data import fake_data_fixture as insert_order_3
from ...academics.section_data import fake_data_fixture as insert_order_4
from ..office_hours_data import fake_data_fixture as insert_order_5

# Import the fake model data in a namespace for test assertions
from .. import office_hours_data
from ...academics.section_data import (
    user__comp110_instructor,
    user__comp110_student_0,
    user__comp110_student_1,
    user__comp110_uta_0,
    user__comp301_instructor,
    user__comp110_non_member,
    user__comp110_gta,
    term_data,
    comp110_student_0,
    comp110_uta,
    comp110_instructor,
)

__authors__ = ["Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


def test_update_oh_section_member_role_student_to_uta(
    oh_section_svc: OfficeHoursSectionService, section_member_svc: SectionMemberService
):

    section_member_to_change = comp110_student_0
    role_change = RosterRole.UTA
    user_attempting_change = user__comp110_instructor

    delta = SectionMemberPartial(
        id=section_member_to_change.id, member_role=RosterRole.UTA
    )

    # Update
    member = oh_section_svc.update_oh_section_member_role(
        user_attempting_change, delta, office_hours_data.comp_110_oh_section.id
    )

    assert isinstance(member, SectionMember)
    assert member.member_role == role_change

    # Verify
    section_member = section_member_svc.get_section_member_by_id(
        section_member_to_change.id
    )
    section_member.member_role == role_change


def test_update_oh_section_member_role_student_to_gta(
    oh_section_svc: OfficeHoursSectionService, section_member_svc: SectionMemberService
):

    section_member_to_change = comp110_student_0
    role_change = RosterRole.GTA
    user_attempting_change = user__comp110_instructor

    delta = SectionMemberPartial(
        id=section_member_to_change.id, member_role=RosterRole.GTA
    )

    # Update
    member = oh_section_svc.update_oh_section_member_role(
        user_attempting_change, delta, office_hours_data.comp_110_oh_section.id
    )

    assert isinstance(member, SectionMember)
    assert member.member_role == role_change

    # Verify
    section_member = section_member_svc.get_section_member_by_id(
        section_member_to_change.id
    )
    section_member.member_role == role_change


def test_update_oh_section_member_role_uta_to_student(
    oh_section_svc: OfficeHoursSectionService, section_member_svc: SectionMemberService
):

    section_member_to_change = comp110_uta
    role_change = RosterRole.STUDENT
    user_attempting_change = user__comp110_instructor

    delta = SectionMemberPartial(
        id=section_member_to_change.id, member_role=RosterRole.STUDENT
    )

    # Update
    member = oh_section_svc.update_oh_section_member_role(
        user_attempting_change, delta, office_hours_data.comp_110_oh_section.id
    )

    assert isinstance(member, SectionMember)
    assert member.member_role == role_change

    # Verify
    section_member = section_member_svc.get_section_member_by_id(
        section_member_to_change.id
    )
    section_member.member_role == role_change


def test_update_oh_section_member_role_uta_to_student_by_gta(
    oh_section_svc: OfficeHoursSectionService, section_member_svc: SectionMemberService
):

    section_member_to_change = user__comp110_uta_0
    role_change = RosterRole.STUDENT
    user_attempting_change = user__comp110_gta

    delta = SectionMemberPartial(
        id=section_member_to_change.id, member_role=role_change
    )

    # Update
    member = oh_section_svc.update_oh_section_member_role(
        user_attempting_change, delta, office_hours_data.comp_110_oh_section.id
    )

    assert isinstance(member, SectionMember)
    assert member.member_role == role_change

    # Verify
    section_member = section_member_svc.get_section_member_by_id(
        section_member_to_change.id
    )
    section_member.member_role == role_change


def test_update_oh_section_member_role_student_to_uta_by_gta(
    oh_section_svc: OfficeHoursSectionService, section_member_svc: SectionMemberService
):

    section_member_to_change = comp110_student_0
    role_change = RosterRole.UTA
    user_attempting_change = user__comp110_gta

    delta = SectionMemberPartial(
        id=section_member_to_change.id, member_role=role_change
    )

    # Update
    member = oh_section_svc.update_oh_section_member_role(
        user_attempting_change, delta, office_hours_data.comp_110_oh_section.id
    )

    assert isinstance(member, SectionMember)
    assert member.member_role == role_change

    # Verify
    section_member = section_member_svc.get_section_member_by_id(
        section_member_to_change.id
    )
    section_member.member_role == role_change


def test_update_oh_section_member_role_student_to_gta_by_gta(
    oh_section_svc: OfficeHoursSectionService, section_member_svc: SectionMemberService
):

    section_member_to_change = comp110_student_0
    role_change = RosterRole.GTA
    user_attempting_change = user__comp110_gta

    delta = SectionMemberPartial(
        id=section_member_to_change.id, member_role=role_change
    )

    # Update
    member = oh_section_svc.update_oh_section_member_role(
        user_attempting_change, delta, office_hours_data.comp_110_oh_section.id
    )

    assert isinstance(member, SectionMember)
    assert member.member_role == role_change

    # Verify
    section_member = section_member_svc.get_section_member_by_id(
        section_member_to_change.id
    )
    section_member.member_role == role_change


def test_update_oh_section_member_role_exception_if_by_uta(
    oh_section_svc: OfficeHoursSectionService,
):

    section_member_to_change = comp110_student_0
    role_change = RosterRole.GTA
    user_attempting_change = user__comp110_uta_0

    delta = SectionMemberPartial(
        id=section_member_to_change.id, member_role=role_change
    )

    # Update
    with pytest.raises(PermissionError):
        oh_section_svc.update_oh_section_member_role(
            user_attempting_change, delta, office_hours_data.comp_110_oh_section.id
        )
        pytest.fail()


def test_update_oh_section_member_role_exception_if_by_student(
    oh_section_svc: OfficeHoursSectionService,
):

    section_member_to_change = comp110_student_0
    delta = SectionMemberPartial(
        id=section_member_to_change.id, member_role=RosterRole.GTA
    )

    # Update
    with pytest.raises(PermissionError):
        oh_section_svc.update_oh_section_member_role(
            user__comp110_student_1, delta, office_hours_data.comp_110_oh_section.id
        )
        pytest.fail()


def test_update_oh_section_member_role_exception_if_non_member(
    oh_section_svc: OfficeHoursSectionService,
):

    section_member_to_change = comp110_student_0
    role_change = RosterRole.GTA
    user_attempting_change = user__comp110_non_member

    delta = SectionMemberPartial(
        id=section_member_to_change.id, member_role=role_change
    )

    # Update
    with pytest.raises(PermissionError):
        oh_section_svc.update_oh_section_member_role(
            user_attempting_change, delta, office_hours_data.comp_110_oh_section.id
        )
        pytest.fail()


def test_update_oh_section_member_role_exception_if_gta_downgrades_instructor(
    oh_section_svc: OfficeHoursSectionService,
):

    section_member_to_change = comp110_instructor
    role_change = RosterRole.STUDENT
    user_attempting_change = user__comp110_gta

    delta = SectionMemberPartial(
        id=section_member_to_change.id, member_role=role_change
    )

    # Update
    with pytest.raises(PermissionError):
        oh_section_svc.update_oh_section_member_role(
            user_attempting_change, delta, office_hours_data.comp_110_oh_section.id
        )
        pytest.fail()


def test_update_oh_section_member_role_exception_if_uta_downgrades_instructor(
    oh_section_svc: OfficeHoursSectionService,
):

    section_member_to_change = comp110_instructor
    role_change = RosterRole.STUDENT
    user_attempting_change = user__comp110_uta_0

    delta = SectionMemberPartial(
        id=section_member_to_change.id, member_role=role_change
    )

    # Update
    with pytest.raises(PermissionError):
        oh_section_svc.update_oh_section_member_role(
            user_attempting_change, delta, office_hours_data.comp_110_oh_section.id
        )
        pytest.fail()


def test_update_oh_section_member_role_exception_if_non_member(
    oh_section_svc: OfficeHoursSectionService, section_member_svc: SectionMemberService
):

    invalid_section_member_id = 99
    role_change = RosterRole.UTA
    user_attempting_change = user__comp110_instructor

    delta = SectionMemberPartial(id=invalid_section_member_id, member_role=role_change)

    with pytest.raises(PermissionError):
        oh_section_svc.update_oh_section_member_role(
            user_attempting_change, delta, office_hours_data.comp_110_oh_section.id
        )
        pytest.fail()
