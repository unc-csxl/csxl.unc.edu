"""Contains mock data for to run tests on the test feature."""

import pytest
from sqlalchemy.orm import Session
from ....models.log import Log
from ....entities.log_entity import LogEntity

from ..reset_table_id_seq import reset_table_id_seq

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

# Sample Data Objects

log_one = Log(id=1, description="Added an organization.", user_id=1)

log_two = Log(id=2, description="Deleted an event.", user_id=2)

logs = [log_one, log_two]

# Data Functions


def insert_fake_data(session: Session):
    """Inserts fake organization data into the test session."""

    global organizations

    # Create entities for test data
    entities = []
    for log in logs:
        entity = LogEntity.from_model(log)
        session.add(entity)
        entities.append(entity)

    # Reset table IDs to prevent ID conflicts
    reset_table_id_seq(session, LogEntity, LogEntity.id, len(logs) + 1)

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
