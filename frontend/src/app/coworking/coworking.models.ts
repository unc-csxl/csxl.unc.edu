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

export interface ReservationJSON extends TimeRangeJSON {
  id: number;
  users: Profile[];
  seats: Seat[];
  walkin: boolean;
  created_at: string;
  updated_at: string;
  state: string;
}

export interface Reservation extends TimeRange {
  id: number;
  users: Profile[];
  seats: Seat[];
  walkin: boolean;
  created_at: Date;
  updated_at: Date;
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
  users: Profile[];
  seats: Seat[];
}
