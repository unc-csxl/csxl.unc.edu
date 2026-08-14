"""Tests for Hiring API CSV responses."""

import asyncio
import csv
import io

from ..api.academics.hiring import get_comp_227_matches_for_term_csv


FIELDNAMES = [
    "student_name",
    "pid",
    "email",
    "matching_course",
    "matching_instructor",
    "comp_227_preference",
]


class StubHiringService:
    def __init__(self, rows: list[dict[str, str]]):
        self.rows = rows
        self.calls: list[tuple[object, str]] = []

    def iter_comp_227_matches_for_term_csv(self, subject: object, term_id: str):
        self.calls.append((subject, term_id))
        return iter(self.rows)


def _consume_response(response) -> str:
    async def consume() -> str:
        chunks = []
        async for chunk in response.body_iterator:
            chunks.append(chunk.decode() if isinstance(chunk, bytes) else chunk)
        return "".join(chunks)

    return asyncio.run(consume())


def test_comp_227_matches_csv_empty_result_has_header_and_filename():
    subject = object()
    service = StubHiringService([])

    response = get_comp_227_matches_for_term_csv(
        "2025-spring", subject=subject, hiring_service=service
    )

    assert service.calls == [(subject, "2025-spring")]
    body = _consume_response(response)

    assert body == ",".join(FIELDNAMES) + "\r\n"
    assert response.headers["content-disposition"] == (
        "attachment; filename=comp-227-matches-2025-spring.csv"
    )


def test_comp_227_matches_csv_quotes_and_round_trips_multiple_instructors():
    row = {
        "student_name": "=Student, Sally",
        "pid": "730000000",
        "email": "sally@example.com",
        "matching_course": "COMP 301",
        "matching_instructor": "Ina Instructor, Cole Teacher",
        "comp_227_preference": "COMP 227 credit only",
    }
    service = StubHiringService([row])

    response = get_comp_227_matches_for_term_csv(
        "2025-spring", subject=object(), hiring_service=service
    )
    body = _consume_response(response)

    assert '"Ina Instructor, Cole Teacher"' in body
    assert list(csv.DictReader(io.StringIO(body))) == [
        {**row, "student_name": "'=Student, Sally"}
    ]
