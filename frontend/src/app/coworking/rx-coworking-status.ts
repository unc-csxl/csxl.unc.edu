import { RxObject } from "../rx-object";
import { CoworkingStatus, Reservation } from "./coworking.models";

export class RxCoworkingStatus extends RxObject<CoworkingStatus> {

    pushReservation(reservation: Reservation): void {
        this.value.my_reservations.push(reservation);
        this.notify();
    }

    updateReservation(reservation: Reservation): void {
        this.value.my_reservations = this.value.my_reservations.map((r) => {
            return r.id !== reservation.id ? r : reservation;
        });
        this.notify();
    }

    removeReservation(reservationToRemove: Reservation): void {
        this.value.my_reservations = this.value.my_reservations.filter(reservation => reservationToRemove.id !== reservation.id);
        this.notify();
    }

}
