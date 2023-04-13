"""Sample Event models to use in the development environment."""

from backend.entities.event_entity import EventEntity
import datetime

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


event1 = EventEntity(
    name="HackNC Hackathon", 
    time=datetime.datetime.fromtimestamp(1680110861), 
    location="Fetzer Gym", 
    description="HackNC is an annual, student-run hackathon hosted by the University of North Carolina at Chapel Hill.", 
    public=True, 
    org_id=12
    )

event2 = EventEntity(
    name="CS+Social Good Scavenger Hunt", 
    time=datetime.datetime.fromtimestamp(1880110861), 
    location="Sitterson", 
    description="CS+SG is hosting a Womxn in Tech Week Scavenger Hunt to celebrate womxn in tech!", 
    public=True, 
    org_id=6
    )

event3 = EventEntity(
    name="PearlHacks Hackathon", 
    time=datetime.datetime.fromtimestamp(1680764400), 
    location="Great Hall", 
    description="PearlHacks is an annual, student-run hackathon specifically for women and nonbinary students.", 
    public=False, 
    org_id=14
    )

event4 = EventEntity(
    name="Black in Technology GBM", 
    time=datetime.datetime.fromtimestamp(1365231600), 
    location="Sitterson", 
    description="This is a general body meeting for Black in Technology. All are welcome.", 
    public=False, 
    org_id=3
    )

models = [
    event1, event2, event3, event4
]