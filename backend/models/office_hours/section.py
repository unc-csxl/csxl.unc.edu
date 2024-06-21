from pydantic import BaseModel

__authors__ = ["Sadie Amato, Bailey DeSouza, Meghan Sun, Maddy Andrews"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OfficeHoursSectionDraft(BaseModel):
    """
    Pydantic model to represent an `OfficeHoursSection` that has not been created yet.

    This model is based on the `CourseSiteEntity` model, which defines the shape
    of the `OfficeHoursSection` database in the PostgreSQL database.
    """

    title: str


class OfficeHoursSection(OfficeHoursSectionDraft):
    """
    Pydantic model to represent an `OfficeHoursSection`.

    This model is based on the `CourseSiteEntity` model, which defines the shape
    of the `OfficeHoursSection` database in the PostgreSQL database.
    """

    id: int
    term_id: str


class OfficeHoursSectionPartial(OfficeHoursSection):
    """
    Pydantic model to represent a partial `OfficeHoursSection`.

    This model is based on the `CourseSiteEntity` model, which defines the shape
    of the `OfficeHoursSection` database in the PostgreSQL database.
    """

    title: str | None = None
