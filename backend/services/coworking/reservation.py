"""Service that manages reservations in the coworking space."""

from fastapi import Depends
from datetime import datetime, timedelta
from random import random
from typing import Sequence
from sqlalchemy.orm import Session, joinedload
from ...database import db_session
from ...models.user import User, UserIdentity
from ..exceptions import UserPermissionException, ResourceNotFoundException
from ...models.coworking import (
    Seat,
    Reservation,
    ReservationRequest,
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


class ReservationException(Exception):
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

    def get_reservation(self, subject: User, id: int) -> Reservation:
        """Lookup a reservation by ID.

        Args:
            subject (User): The user making the request
            id (int): The ID of the reservation being retrieved

        Returns:
            Reservation: Reservation with the requested ID.

        Raises:
            UserPermissionException
            ResourceNotFoundException
        """
        reservation: ReservationEntity | None = self._session.get(ReservationEntity, id)
        if reservation == None:
            raise ResourceNotFoundException(f"No reservation with an ID of {id} found.")

        # The subject sould _be_ one of the users or have read access on reservations
        # for at least one of the users.
        has_permission = False
        for user in reservation.users:
            if user.id == subject.id or self._permission_svc.check(
                subject, "coworking.reservation.read", f"user/{user.id}"
            ):
                has_permission = True
                break

        if not has_permission:
            raise UserPermissionException("coworking.reservation.read", "user/")

        return reservation.to_model()

    def get_current_reservations_for_user(
        self, subject: User, focus: User
    ) -> Sequence[Reservation]:
        """Find current and upcoming reservations for a given user.
        The subject must either also be the focus or have permission to view reservations of
        the given user. The permission needed is action "coworking.reservation.read" and
        resource "coworking.reservation.users/:focus_id"

        Args:
            subject (User): The user making the request
            focus (User): The user whose reservations are being retrieved

        Returns:
            Sequence[Reservation]: Upcoming reservations for the user.

        Raises:
            UserPermissionException"""
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
    ) -> Sequence[Reservation]:
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
        self, seats: Sequence[Seat], time_range: TimeRange
    ) -> Sequence[Reservation]:
        """Returns all reservations for a set of seats in a given time range.

        Args:
            seats (Sequence[Seat]): The list of seats to query for reservations.
            time_range (TimeRange): The date range to check for matching reservations.

        Returns:
            Sequence[Reservation]: All reservations for the seats within the given time_range, including overlaps.
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
        self, cutoff: datetime, reservations: Sequence[ReservationEntity]
    ) -> Sequence[ReservationEntity]:
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
            reservations (Sequence[ReservationEntity]): The list of entities to state transition.

        Returns:
            Sequence[ReservationEntity] - All ReservationEntities that were not state transitioned.
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
        self, seats: Sequence[Seat], bounds: TimeRange
    ) -> Sequence[SeatAvailability]:
        """Returns a list of all seat availability for specific seats within a given timerange.

        Args:
            bounds (TimeRange): The time range of interest.
            seats (list[Seat]): The seats to check the availability of.

        Returns:
            Sequence[SeatAvailability]: All seat availability ordered by nearest and longest available.
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
        available_seats: list[SeatAvailability] = list(
            self._prune_seats_below_availability_threshold(
                list(seat_availability_dict.values()),
                self._policy_svc.minimum_reservation_duration()
                - MINUMUM_RESERVATION_EPSILON,
            )
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
            raise NotImplementedError("Multi-user reservations not yet supproted.")

        # Enforce Reservation Draft Permissions
        if subject.id not in [user.id for user in request.users]:
            for user in request.users:
                self._permission_svc.enforce(
                    subject, "coworking.reservation.manage", f"user/{user.id}"
                )

        # Bound start
        now = datetime.now()
        start = request.start if request.start >= now else now

        is_walkin = abs(start - now) < self._policy_svc.walkin_window(subject)

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
            raise ReservationException(
                "At least one valid user is required to make a reservation."
            )

        # Check for overlapping reservations for a single user
        # if len(user_entities) == 1:
        conflicts = self._get_active_reservations_for_user(request.users[0], bounds)
        for conflict in conflicts:
            if is_walkin and conflict.walkin:
                raise ReservationException(
                    "Users may not have concurrent walk-in reservations."
                )

            nonconflicting = bounds.subtract(conflict)
            if len(nonconflicting) == 1:
                bounds = nonconflicting[0]
            else:
                raise ReservationException(
                    "Users may not have conflicting reservations."
                )
        # Dead code because of the NotImplementedError testing for multiple users at the top
        # else:
        #     # Draft of expected functionality (needs testing and sanity checking)
        #     # Multiple users all need to not have conflicts
        #     for user in request.users:
        #         conflicts = self._get_active_reservations_for_user(user, bounds)
        #         if len(conflicts) > 0:
        #             raise ReservationException(
        #                 "Users may not have conflicting reservations."
        #             )

        # Look at the seats - match bounds of assigned seat's availability
        # TODO: Fetch all seats
        seats: list[Seat] = SeatEntity.get_models_from_identities(
            self._session, request.seats
        )
        seat_availability = self.seat_availability(seats, bounds)

        if not is_walkin:
            seat_availability = [seat for seat in seat_availability if seat.reservable]

        if len(seat_availability) == 0:
            raise ReservationException("The requested seat(s) are no longer available.")

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
        """Modify an existing reservation.

        Users should be able to change reservations without hassle. Different restrictions apply to changes based on state of reservation.

        Args:
            subject (User): The user initiating the reservation change request.
            delta (ReservationPartial): The fields of a reservation with requested changes.

        Returns:
            Reservation - the updated reservation

        Raises:
            ResourceNotFoundException when the requested ID is not found
            UserPermissionException when user does not have permission to modify the reservation
            NotImplementedError when requested changes are not yet implemented as features

        Future work:
            Implement the ability to change seats, party, and start/end time within policy restrictions
        """
        entity = self._session.get(ReservationEntity, delta.id)
        if entity is None:
            raise ResourceNotFoundException(
                f"Reservation(id={delta.id}) does not exist"
            )

        # Either the current user is party to the reservation or an admin has
        # permission to manage reservations for all users.
        current = entity.to_model()
        user_ids = set((user.id for user in current.users))
        if subject.id not in user_ids:
            for user_id in user_ids:
                self._permission_svc.enforce(
                    subject, "coworking.reservation.manage", f"user/{user_id}"
                )

        # Handle Requested State Changes
        dirty = False
        if delta.state is not None and delta.state != entity.state:
            dirty = dirty or self._change_state(entity, delta.state)
            if entity.state == ReservationState.CHECKED_OUT:
                entity.end = datetime.now()

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

    def list_all_active_and_upcoming(self, subject: User) -> Sequence[Reservation]:
        """Ambassadors need to see all active and upcoming reservations.

        This method queries all future events. When pre-reservations are added, this method
        will need redesign to support date/time based pagination.

        Args:
            subject (User): The user initiating the reservation change request.

        Returns:
            Sequence[Reservation] - all active and upcoming reservations

        Raises:
            UserPermissionException when user does not have permission to read reservations

        Future work:
            Pagination based on timespans in the future.
        """
        self._permission_svc.enforce(subject, "coworking.reservation.read", f"user/*")
        now = datetime.now()
        reservations = (
            self._session.query(ReservationEntity)
            .join(ReservationEntity.users)
            .filter(
                ReservationEntity.start <= now + timedelta(minutes=5),
                ReservationEntity.end > now,
                ReservationEntity.state.in_(
                    (
                        ReservationState.CONFIRMED,
                        ReservationState.CHECKED_IN,
                        ReservationState.CHECKED_OUT,
                    )
                ),
            )
            .options(
                joinedload(ReservationEntity.users), joinedload(ReservationEntity.seats)
            )
            .order_by(ReservationEntity.start.desc())
            .all()
        )
        return [reservation.to_model() for reservation in reservations]

    def staff_checkin_reservation(
        self, subject: User, reservation: Reservation
    ) -> Reservation:
        """XL Staff members can check users in to their reservations directly.

        Args:
            subject (User): The user initiating the checkin request.
            reservation(Reservation): The reservation being checked in.

        Returns:
            Reservation: The updated reservation.

        Raises:
            ReservationError: If the requested checkin request cannot be satisfied, such as
            attempting to check-in a reservation that's in the wrong state.

        Future Work:
            Should staff only be able to check-in reservations whose start time is
            within the next time interval defined by a policy?
        """
        entity = self._session.get(ReservationEntity, reservation.id)
        if entity is None:
            raise ResourceNotFoundException(
                f"Reservation(id={reservation.id}) does not exist"
            )

        # Ensure permissions to manage reservation checkins
        self._permission_svc.enforce(subject, "coworking.reservation.manage", f"user/*")

        # Update state iff ReservationState is current CONFIRMED
        if entity.state == ReservationState.CONFIRMED:
            entity.state = ReservationState.CHECKED_IN
            self._session.commit()
        elif entity.state in (
            ReservationState.CANCELLED,
            ReservationState.CHECKED_OUT,
            ReservationState.DRAFT,
        ):
            raise ReservationException(
                f"Cannot check in from current state of {entity.state}"
            )
        else:
            ...  # Idempotent case of ReservationState.CHECKED_IN

        return entity.to_model()

    # Private helper methods

    def _operating_hours_to_bounded_availability_list(
        self, operating_hours: Sequence[OperatingHours], bounds: TimeRange
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
        self, seats: Sequence[Seat], availability: AvailabilityList
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
        reservations: Sequence[Reservation],
    ):
        for reservation in reservations:
            if len(reservation.seats) > 0:
                for seat in reservation.seats:
                    if seat.id in seat_availability_dict:
                        seat_availability_dict[seat.id].subtract(reservation)

    def _prune_seats_below_availability_threshold(
        self, seats: Sequence[SeatAvailability], threshold: timedelta
    ) -> Sequence[SeatAvailability]:
        available_seats: list[SeatAvailability] = []
        for seat in seats:
            seat.filter_time_ranges_below(threshold)
            if len(seat.availability) > 0:
                available_seats.append(seat)
        return available_seats
