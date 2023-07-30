"""Service that manages reservations in the coworking space."""

from fastapi import Depends
from datetime import datetime, timedelta
from random import random
from sqlalchemy.orm import Session, joinedload
from ...database import db_session
from ...models.user import User, UserIdentity
from ...models.coworking import (
    Seat,
    Reservation,
    ReservationRequest,
    ReservationIdentity,
    ReservationPartial,
    TimeRange,
    SeatAvailability,
    ReservationState,
    AvailabilityList,
    OperatingHours,
)
from ...entities import UserEntity
from ...entities.coworking import ReservationEntity, SeatEntity
from .seat import SeatService
from .policy import PolicyService
from .operating_hours import OperatingHoursService
from ..permission import PermissionService

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class ReservationError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class ReservationService:
    """ReservationService is the access layer to managing reservations for seats and rooms."""

    def __init__(
        self,
        session: Session = Depends(db_session),
        permission_svc: PermissionService = Depends(),
        policy_svc: PolicyService = Depends(),
        operating_hours_svc: OperatingHoursService = Depends(),
        seats_svc: SeatService = Depends(),
    ):
        """Initializes a new ReservationService.

        Args:
            session (Session): The database session to use, typically injected by FastAPI.
        """
        self._session = session
        self._permission_svc = permission_svc
        self._policy_svc = policy_svc
        self._operating_hours_svc = operating_hours_svc
        self._seat_svc = seats_svc

    def get_current_reservations_for_user(
        self, subject: User, focus: User
    ) -> list[Reservation]:
        """Find current and upcoming reservations for a given user.
        The subject must either also be the focus or have permission to view reservations of
        the given user. The permission needed is action "coworking.reservation.read" and
        resource "coworking.reservation.users/:focus_id"

        Args:
            subject (User): The user making the request
            focus (User): The user whose reservations are being retrieved

        Returns:
            list[Reservation]: Upcoming reservations for the user.

        Raises:
            UserPermissionError"""
        if subject != focus:
            self._permission_svc.enforce(
                subject,
                "coworking.reservation.read",
                f"user/{focus.id}",
            )
        #
        now = datetime.now()
        time_range = TimeRange(
            start=now - timedelta(days=1),
            end=now + self._policy_svc.reservation_window(focus),
        )
        return self._get_active_reservations_for_user(focus, time_range)

    def _get_active_reservations_for_user(
        self, focus: UserIdentity, time_range: TimeRange
    ) -> list[Reservation]:
        reservations = (
            self._session.query(ReservationEntity)
            .join(ReservationEntity.users)
            .filter(
                ReservationEntity.start < time_range.end,
                ReservationEntity.end > time_range.start,
                ReservationEntity.state.not_in(
                    [ReservationState.CANCELLED, ReservationState.CHECKED_OUT]
                ),
                UserEntity.id == focus.id,
            )
            .options(
                joinedload(ReservationEntity.users), joinedload(ReservationEntity.seats)
            )
            .order_by(ReservationEntity.start)
            .all()
        )

        reservations = self._state_transition_reservation_entities_by_time(
            datetime.now(), reservations
        )

        return [reservation.to_model() for reservation in reservations]

    def get_seat_reservations(
        self, seats: list[Seat], time_range: TimeRange
    ) -> list[Reservation]:
        """Returns all reservations for a set of seats in a given time range.

        Args:
            seats (list[Seat]): The list of seats to query for reservations.
            time_range (TimeRange): The date range to check for matching reservations.

        Returns:
            list[Reservation]: All reservations for the seats within the given time_range, including overlaps.
        """
        reservations = (
            self._session.query(ReservationEntity)
            .join(ReservationEntity.seats)
            .filter(
                ReservationEntity.start < time_range.end,
                ReservationEntity.end > time_range.start,
                ReservationEntity.state.not_in(
                    [ReservationState.CANCELLED, ReservationState.CHECKED_OUT]
                ),
                SeatEntity.id.in_([seat.id for seat in seats]),
            )
            .options(
                joinedload(ReservationEntity.seats), joinedload(ReservationEntity.users)
            )
            .all()
        )

        reservations = self._state_transition_reservation_entities_by_time(
            datetime.now(), reservations
        )

        return [reservation.to_model() for reservation in reservations]

    def _state_transition_reservation_entities_by_time(
        self, cutoff: datetime, reservations: list[ReservationEntity]
    ) -> list[ReservationEntity]:
        """Private, internal helper method for transitioning reservation entities
        based on time. Three transitions are time-based:

        1. Draft -> Cancelled following PolicyService#reservation_draft_timeout() after
           the reservation's created at.
        2. Confirmed -> Cancelled following PolicyService#reservation_checkin_timeout() after
            the reservation's start.
        3. Checked In -> Checked Out following the reservation's end.

        Args:
            moment (datetime): The time in which checks of expiration are made against. In
                production, this is the current time.
            reservations (list[ReservationEntity]): The list of entities to state transition.

        Returns:
            list[ReservationEntity] - All ReservationEntities that were not state transitioned.
        """
        valid: list[ReservationEntity] = []
        dirty = False
        for reservation in reservations:
            if (
                reservation.state == ReservationState.DRAFT
                and reservation.created_at
                + self._policy_svc.reservation_draft_timeout()
                < cutoff
            ):
                reservation.state = ReservationState.CANCELLED
                dirty = True
            elif (
                reservation.state == ReservationState.CONFIRMED
                and reservation.start + self._policy_svc.reservation_checkin_timeout()
                < cutoff
            ):
                reservation.state = ReservationState.CANCELLED
                dirty = True
            elif (
                reservation.state == ReservationState.CHECKED_IN
                and reservation.end <= cutoff
            ):
                reservation.state = ReservationState.CHECKED_OUT
                dirty = True
            else:
                valid.append(reservation)

        if dirty:
            self._session.commit()

        return valid

    def seat_availability(
        self, seats: list[Seat], bounds: TimeRange
    ) -> list[SeatAvailability]:
        """Returns a list of all seat availability for specific seats within a given timerange.

        Args:
            bounds (TimeRange): The time range of interest.
            seats (list[Seat]): The seats to check the availability of.

        Returns:
            list[SeatAvailability]: All seat availability ordered by nearest and longest available.
        """
        # No seats are available in the past
        now = datetime.now()
        if bounds.end <= now:
            return []

        # Ensure the start of the bounds is at least right now
        if bounds.start < now:
            bounds.start = now

        # Ensure the bounds is at least as long as a minimum reservation length, with a fudge factor
        MINUMUM_RESERVATION_EPSILON = timedelta(minutes=1)
        if (
            bounds.duration()
            < self._policy_svc.minimum_reservation_duration()
            - MINUMUM_RESERVATION_EPSILON
        ):
            return []

        # Find operating hours schedule during the requested bounds
        open_hours = self._operating_hours_svc.schedule(bounds)
        if len(open_hours) == 0:
            return []

        # Convert the operating hours during the bounds into an availability list
        # and constrain the availability list within the bounds.
        open_availability_list = self._operating_hours_to_bounded_availability_list(
            open_hours, bounds
        )
        if len(open_availability_list.availability) == 0:
            return []

        # Start from a position where all seats begin with same availability as
        # open_availability_list. From there, reservations will subtract availability
        # from the given seat.
        seat_availability_dict = self._initialize_seat_availability_dict(
            seats, open_availability_list
        )

        # Get all active reservations during the availability bounds for the seats.
        reservation_range = TimeRange(
            start=open_availability_list.availability[0].start,
            end=open_availability_list.availability[-1].end,
        )
        reservations = self.get_seat_reservations(seats, reservation_range)

        # Subtract all seat reservations from their availability
        self._remove_reservations_from_availability(
            seat_availability_dict, reservations
        )

        # Remove seats with availability below threshold
        available_seats = self._prune_seats_below_availability_threshold(
            list(seat_availability_dict.values()),
            self._policy_svc.minimum_reservation_duration()
            - MINUMUM_RESERVATION_EPSILON,
        )

        # Sort by nearest available ASC, duration DESC, reservable (False before True), with entropy
        # The rationale for entropy is when XL is wide open for walkins, within the given seat search
        # we'd like to mix up the order in which seats are assigned rather than always giving away
        # the same sequence of seats (and causing more consisten wear and tear to it).
        available_seats.sort(
            key=lambda sa: (
                sa.availability[0].start,
                -1 * sa.availability[0].duration(),
                sa.reservable,
                random(),
            )
        )

        return available_seats

    def draft_reservation(
        self, subject: User, request: ReservationRequest
    ) -> Reservation:
        """When a user begins the process of making a reservation, a draft holds its place until confired.

        For launch, reservations are limited to a single user. Reservations must either be made by and for
        the subject initiating the request, or by an admin with permission to complete the action
        "coworking.reservation.manage" for resource "user/{user.id}".

        Args:
            subject (User): The user initiating the draft request.
            request (ReservationRequest): The requested reservation.

        Returns:
            Reservation: The DRAFT reservation.

        Raises:
            ReservationError: If the requested reservation cannot be satisfied.

        Future work:
            * Think about errors/validations of drafts that can be edited rather than raising exceptions.
            * Multi-user reservations
                * Check for equality between users and available seats
                * Limit users and seats counts to policy
            * Clean-up / Refactor Implementation
        """
        # For the time being, reservations are limited to one user. As soon as
        # possible, we'd like to add multi-user reservations so that pairs and teams
        # can be simplified.
        if len(request.users) > 1:
            raise ReservationError("Multi-user reservations not yet supproted.")

        # Enforce Reservation Draft Permissions
        if subject.id not in [user.id for user in request.users]:
            for user in request.users:
                self._permission_svc.enforce(
                    subject, "coworking.reservation.manage", f"user/{user.id}"
                )

        # Bound start
        now = datetime.now()
        start = request.start if request.start >= now else now

        is_walkin = abs(request.start - now) < self._policy_svc.walkin_window(subject)

        # Bound end to policy limits for duration of a reservation
        if is_walkin:
            max_length = self._policy_svc.walkin_initial_duration(subject)
        else:
            max_length = self._policy_svc.maximum_initial_reservation_duration(subject)
        end_limit = start + max_length
        end = request.end if request.end <= end_limit else end_limit

        # Enforce request range is within bounds of walkin vs. pre-reserved policies
        bounds = TimeRange(start=start, end=end)

        # Fetch User entities for all requested in reservation
        user_entities = (
            self._session.query(UserEntity)
            .filter(UserEntity.id.in_([user.id for user in request.users]))
            .all()
        )
        if len(user_entities) == 0:
            raise ReservationError(
                "At least one valid user is required to make a reservation."
            )

        # Check for overlapping reservations for a single user
        for user in request.users:
            conflicts = self._get_active_reservations_for_user(user, bounds)
            if len(conflicts) > 0:
                raise ReservationError("Users may not have conflicting reservations.")

        # Look at the seats - match bounds of assigned seat's availability
        # TODO: Fetch all seats
        seats: list[Seat] = SeatEntity.get_models_from_identities(
            self._session, request.seats
        )
        seat_availability = self.seat_availability(seats, bounds)

        if not is_walkin:
            seat_availability = [seat for seat in seat_availability if seat.reservable]

        if len(seat_availability) == 0:
            raise ReservationError("The requested seat(s) are no longer available.")

        # TODO (limit to # of users on request if multiple users)
        # Here we constrain the reservation start/end to that of the best available seat requested.
        # This matters as walk-in availability becomes scarce (may start in the near future even though request
        # start is for right now), alternatively may end early due to reserved seat on backend.
        seat_entities = [self._session.get(SeatEntity, seat_availability[0].id)]
        bounds = seat_availability[0].availability[0]

        draft = ReservationEntity(
            state=ReservationState.DRAFT,
            start=bounds.start,
            end=bounds.end,
            users=user_entities,
            walkin=is_walkin,
            room_id=None,
            seats=seat_entities,
        )

        self._session.add(draft)
        self._session.commit()
        return draft.to_model()

    def change_reservation(
        self, subject: User, delta: ReservationPartial
    ) -> Reservation:
        """Users should be able to change reservations without hassle. Different restrictions apply to changes based on state of reservation."""
        entity = self._session.get(ReservationEntity, delta.id)
        if entity is None:
            raise LookupError(f"Reservation(id={delta.id}) does not exist")

        # Ensure permissions to manage reservations for all users in reservation
        current = entity.to_model()
        if subject not in current.users:
            for user in current.users:
                self._permission_svc.enforce(
                    subject, "coworking.reservation.manage", f"user/{user.id}"
                )

        # Handle Requested State Changes
        dirty = False
        if delta.state is not None and delta.state != entity.state:
            dirty = dirty or self._change_state(entity, delta.state)

        # Handle Requested Seat Changes?
        if delta.seats is not None:
            raise NotImplementedError("Changing seats not yet supported.")

        # Handle Requested Party Changes
        if delta.users is not None:
            raise NotImplementedError("Changing party not yet supported.")

        # Handle Requested Time Changes (TODO)
        if delta.start is not None or delta.end is not None or delta.seats is not None:
            # TODO: Assure these requested changes are valid within policies
            raise NotImplementedError("Changing start/end not yet supported")

        if dirty:  # and valid():
            self._session.commit()

        return entity.to_model()

    def _change_state(self, entity: ReservationEntity, delta: ReservationState) -> bool:
        RS = ReservationState

        transition = (entity.state, delta)
        valid_transition = False
        match transition:
            case (RS.DRAFT, RS.CONFIRMED):
                valid_transition = True
            case (RS.DRAFT, RS.CANCELLED):
                valid_transition = True
            case (RS.CONFIRMED, RS.CANCELLED):
                valid_transition = True
            case (RS.CHECKED_IN, RS.CHECKED_OUT):
                valid_transition = True
            case _:
                return False

        if valid_transition:
            entity.state = delta

        return True

    def self_checkin_reservation(
        self, subject: User, reservation: Reservation, checkin_code: str
    ) -> Reservation:
        """When the user is ready to check-in for their reservation near the reserved time, via a checkin-code, this endpoint is used."""
        # TODO: Should check-in be on the join table between reservation and user??
        raise NotImplementedError()

    def staff_checkin_reservation(
        self, subject: User, reservation: Reservation
    ) -> Reservation:
        """Staff members with the correct permissions can check users in to their reservations directly."""
        # TODO: Should check-in be on the join table between reservation and user??
        raise NotImplementedError()

    # Private helper methods

    def _operating_hours_to_bounded_availability_list(
        self, operating_hours: list[OperatingHours], bounds: TimeRange
    ) -> AvailabilityList:
        availability = AvailabilityList(
            availability=[
                TimeRange(start=operating_hour.start, end=operating_hour.end)
                for operating_hour in operating_hours
            ]
        )
        availability.constrain(bounds)
        return availability

    def _initialize_seat_availability_dict(
        self, seats: list[Seat], availability: AvailabilityList
    ) -> dict[int, SeatAvailability]:
        return {
            seat.id: SeatAvailability(
                availability=availability.model_copy(deep=True).availability,
                **seat.model_dump(),
            )
            for seat in seats
            if seat.id is not None
        }

    def _remove_reservations_from_availability(
        self,
        seat_availability_dict: dict[int, SeatAvailability],
        reservations: list[Reservation],
    ):
        for reservation in reservations:
            if len(reservation.seats) > 0:
                for seat in reservation.seats:
                    if seat.id in seat_availability_dict:
                        seat_availability_dict[seat.id].subtract(reservation)

    def _prune_seats_below_availability_threshold(
        self, seats: list[SeatAvailability], threshold: timedelta
    ) -> list[SeatAvailability]:
        available_seats: list[SeatAvailability] = []
        for seat in seats:
            seat.filter_time_ranges_below(threshold)
            if len(seat.availability) > 0:
                available_seats.append(seat)
        return available_seats
