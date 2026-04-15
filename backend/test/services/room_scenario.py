from dataclasses import dataclass

from sqlalchemy.orm import Session

from ...entities import RoomEntity
from ...models import RoomDetails


@dataclass(frozen=True)
class RoomScenario:
    the_xl: RoomDetails
    group_a: RoomDetails
    group_b: RoomDetails
    group_c: RoomDetails
    pair_a: RoomDetails
    virtual: RoomDetails
    new_room: RoomDetails
    edited_xl: RoomDetails

    @property
    def rooms(self) -> list[RoomDetails]:
        return [
            self.the_xl,
            self.group_a,
            self.group_b,
            self.group_c,
            self.pair_a,
            self.virtual,
        ]


def build_room_scenario() -> RoomScenario:
    return RoomScenario(
        the_xl=RoomDetails(
            id="SN156",
            building="Sitterson",
            room="156",
            nickname="The XL",
            capacity=40,
            reservable=False,
            seats=[],
        ),
        group_a=RoomDetails(
            id="SN135",
            building="Sitterson",
            room="135",
            nickname="Group A",
            capacity=4,
            reservable=True,
            seats=[],
        ),
        group_b=RoomDetails(
            id="SN137",
            building="Sitterson",
            room="137",
            nickname="Group B",
            capacity=4,
            reservable=True,
            seats=[],
        ),
        group_c=RoomDetails(
            id="SN141",
            building="Sitterson",
            room="141",
            nickname="Group C",
            capacity=6,
            reservable=True,
            seats=[],
        ),
        pair_a=RoomDetails(
            id="SN139",
            building="Sitterson",
            room="139",
            nickname="Pair A",
            capacity=2,
            reservable=True,
            seats=[],
        ),
        new_room=RoomDetails(
            id="FB009",
            building="Fred Brooks",
            room="009",
            nickname="Large Room",
            capacity=100,
            reservable=False,
            seats=[],
        ),
        edited_xl=RoomDetails(
            id="SN156",
            building="Sitterson",
            room="156",
            nickname="The CSXL",
            capacity=100,
            reservable=False,
            seats=[],
        ),
        virtual=RoomDetails(
            id="Virtual",
            building="Virtual",
            room="Virtual",
            nickname="Virtual CSXL",
            capacity=999,
            reservable=False,
            seats=[],
        ),
    )


def arrange_room_scenario(session: Session) -> RoomScenario:
    scenario = build_room_scenario()
    session.add_all([RoomEntity.from_model(room) for room in scenario.rooms])
    session.commit()
    return scenario