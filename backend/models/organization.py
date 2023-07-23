from pydantic import BaseModel

class Organization(BaseModel):
    """
    Model to represent an `OrganizationDetail` object in a relationship

    This model is based on the `OrganizationDetail` model, which defines the shape
    of the `OrganizationDetail` database in the PostgreSQL database

    This model exists to prevent infinite recursion with bidirectional
    relationship mapping.
    """

    id: int | None=None
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