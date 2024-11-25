from datetime import date, datetime, time
import pytest
from sqlalchemy.orm import Session
from ....models.academic_advising.drop_in import DropIn
from ....entities.academic_advising import DropInEntity
from ..reset_table_id_seq import reset_table_id_seq

# drop in objects after API parsing + committing to table
drop_in_one = DropIn(
    id=1,
    title="KMP Advising",
    date=date(2024, 11, 29),
    start=time(8, 0, 0, 0),
    end=time(9, 0, 0, 0),
    link="www.calendar.google.com",
)

drop_in_two = DropIn(
    id=2,
    title="Brent Advising",
    date=date(2024, 11, 30),
    start=time(9, 0, 0, 0),
    end=time(10, 0, 0, 0),
    link="www.calendar.google.com",
)


# for testing parse_events()
sample_response = {'kind': 'calendar#events', 'etag': '"p320el24unnmoi0o"', 'summary': 'CS Advising Team (For Current Students)', 'description': 'Make Appointments to see students for advising and program of study planning.', 'updated': '2024-11-21T12:58:47.968Z', 'timeZone': 'America/New_York', 'accessRole': 'reader', 'defaultReminders': [], 'nextPageToken': 'EjgKNhI0CgYI-NKXugYSKhIoChwKGnJrNWpjbzZsdWw3ZTUxYjBvdGJ0MnA5ZWNtEggKBgj43fK5BsA-AQ==', 'items': [{'kind': 'calendar#event', 'etag': '"3463898625890000"', 'id': '7n61ivno7241tqtrrpac55v7aa_20241125T180000Z', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=N242MWl2bm83MjQxdHF0cnJwYWM1NXY3YWFfMjAyNDExMjVUMTgwMDAwWiBjcy51bmMuZWR1XzM0MG9vbnI0ZWMyNm4xZm85bDg1NHIzaXA4QGc', 'created': '2024-08-01T16:11:44.000Z', 'updated': '2024-11-18T17:01:52.945Z', 'summary': 'Brent -Advising', 'description': '<a href="https://zoom.us/j/98584874906" target="_blank"><u>https://zoom.us/j/98584874906</u></a>', 'creator': {'email': 'munsell@cs.unc.edu'}, 'organizer': {'email': 'cs.unc.edu_340oonr4ec26n1fo9l854r3ip8@group.calendar.google.com', 'displayName': 'CS Advising Team (For Current Students)', 'self': True}, 'start': {'dateTime': '2024-11-25T13:00:00-05:00', 'timeZone': 'America/New_York'}, 'end': {'dateTime': '2024-11-25T14:00:00-05:00', 'timeZone': 'America/New_York'}, 'recurringEventId': '7n61ivno7241tqtrrpac55v7aa', 'originalStartTime': {'dateTime': '2024-11-25T13:00:00-05:00', 'timeZone': 'America/New_York'}, 'iCalUID': '7n61ivno7241tqtrrpac55v7aa@google.com', 'sequence': 0, 'reminders': {'useDefault': True}, 'eventType': 'default'}, {'kind': 'calendar#event', 'etag': '"3463038203872000"', 'id': 'rk5jco6lul7e51b0otbt2p9ecm_20241126T153000Z', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=cms1amNvNmx1bDdlNTFiMG90YnQycDllY21fMjAyNDExMjZUMTUzMDAwWiBjcy51bmMuZWR1XzM0MG9vbnI0ZWMyNm4xZm85bDg1NHIzaXA4QGc', 'created': '2024-08-13T16:35:36.000Z', 'updated': '2024-11-13T17:31:41.936Z', 'summary': 'KMP Advising', 'location': 'https://unc.zoom.us/j/99147066273', 'creator': {'email': 'kmp@cs.unc.edu', 'displayName': 'Ketan Mayer-Patel'}, 'organizer': {'email': 'cs.unc.edu_340oonr4ec26n1fo9l854r3ip8@group.calendar.google.com', 'displayName': 'CS Advising Team (For Current Students)', 'self': True}, 'start': {'dateTime': '2024-11-26T10:30:00-05:00', 'timeZone': 'America/New_York'}, 'end': {'dateTime': '2024-11-26T11:30:00-05:00', 'timeZone': 'America/New_York'}, 'recurringEventId': 'rk5jco6lul7e51b0otbt2p9ecm_R20241119T153000', 'originalStartTime': {'dateTime': '2024-11-26T10:30:00-05:00', 'timeZone': 'America/New_York'}, 'iCalUID': 'rk5jco6lul7e51b0otbt2p9ecm_R20241119T153000@google.com', 'sequence': 2, 'reminders': {'useDefault': True}, 'eventType': 'default'}]}

sample_parsed_response = {'7n61ivno7241tqtrrpac55v7aa_20241125T180000Z': {'summary': 'Brent Advising', 'start': time(13, 0), 'end': time(14, 0), 'date': date(2024, 11, 25), 'link': 'https://www.google.com/calendar/event?eid=N242MWl2bm83MjQxdHF0cnJwYWM1NXY3YWFfMjAyNDExMjVUMTgwMDAwWiBjcy51bmMuZWR1XzM0MG9vbnI0ZWMyNm4xZm85bDg1NHIzaXA4QGc'}, 'rk5jco6lul7e51b0otbt2p9ecm_20241126T153000Z': {'summary': 'KMP Advising', 'start': time(10, 30), 'end': time(11, 30), 'date': date(2024, 11, 26), 'link': 'https://www.google.com/calendar/event?eid=cms1amNvNmx1bDdlNTFiMG90YnQycDllY21fMjAyNDExMjZUMTUzMDAwWiBjcy51bmMuZWR1XzM0MG9vbnI0ZWMyNm4xZm85bDg1NHIzaXA4QGc'}}


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
