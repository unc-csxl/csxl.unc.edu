"""Pydantic models for the `Document Section` entity."""


__author__ = ["Nathan Kelete"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

from pydantic import BaseModel

class DocumentSection(BaseModel):
    id: int
    title: str
    content: str
    doc_id: int
    
    

