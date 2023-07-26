"""Helper data file that is used commonly for users, roles, and permissions.

Rather than importing each of these data insertion fixtures directly into tests,
this module serves as a helper to bring them all in at once.
"""

import pytest
from sqlalchemy.orm import Session
from . import user_data
from . import role_data
from . import permission_data


@pytest.fixture(autouse=True)
def setup_insert_data_fixture(test_session: Session):
    role_data.insert_fake_data(test_session)
    user_data.insert_fake_data(test_session)
    permission_data.insert_fake_data(test_session)
    test_session.commit()
    yield
