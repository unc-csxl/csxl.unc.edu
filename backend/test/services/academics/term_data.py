"""Term data for tests."""

import pytest
from sqlalchemy.orm import Session
from ....entities.academics import TermEntity
from ....models.academics import Term
from ..reset_table_id_seq import reset_table_id_seq
from datetime import datetime, timedelta

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

TERM_LENGTH = timedelta(weeks=17)
TERM_GAP = timedelta(weeks=1)

previous_term = Term(
    id="Prev",
    name="Previous Term",
    start=datetime.now() - TERM_GAP - TERM_LENGTH,
    end=datetime.now() - TERM_GAP,
    applications_open=datetime.now() - TERM_GAP - TERM_LENGTH,
    applications_close=datetime.now() - TERM_GAP,
)

current_term = Term(
    id="Curr",
    name="Current Term",
    start=datetime.now(),
    end=datetime.now() + TERM_LENGTH,
    applications_open=datetime.now(),
    applications_close=datetime.now() + TERM_LENGTH,
)

current_term_edited = Term(
    id="Curr",
    name="Current Term Edited",
    start=datetime.now(),
    end=datetime.now() + TERM_LENGTH,
    applications_open=datetime.now(),
    applications_close=datetime.now() + TERM_LENGTH,
)

future_term = Term(
    id="Future",
    name="Future Term",
    start=current_term.end + TERM_GAP,
    end=current_term.end + TERM_GAP + TERM_LENGTH,
    applications_open=current_term.applications_open + TERM_GAP,
    applications_close=current_term.applications_close + TERM_GAP + TERM_LENGTH,
)

terms = [previous_term, current_term]

today = datetime.now()
bad_day = datetime.max


def insert_fake_data(session: Session):
    for term in terms:
        entity = TermEntity.from_model(term)
        session.add(entity)


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    session.commit()
