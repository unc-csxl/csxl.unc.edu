"""Scrapes and loads course data from the UNC Course Catalog into the backend database.

Usage: python3 -m script.scrapers.academics.courses
"""

from bs4 import BeautifulSoup
import requests
from pydantic import BaseModel
from ....models.academics.course import Course
from ....entities.academics.course_entity import CourseEntity
from sqlalchemy.orm import Session
from ....database import engine

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class DepartmentData:
    """
    Custom model to represent department catalog scraped from the catalog.
    """

    code: str
    name: str
    url_suffix: str

    def __init__(self, code: str, name: str, url_suffix: str):
        self.code = code
        self.name = name
        self.url_suffix = url_suffix


def scrape_department_data() -> list[DepartmentData]:
    """
    Function that scrapes the UNC catalog to retrieve data on UNC departments.

    Returns:
        list[DepartmentData]: List of departments scraped from the catalog.
    """

    # URL to scrape data from
    url = "https://catalog.unc.edu/courses/"
    # Retrieve HTML from HTTP response content
    html = requests.get(url).content
    # Create BeautifulSoup object to parse HTML
    soup = BeautifulSoup(html, "html.parser")

    # Select HTML elements in the A-Z Department list
    dept_list = soup.find("div", id="atozindex")

    # Select all list items from the department list and select links
    dept_list_items = dept_list.find_all("li")
    depts = []
    for list_item in dept_list_items:
        depts += list_item.find_all("a", href=True)

    # Parse data
    data = []
    for dept in depts:
        code = dept.text.split("(")[1].split(")")[0].strip().lower()
        dept_name = dept.text.split("(")[0].title()
        url_suffix = dept["href"]
        data.append(DepartmentData(code=code, name=dept_name, url_suffix=url_suffix))

    # Return data
    return data


def scrape_courses_for_department(dept: DepartmentData) -> list[Course]:
    """
    Retrieves data for courses in a single department.

    Parameters:
        dept: The department to scrape data for.

    Returns:
        list[Course]: List of course data scraped.
    """

    # URL to scrape data from
    url = "https://catalog.unc.edu" + dept.url_suffix
    # Retrieve HTML from HTTP response content
    html = requests.get(url).content
    # Create BeautifulSoup object to parse HTML
    soup = BeautifulSoup(html, "html.parser")

    # Retrieve all course block divs
    course_blocks = soup.find_all("div", class_="courseblock")

    # Scrape data for each course
    courses = []
    for course_block in course_blocks:
        course = (
            course_block.find("span", class_="detail-code")
            .text.replace(".", "")
            .strip()
        )
        course_subject_code = course.split(" ")[0]
        course_number = course.split(" ")[1]
        course_title = (
            course_block.find("span", class_="detail-title")
            .text.replace(".", "")
            .strip()
        )
        course_description = ""
        try:
            course_description = course_block.find(
                "p", class_="courseblockextra"
            ).text.strip()
        except:
            ...
        credits = (
            course_block.find("span", class_="detail-hours")
            .text.replace(".", "")
            .strip()
            .split(" ")[0]
            .split("-")[-1]
        )

        course_model = Course(
            id=course_subject_code.lower() + str(course_number),
            subject_code=course_subject_code,
            number=course_number,
            title=course_title,
            description=course_description,
            credit_hours=credits,
        )

        courses.append(course_model)

    # Return scraped courses
    return courses


def scrape_course_data(show_logs: bool = True) -> list[Course]:
    """
    Scrapes all of the data for all of courses in the UNC course catalog.

    Returns:
        list[CourseModel]: Returns the list of courses as Course Pydantic models.
    """

    # Create list to store final list of courses
    courses = []

    # Find all deparments to scrape data for
    departments = scrape_department_data()

    # Scrape data for each department
    for department in departments:
        if show_logs:
            print("Scraping data for:", department.name)
        dept_courses = scrape_courses_for_department(department)
        courses += dept_courses

    return courses


def insert_scraped_data(session: Session):
    """Inserts the scraped data from the script into the database."""
    for course in scrape_course_data(show_logs=False):
        entity = CourseEntity.from_model(course)
        session.add(entity)
