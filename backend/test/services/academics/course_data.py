"""Course data for tests."""

import pytest
from sqlalchemy.orm import Session
from ....entities.academics import CourseEntity
from ....models.academics import Course
from ..reset_table_id_seq import reset_table_id_seq
from datetime import datetime

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

comp_110 = Course(
    id="comp110",
    subject_code="COMP",
    number="110",
    title="Introduction to Programming and Data Science",
    description="Introduces students to programming and data science from a computational perspective. With an emphasis on modern applications in society, students gain experience with problem decomposition, algorithms for data analysis, abstraction design, and ethics in computing. No prior programming experience expected. Foundational concepts include data types, sequences, boolean logic, control flow, functions/methods, recursion, classes/objects, input/output, data organization, transformations, and visualizations.",
    credit_hours=3,
)

comp_210 = Course(
    id="comp210",
    subject_code="COMP",
    number="210",
    title="Data Structures and Analysis",
    description="This course will teach you how to organize the data used in computer programs so that manipulation of that data can be done efficiently on large problems and large data instances. Rather than learning to use the data structures found in the libraries of programming languages, you will be learning how those libraries are constructed, and why the items that are included in them are there (and why some are excluded).",
    credit_hours=3,
)

comp_301 = Course(
    id="comp301",
    subject_code="COMP",
    number="301",
    title="Foundations of Programming",
    description="Students will learn how to reason about how their code is structured, identify whether a given structure is effective in a given context, and look at ways of organizing units of code that support larger programs. In a nutshell, the primary goal of the course is to equip students with tools and techniques that will help them not only in later courses in the major but also in their careers afterwards.",
    credit_hours=3,
)

comp_523 = Course(
    id="comp523",
    subject_code="COMP",
    number="523",
    title="Software Engineering Lab",
    description="Work with Clients to Build Projects",
    credit_hours=4,
)

edited_comp_110 = Course(
    id="comp110",
    subject_code="COMP",
    number="110",
    title="Introduction to Programming",
    description="Introduces students to programming and data science from a computational perspective. With an emphasis on modern applications in society, students gain experience with problem decomposition, algorithms for data analysis, abstraction design, and ethics in computing. No prior programming experience expected. Foundational concepts include data types, sequences, boolean logic, control flow, functions/methods, recursion, classes/objects, input/output, data organization, transformations, and visualizations.",
    credit_hours=3,
)

new_course = Course(
    id="comp423",
    subject_code="COMP",
    number="423",
    title="Foundations of Software Engineering",
    description="Best course in the department : )",
    credit_hours=3,
)

courses = [comp_110, comp_210, comp_301, comp_523]


def insert_fake_data(session: Session):
    for course in courses:
        entity = CourseEntity.from_model(course)
        session.add(entity)


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    session.commit()
