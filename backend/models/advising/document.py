"""Pydantic models for the `Document` entity."""

from pydantic import BaseModel

class Document(BaseModel):
    id: int
    title: str
    
    

