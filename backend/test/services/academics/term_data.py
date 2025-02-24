"""Term data for tests."""

import pytest
from sqlalchemy.orm import Session
from ....entities.academics import TermEntity
from ....models.academics import Term
from ..reset_table_id_seq import reset_table_id_seq
from datetime import datetime

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


sp_23 = Term(
    id="23S", name="Spring 2023", start=datetime(2023, 1, 10), end=datetime(2023, 5, 10)
)

f_23 = Term(
    id="23F", name="Fall 2023", start=datetime(2023, 8, 20), end=datetime(2023, 12, 15)
)

edited_f_23 = Term(
    id="23F",
    name="Best Semester Ever",
    start=datetime(2023, 8, 20),
    end=datetime(2023, 12, 15),
)

sp_24 = Term(
    id="24S", name="Spring 2024", start=datetime(2024, 1, 10), end=datetime(2024, 5, 10)
)

ss1_24 = Term(
    id="24SuI",
    name="Summer Session I 2024",
    start=datetime(2024, 5, 13),
    end=datetime(2024, 6, 23),
)

ss2_24 = Term(
    id="SuII24",
    name="Summer Session II 2024",
    start=datetime(2024, 6, 23),
    end=datetime(2024, 8, 30),
    applications_open=datetime(2024, 6, 30),
    applications_close=datetime(2024, 8, 30),
)

f24 = Term(
    id="24F", name="Fall 2024", start=datetime(2024, 8, 20), end=datetime(2024, 12, 31)
)

s25 = Term(
    id="25S", name="Spring 2025", start=datetime(2025, 1, 1), end=datetime(2025, 5, 31)
)

terms = [sp_23, f_23, sp_24, ss1_24, ss2_24, f24, s25]

current_term = s25

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
