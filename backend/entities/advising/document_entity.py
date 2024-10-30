from sqlalchemy import Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .entity_base import EntityBase
from ...models.advising import document
from backend.models.document import DocumentEnum

class DocumentEntity(EntityBase):
    __tablename__ = "document"

    # Unique ID for the news post
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Title of the document
    title: Mapped[str] = mapped_column(String, nullable=False)

    # Content of the document
    content: Mapped[str] = mapped_column(String, nullable=False) # Might have to change later based on full text search

    # Type of document
    type: Mapped[int] = mapped_column(Integer, nullable=False) # Registration guide = 1, FAQ = 2

    @classmethod
    def from_model(cls, model: document) -> "DocumentEntity":
        """
        Create a DocumentEntity from a Document model.

        Args:
            model (Document): The model to create the entity from.

        Returns:
            DocumentEntity: The entity.
        """
        return cls(
            id=document.id,
            title=document.title,
            content=document.content,
            type=document.type,
        )
    def to_model(self) -> document:
        """
        Create a Document model from a DocumentEntity.

        Returns:
            Document: A Document model for API usage.
        """
        return document(
            id=self.id,
            title=self.title,
            content=self.content,
            type=self.type,
        )
