import { Profile } from '../models.module';
import { TimeRangeJSON, TimeRange } from '../time-range';

export interface OperatingHoursJSON extends TimeRangeJSON {
  id: number;
}

export interface OperatingHours extends TimeRange {
  id: number;
}

export const parseTimeRange = (json: TimeRangeJSON): TimeRange => {
  return {
    start: new Date(json.start),
    end: new Date(json.end)
  };
};

export const parseOperatingHoursJSON = (
  json: OperatingHoursJSON
): OperatingHours => {
  return Object.assign({}, json, parseTimeRange(json));
};

export interface Seat {
  id: number;
  title: string;
  shorthand: string;
  reservable: boolean;
  has_monitor: boolean;
  sit_stand: boolean;
  x: number;
  y: number;
}

export interface Room {
  id: string | null;
  nickname: string;
}

export interface RoomDetails {
  id: string | null;
  nickname: string;
  building: string;
  room: string;
  capacity: number;
  reservable: boolean;
  description: string;
  seats: Seat[];
}

export interface ReservationJSON extends TimeRangeJSON {
  id: number;
  users: Profile[];
  seats: Seat[];
  walkin: boolean;
  created_at: string;
  updated_at: string;
  room: Room | null;
  state: string;
}

export interface Reservation extends TimeRange {
  id: number;
  users: Profile[];
  seats: Seat[];
  walkin: boolean;
  created_at: Date;
  updated_at: Date;
  room: Room | null;
  state: string;
}

export const parseReservationJSON = (json: ReservationJSON): Reservation => {
  const timestamps = {
    created_at: new Date(json.created_at),
    updated_at: new Date(json.updated_at)
  };
  return Object.assign({}, json, parseTimeRange(json), timestamps);
};

export interface SeatAvailabilityJSON extends Seat {
  availability: TimeRangeJSON[];
}

export interface SeatAvailability extends Seat {
  availability: TimeRange[];
}

export const parseSeatAvailabilityJSON = (
  json: SeatAvailabilityJSON
): SeatAvailability => {
  let availability = json.availability.map(parseTimeRange);
  return Object.assign({}, json, { availability });
};

export interface CoworkingStatusJSON {
  my_reservations: ReservationJSON[];
  seat_availability: SeatAvailabilityJSON[];
  operating_hours: OperatingHoursJSON[];
}

export interface CoworkingStatus {
  my_reservations: Reservation[];
  seat_availability: SeatAvailability[];
  operating_hours: OperatingHours[];
}

export const parseCoworkingStatusJSON = (
  json: CoworkingStatusJSON
): CoworkingStatus => {
  return {
    my_reservations: json.my_reservations.map(parseReservationJSON),
    seat_availability: json.seat_availability.map(parseSeatAvailabilityJSON),
    operating_hours: json.operating_hours.map(parseOperatingHoursJSON)
  };
};

export interface ReservationRequest extends TimeRange {
  users: Profile[] | null;
  seats: Seat[] | null;
  room: { id: string };
}
/* Interface for Room Reservation Type */
export interface RoomReservation {
  reservation_id: number | null;
  user_id: number;
  room_name: string;
  start: Date;
  end: Date;
}

/** Interface for the RoomReservation JSON Response model
 *  Note: The API returns object data, such as `Date`s, as strings. So,
 *  this interface models the data directly received from the API. It is
 *  the job of the `parseRoomReservationJson` function to convert it to the
 *  `RoomReservation` type
 */
export interface RoomReservationJson {
  reservation_id: number | null;
  user_id: number;
  room_name: string;
  start: string;
  end: string;
}

/** Function that converts a RoomReservationJSON response model to a
 *  Room Reservation model. This function is needed because the API response
 *  will return certain objects (such as `Date`s) as strings. We need to
 *  convert this to TypeScript objects ourselves.
 */
export const parseEventJson = (
  roomReservationJson: RoomReservationJson
): RoomReservation => {
  return Object.assign({}, roomReservationJson, {
    start: new Date(roomReservationJson.start),
    end: new Date(roomReservationJson.end)
  });
};

/**
 * Represents a cell in a Table Widget
 * @property key - The room of the cell acting as key
 * @property index - The index of the cell in the reservationMap that represents the timeslot's state
 */
export interface TableCell {
  key: string;
  index: number;
}

export interface TableCellProperty {
  backgroundColor: string;
  isDisabled: boolean;
}

export interface TablePropertyMap {
  [key: number]: TableCellProperty;
}

export interface ReservationMapDetails {
  reserved_date_map: Record<string, number[]>;
  operating_hours_start: string;
  operating_hours_end: string;
  number_of_time_slots: number;
}
