"""Helper data file that is used commonly for users, roles, and permissions.

Rather than importing each of these data insertion fixtures directly into tests,
this module serves as a helper to bring them all in at once.
"""

import pytest
from sqlalchemy.orm import Session
from .organization import organization_test_data
from . import permission_data, role_data, user_data

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

@pytest.fixture(autouse=True)
def setup_insert_data_fixture(session: Session):
    role_data.insert_fake_data(session)
    user_data.insert_fake_data(session)
    permission_data.insert_fake_data(session)
    organization_test_data.insert_fake_data(session)
    
    session.commit()
    yield
