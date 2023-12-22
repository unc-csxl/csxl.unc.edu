"""Courses Course API

This API is used to access course data."""

from fastapi import APIRouter, Depends
from ..authentication import registered_user
from ...services.courses import CourseService
from ...models import User
from ...models.courses import Course, CourseDetails

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


api = APIRouter(prefix="/api/courses/course")


@api.get("", response_model=list[CourseDetails], tags=["Courses"])
def get_courses(course_service: CourseService = Depends()) -> list[CourseDetails]:
    """
    Get all courses

    Returns:
        list[CourseDetails]: All `Course`s in the `Course` database table
    """
    return course_service.all()


@api.get("/{id}", response_model=CourseDetails, tags=["Courses"])
def get_course_by_id(
    id: str, course_service: CourseService = Depends()
) -> CourseDetails:
    """
    Gets one course by its id

    Returns:
        CourseDetails: Course with the given ID
    """
    return course_service.get_by_id(id)


@api.get("/{subject_code}/{number}", response_model=CourseDetails, tags=["Courses"])
def get_course_by_subject_code(
    subject_code: str, number: str, course_service: CourseService = Depends()
) -> CourseDetails:
    """
    Gets one course by its properties

    Returns:
        CourseDetails: Course with the given ID
    """
    return course_service.get(subject_code, number)


@api.post("", response_model=CourseDetails, tags=["Courses"])
def new_course(
    course: Course,
    subject: User = Depends(registered_user),
    course_service: CourseService = Depends(),
) -> CourseDetails:
    """
    Adds a new course to the database

    Returns:
        CourseDetails: Course created
    """
    return course_service.create(subject, course)


@api.put("", response_model=CourseDetails, tags=["Courses"])
def update_course(
    course: Course,
    subject: User = Depends(registered_user),
    course_service: CourseService = Depends(),
) -> CourseDetails:
    """
    Updates a course to the database

    Returns:
        CourseDetails: Course updated
    """
    return course_service.update(subject, course)


@api.delete("", response_model=None, tags=["Courses"])
def delete_course(
    course: Course,
    subject: User = Depends(registered_user),
    course_service: CourseService = Depends(),
):
    """
    Deletes a course from the database
    """
    return course_service.delete(subject, course)