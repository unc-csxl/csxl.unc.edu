from sqlalchemy import Integer, String, Boolean, ForeignKey, DateTime, func, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..entity_base import EntityBase
from ...models.academic_advising.document import Document
from ...models.academic_advising.document_details import DocumentDetails
from typing import Self


class DocumentEntity(EntityBase):
    __tablename__ = "document"

    # Unique ID for the news post
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Title of the document
    title: Mapped[str] = mapped_column(String, nullable=False)


    # NOTE: This field establishes a one-to-many relationship between the documents and sections table.
    doc_sections: Mapped[list["DocumentSectionEntity"]] = relationship(
        back_populates="document", cascade="all,delete"
    )
   

    @classmethod
    def from_model(cls, model: Document) -> Self:
        """
        Create a DocumentEntity from a Document model.

        Args:
            model (Document): The model to create the entity from.

        Returns:
            DocumentEntity: The entity.
        """
        return cls(
            id=model.id,
            title=model.title
        )
    
    def to_model(self) -> Document:
        """
        Create a Document model from a DocumentEntity.

        Returns:
            Document: A Document model for API usage.
        """
        return Document(
            id=self.id,
            title=self.title,
        )
    
    def to_details_model(self) -> DocumentDetails:
        """
        Converts a `DocumentEntity` object into a `DocumentDetails` model object

        Returns:
            DocumentDetails: `DocumentDetails` object from the entity
        """
        return DocumentDetails(
            id=self.id,
            title=self.title,
            sections=[section.to_model() for section in self.sections],
        )

