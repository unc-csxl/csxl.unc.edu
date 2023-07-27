"""Sample EventDetail models to use in the development environment."""

from backend.entities.event_entity import EventEntity
import datetime

__authors__ = ["Ajay Gandecha", "Jade Keegan", "Brianna Ta", "Audrey Toney"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

event1 = EventEntity(
    name="HackNC Hackathon",
    time=datetime.datetime.fromtimestamp(1681653600),
    location="Fetzer Gym",
    description="HackNC is an annual, student-run hackathon hosted by the University of North Carolina at Chapel Hill.",
    public=True,
    org_id=12,
)

event2 = EventEntity(
    name="CSSG Scavenger Hunt",
    time=datetime.datetime.fromtimestamp(1681765200),
    location="Sitterson",
    description="CS+SG is hosting a Womxn in Tech Week Scavenger Hunt to celebrate womxn in tech!",
    public=True,
    org_id=6,
)

event3 = EventEntity(
    name="PearlHacks Hackathon",
    time=datetime.datetime.fromtimestamp(1681819200),
    location="Great Hall",
    description="PearlHacks is an annual, student-run hackathon specifically for women and nonbinary students.",
    public=False,
    org_id=14,
)

event4 = EventEntity(
    name="Black in Technology GBM",
    time=datetime.datetime.fromtimestamp(1681929000),
    location="Sitterson",
    description="This is a general body meeting for Black in Technology. All are welcome.",
    public=True,
    org_id=3,
)

event5 = EventEntity(
    name="Club Meeting",
    time=datetime.datetime.fromtimestamp(1682026200),
    location="Sitterson",
    description="Meeting time for app team members to code together and have snacks!",
    public=False,
    org_id=2,
)

event6 = EventEntity(
    name="Project Showcase",
    time=datetime.datetime.fromtimestamp(1682103600),
    location="Sitterson",
    description="CSSG's end of semester showcase where everyone shows off their projects! Pizza will be provided.",
    public=False,
    org_id=6,
)

event7 = EventEntity(
    name="CADS Public Event",
    time=datetime.datetime.fromtimestamp(1690732800),
    location="Sitterson",
    description="This is a public CADS event.",
    public=True,
    org_id=4,
)

event8 = EventEntity(
    name="CADS Private Event",
    time=datetime.datetime.fromtimestamp(1690732800),
    location="Sitterson",
    description="This is a private CADS event.",
    public=False,
    org_id=4,
)


models = [event1, event2, event3, event4, event5, event6, event7, event8]
