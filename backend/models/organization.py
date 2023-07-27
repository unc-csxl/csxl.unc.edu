from pydantic import BaseModel

__authors__ = ["Ajay Gandecha", "Jade Keegan", "Brianna Ta", "Audrey Toney"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class Organization(BaseModel):
    """
    Model to represent an `OrganizationDetail` object in a relationship

    This model is based on the `OrganizationDetail` model, which defines the shape
    of the `OrganizationDetail` database in the PostgreSQL database

    This model exists to prevent infinite recursion with bidirectional
    relationship mapping.
    """

    id: int | None = None
    name: str
    slug: str
    logo: str
    short_description: str
    long_description: str
    website: str
    email: str
    instagram: str
    linked_in: str
    youtube: str
    heel_life: str
    public: bool
