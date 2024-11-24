from datetime import date, time
import pytest
from sqlalchemy.orm import Session
from ....models.academic_advising.drop_in import DropIn
from ....entities.academic_advising import DropInEntity
from ..reset_table_id_seq import reset_table_id_seq

drop_in_one = DropIn(
    id=1,
    title="KMP Advising",
    date=date(2024, 11, 29),
    start=time(8,0),
    end=time(9,0),
    link="www.calendar.google.com"
)

drop_in_two = DropIn(
    id=2,
    title="Brent Advising",
    date=date(2024, 11, 30),
    start=time(9,0),
    end=time(10,0),
    link="www.calendar.google.com"
)

drop_ins = [drop_in_one, drop_in_two]

def insert_fake_data(session: Session):
    """Inserts fake event data into the test session."""

    global drop_ins

    # Create entities for test event data
    entities = []
    for drop_in in drop_ins:
        drop_in_entity = DropInEntity.from_model(drop_in)
        session.add(drop_in_entity)
        entities.append(drop_in_entity)

    session.commit()

    # Reset table IDs to prevent ID conflicts
    reset_table_id_seq(session, DropInEntity, DropInEntity.id, len(drop_ins) + 1)

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
