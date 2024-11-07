from pydantic import BaseModel

"""Pydantic models for the `Document` entity."""


__author__ = ["Nathan Kelete"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class Document(BaseModel):
    id: int
    title: str
    
    

