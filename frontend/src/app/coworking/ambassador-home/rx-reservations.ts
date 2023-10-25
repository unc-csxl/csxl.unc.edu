import { RxObject } from 'src/app/rx-object';
import { Reservation } from '../coworking.models';

export class RxReservations extends RxObject<Reservation[]> {
  updateReservation(updates: Reservation) {
    let reservation = this.value.find((r) => r.id === updates.id);
    if (reservation) {
      Object.assign(reservation, updates);
    }
    this.notify();
  }

  remove(reservation: Reservation) {
    this.value = this.value.filter((r) => r.id !== reservation.id);
    this.notify();
  }
}
