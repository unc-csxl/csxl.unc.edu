"""Definition of SQLAlchemy table-backed object mapping entity for OrganizationEntity."""

from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .entity_base import EntityBase
from typing import Self
from ..models.organization import Organization
from ..models.organization_details import OrganizationDetails

__authors__ = ["Ajay Gandecha", "Jade Keegan", "Brianna Ta", "Audrey Toney"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

class OrganizationEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Organization` table"""

    __tablename__ = "organization"

    # Unique ID for the organization
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Name of the organization
    name: Mapped[str] = mapped_column(String, nullable=False, default="")
    # Short hand name of the organization
    shorthand: Mapped[str] = mapped_column(String, nullable=False)
    # Slug of the organization
    slug: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    # Logo of the organization
    logo: Mapped[str] = mapped_column(String)
    # Short description of the organization
    short_description: Mapped[str] = mapped_column(String)
    # Long description of the organization
    long_description: Mapped[str] = mapped_column(String)
    # Website of the organization
    website: Mapped[str] = mapped_column(String)
    # Contact email for the organization
    email: Mapped[str] = mapped_column(String)
    # Instagram username for the organization
    instagram: Mapped[str] = mapped_column(String)
    # LinkedIn for the organization
    linked_in: Mapped[str] = mapped_column(String)
    # YouTube for the organization
    youtube: Mapped[str] = mapped_column(String)
    # Heel Life for the organization
    heel_life: Mapped[str] = mapped_column(String)
    # Whether the organization can be joined by anyone or not
    public: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    # Holds a list of events that the organization hosts
    events: Mapped[list['EventEntity']] = relationship(back_populates="organization", cascade="all,delete")

    @classmethod
    def from_model(cls, model: Organization) -> Self:
        """
        Class method that converts a `Organization` object into a `OrganizationEntity`

        Parameters:
            - model (Organization): Model to convert into an entity

        Returns:
            OrganizationEntity: Entity created from model
        """
        return cls(
            id=model.id,
            name=model.name,
            shorthand=model.shorthand,
            slug=model.slug,
            logo=model.logo,
            short_description=model.short_description,
            long_description=model.long_description,
            website=model.website,
            email=model.email,
            instagram=model.instagram,
            linked_in=model.linked_in,
            youtube=model.youtube,
            heel_life=model.heel_life,
            public=model.public,
        )

    def to_model(self) -> Organization:
        """
        Converts a `OrganizationEntity` object into a `Organization`

        Returns:
            Organization: `Organization` object from the entity
        """
        return Organization(
            id=self.id,
            name=self.name,
            shorthand=self.shorthand,
            slug=self.slug,
            logo=self.logo,
            short_description=self.short_description,
            long_description=self.long_description,
            website=self.website,
            email=self.email,
            instagram=self.instagram,
            linked_in=self.linked_in,
            youtube=self.youtube,
            heel_life=self.heel_life,
            public=self.public
        )
        
    def to_details_model(self) -> OrganizationDetails:
        """Create a RoleDetails model from a RoleEntity, with permissions and members included.

        Returns:
            RoleDetails: A RoleDetails model for API usage.
        """
        return OrganizationDetails(
            id=self.id,
            name=self.name,
            shorthand=self.shorthand,
            slug=self.slug,
            logo=self.logo,
            short_description=self.short_description,
            long_description=self.long_description,
            website=self.website,
            email=self.email,
            instagram=self.instagram,
            linked_in=self.linked_in,
            youtube=self.youtube,
            heel_life=self.heel_life,
            public=self.public,
            events=self.events
        )