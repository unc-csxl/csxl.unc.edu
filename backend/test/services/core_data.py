"""Helper data file that is used commonly for users, roles, and permissions.

Rather than importing each of these data insertion fixtures directly into tests,
this module serves as a helper to bring them all in at once.
"""

import pytest
from sqlalchemy.orm import Session
from .organization import organization_test_data
from .event import event_test_data
from . import permission_data, role_data, user_data
from .academics import section_data, term_data, course_data
from .office_hours import office_hours_data

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


@pytest.fixture(autouse=True)
def setup_insert_data_fixture(session: Session):
    role_data.insert_fake_data(session)
    user_data.insert_fake_data(session)
    permission_data.insert_fake_data(session)
    organization_test_data.insert_fake_data(session)
    event_test_data.insert_fake_data(session)
    # term_data.insert_fake_data(session)
    # course_data.insert_fake_data(session)
    # section_data.insert_fake_data(session)
    # office_hours_data.insert_fake_data(session)
    session.commit()
    yield
