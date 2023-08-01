import { Profile } from "../models.module";

export interface OperatingHoursJSON {
    id: number;
    start: string;
    end: string;
}

export interface OperatingHours {
    id: number;
    start: Date;
    end: Date;
}

export const parseOperatingHoursJSON = (json: OperatingHoursJSON): OperatingHours => {
    return {
        id: json.id,
        start: new Date(json.start),
        end: new Date(json.end)
    }
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

export interface ReservationJSON {
    id: number;
    start: string;
    end: string;
    users: Profile[];
    seats: Seat[];
    walkin: boolean;
}

export interface Reservation {
    id: number;
    start: Date;
    end: Date;
    users: Profile[];
    seats: Seat[];
    walkin: boolean;
}

export const parseReservationJSON = (json: ReservationJSON): Reservation => {
    return {
        id: json.id,
        start: new Date(json.start),
        end: new Date(json.end),
        users: json.users,
        seats: json.seats,
        walkin: json.walkin
    };
};

export interface ReservationRequest {
    start: Date;
    end: Date;
    users: Profile[];
    seats: Seat[];
}

export interface CoworkingStatus {
    my_reservations: Reservation[];
    operating_hours: OperatingHours[];
}

export interface CoworkingStatusJSON {
    my_reservations: ReservationJSON[];
    operating_hours: OperatingHoursJSON[];
}

export const parseCoworkingStatusJSON = (json: CoworkingStatusJSON): CoworkingStatus => {
    return {
        my_reservations: json.my_reservations.map(parseReservationJSON),
        operating_hours: json.operating_hours.map(parseOperatingHoursJSON)
    }
};