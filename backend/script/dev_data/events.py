"""Sample Event models to use in the development environment."""

from backend.entities.event_entity import EventEntity
import datetime

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


event1 = EventEntity(
    id=1, 
    name="HackNC", 
    time=datetime.datetime.fromtimestamp(1680110861), 
    location="Fetzer Gym", 
    description="HackNC is an annual, student-run hackathon hosted by the University of North Carolina at Chapel Hill.", 
    public=True, 
    org_id=12
    )

event2 = EventEntity(
    id=2, 
    name="CS+Social Good", 
    time=datetime.datetime.fromtimestamp(1880110861), 
    location="Sitterson", 
    description="Club meeting", 
    public=True, 
    org_id=6
    )

models = [
    event1, event2
]