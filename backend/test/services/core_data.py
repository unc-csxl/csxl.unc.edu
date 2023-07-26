"""Helper data file that is used commonly for users, roles, and permissions.

Rather than importing each of these data insertion fixtures directly into tests,
this module serves as a helper to bring them all in at once.
"""

import pytest
from sqlalchemy.orm import Session
from . import user_data
from . import role_data
from . import permission_data
from . import organization_data
from . import event_data
from . import org_role_data


@pytest.fixture(autouse=True)
def setup_insert_data_fixture(session: Session):
    role_data.insert_fake_data(session)
    user_data.insert_fake_data(session)
    permission_data.insert_fake_data(session)
    organization_data.insert_fake_data(session)
    event_data.insert_fake_data(session)
    org_role_data.insert_fake_data(session)
    session.commit()
    yield
