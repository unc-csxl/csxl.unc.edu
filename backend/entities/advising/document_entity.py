from sqlalchemy import Integer, String, Boolean, ForeignKey, DateTime, func, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .entity_base import EntityBase
from ...models.advising import document
from backend.models.document import DocumentEnum

class DocumentEntity(EntityBase):
    __tablename__ = "document"

    # Unique ID for the document
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Title of the document
    title: Mapped[str] = mapped_column(String, nullable=False)

    # Tsvector for full-text search
    tsv_content: Mapped[str] = mapped_column(
        "tsv_content", 
        type_=String, 
        index=True,
        nullable=False,
    )

    # Create a GIN index on the tsv_content column
    __table_args__ = (
        Index('ix_document_tsv_content', tsv_content, postgresql_using='gin'),
    )


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
            tsv_content=func.to_tsvector('english', model.content),
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
            title=self.title
        )
