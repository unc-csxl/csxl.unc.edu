"""Definition for a COMP 423 project for showcasing."""

from pydantic import BaseModel
from enum import Enum

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class ShowcaseProject(BaseModel):
    team_name: str
    type: str
    members: list[str]
    video_url: str
    deployment_url: str
