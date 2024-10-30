"""Pydantic models for the `Document` entity."""

from pydantic import BaseModel
from enum import Enum

class DocumentEnum(str, Enum):
    REGISTRATION_GUIDE = "REGISTRATION GUIDE"
    FAQ = "FAQ"

class Document(BaseModel):
    id: int
    title: str
    content: str # TODO: Change to full text search / text
    type: int # Registration guide = 1, FAQ = 2
    
    

