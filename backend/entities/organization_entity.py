from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .entity_base import EntityBase
from typing import Self
from backend.models import Role
from backend.models.organization import Organization, OrganizationSummary

class OrganizationEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Organization` table"""

    __tablename__ = "organization"

    # Unique ID for the organization
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Name of the organization
    name: Mapped[str] = mapped_column(String)
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
    # All of the events hosted by the organization
        # Generated from a relationship with the "events" table
        # Back-populates the `organization` field of `EventEntity`
    events: Mapped[list["EventEntity"]] = relationship(back_populates="organization", cascade="all, delete")

    users: Mapped[list["UserEntity"]] = relationship(secondary="org_role", back_populates="organizations")
    user_associations: Mapped[list["OrgRoleEntity"]] = relationship(back_populates="organization")


    @classmethod
    def from_model(cls, model: Organization) -> Self:
        """
        Class method that converts a `Organization` object into a `OrganizationEntity`
        
        Parameters:
            - model (Organization): Model to convert into an entity

        Returns:
            OrganizationEntity: Entity created from model
        """
        return cls(id=model.id, name=model.name, logo=model.logo, short_description=model.short_description, long_description=model.long_description, website=model.website, email=model.email, instagram=model.instagram, linked_in=model.linked_in, youtube=model.youtube, heel_life=model.heel_life)

    def to_model(self) -> Organization:
        """
        Converts a `OrganizationEntity` object into a `Organization`
        
        Returns:
            Organization: `Organization` object from the entity
        """
        from backend.models.event import Event
        from backend.entities.event_entity import EventEntity

        return Organization(id=self.id, 
                            name=self.name, 
                            logo=self.logo, 
                            short_description=self.short_description, 
                            long_description=self.long_description, 
                            website=self.website, 
                            email=self.email, 
                            instagram=self.instagram, 
                            linked_in=self.linked_in, 
                            youtube=self.youtube, 
                            heel_life=self.heel_life, 
                            events=[event.to_model() for event in self.events],
                            users=[user.to_summary() for user in self.users],
                            user_associations=[association.to_model() for association in self.user_associations])
    
    def to_summary(self) -> OrganizationSummary:
        """
        Converts a `OrganizationEntity` object into a `OrganizationSummary`
        
        Returns:
            Organization: `OrganizationSummary` object from the entity
        """

        return OrganizationSummary(id=self.id, 
                            name=self.name, 
                            logo=self.logo, 
                            short_description=self.short_description, 
                            long_description=self.long_description, 
                            website=self.website, 
                            email=self.email, 
                            instagram=self.instagram, 
                            linked_in=self.linked_in, 
                            youtube=self.youtube, 
                            heel_life=self.heel_life)

from backend.entities.user_entity import UserEntity
from backend.entities.org_role_entity import OrgRoleEntity