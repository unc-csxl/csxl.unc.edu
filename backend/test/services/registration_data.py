"""Mock data for event egistrations."""

import pytest
import datetime
from sqlalchemy.orm import Session
from ...models.registration import Registration
from ...entities.registration_entity import RegistrationEntity

from .reset_table_id_seq import reset_table_id_seq

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

# Sample Data Objects

user_cdc_registration = Registration(id=1, user_id=3, event_id=1, status=0)

registrations = [user_cdc_registration]

to_add = RegistrationEntity(id=1, user_id=3, event_id=2, status=0)

# Data Functions


def insert_fake_data(session: Session):
    """Inserts fake event data into the test session."""

    global registrations

    # Create entities for test registration data
    entities = []
    for registration in registrations:
        entity = RegistrationEntity.from_model(registration)
        session.add(entity)
        entities.append(entity)

    # Reset table IDs to prevent ID conflicts
    reset_table_id_seq(
        session, RegistrationEntity, RegistrationEntity.id, len(registrations) + 1
    )

    # Commit all changes
    session.commit()


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    """Insert fake data the session automatically when test is run.
    Note:
        This function runs automatically due to the fixture property `autouse=True`.
    """
    insert_fake_data(session)
    session.commit()
    yield
