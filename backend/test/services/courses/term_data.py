"""Term data for tests."""

import pytest
from sqlalchemy.orm import Session
from ....entities.courses import TermEntity
from ....models.courses import Term
from ..reset_table_id_seq import reset_table_id_seq
from datetime import datetime

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


sp_23 = Term(
    id="S23", name="Spring 2023", start=datetime(2023, 1, 10), end=datetime(2023, 5, 10)
)

f_23 = Term(
    id="F23", name="Fall 2023", start=datetime(2023, 8, 20), end=datetime(2023, 12, 15)
)

edited_f_23 = Term(
    id="F23",
    name="Best Semester Ever",
    start=datetime(2023, 8, 20),
    end=datetime(2023, 12, 15),
)

sp_24 = Term(
    id="S24", name="Spring 2024", start=datetime(2024, 1, 10), end=datetime(2024, 5, 10)
)

new_term = Term(
    id="F24", name="Fall 2024", start=datetime(2024, 8, 20), end=datetime(2024, 12, 15)
)

terms = [sp_23, f_23, sp_24]

today = datetime(2023, 12, 1)
bad_day = datetime(3000, 1, 1)


def insert_fake_data(session: Session):
    for term in terms:
        entity = TermEntity.from_model(term)
        session.add(entity)


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    session.commit()
