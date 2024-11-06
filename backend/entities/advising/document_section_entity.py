from sqlalchemy import Integer, String, Boolean, ForeignKey, DateTime, func, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .entity_base import EntityBase
from ...models.advising import document
from backend.models.document import DocumentEnum
from document_entity import DocumentEntity
from ...models.advising import document_section
from ...models.advising.document_section import DocumentSection
from ...models.advising.document_details import DocumentDetails

class SectionEntity(EntityBase):
    __tablename__ = "section"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    title: Mapped[str] = mapped_column(String, nullable=False)

    content: Mapped[str] = mapped_column(String, nullable=False)

    # NOTE: This defines a one-to-many relationship between the document and section tables.
    document_id: Mapped[int] = mapped_column(ForeignKey("document.id"))
    document: Mapped["DocumentEntity"] = relationship(back_populates="sections")

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
    def from_model(cls, model: DocumentSection) -> "SectionEntity":
        return cls(
            id=model.id,
            title=model.title,
            content=model.content,
            document_id=model.document_id,
        )

    def to_model(self) -> DocumentSection:
        return DocumentSection(
            id=self.id,
            title=self.title,
            content=self.content,
            document_id=self.document_id,
        )