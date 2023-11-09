import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, map, shareReplay, tap } from 'rxjs';
import {
  Reservation,
  ReservationJSON,
  parseReservationJSON
} from '../coworking.models';
import { RxReservation } from './rx-reservation';

@Injectable({
  providedIn: 'root'
})
export class ReservationService {
  private reservations: Map<number, RxReservation> = new Map();

  constructor(private http: HttpClient) {}

  get(id: number): Observable<Reservation> {
    let reservation = this.getRxReservation(id);
    reservation.load();
    return reservation.value$;
  }

  cancel(reservation: Reservation) {
    let endpoint = `/api/coworking/reservation/${reservation.id}`;
    let payload = { id: reservation.id, state: 'CANCELLED' };
    return this.http.put<ReservationJSON>(endpoint, payload).pipe(
      map(parseReservationJSON),
      tap((reservation) => {
        let rxReservation = this.getRxReservation(reservation.id);
        rxReservation.set(reservation);
      })
    );
  }

  confirm(reservation: Reservation) {
    let endpoint = `/api/coworking/reservation/${reservation.id}`;
    let payload = { id: reservation.id, state: 'CONFIRMED' };
    return this.http.put<ReservationJSON>(endpoint, payload).pipe(
      map(parseReservationJSON),
      tap((reservation) => {
        let rxReservation = this.getRxReservation(reservation.id);
        rxReservation.set(reservation);
      })
    );
  }

  checkout(reservation: Reservation) {
    let endpoint = `/api/coworking/reservation/${reservation.id}`;
    let payload = { id: reservation.id, state: 'CHECKED_OUT' };
    return this.http.put<ReservationJSON>(endpoint, payload).pipe(
      map(parseReservationJSON),
      tap((reservation) => {
        let rxReservation = this.getRxReservation(reservation.id);
        rxReservation.set(reservation);
      })
    );
  }

  private getRxReservation(id: number): RxReservation {
    let reservation = this.reservations.get(id);
    if (reservation === undefined) {
      let loader = this.http
        .get<ReservationJSON>(`/api/coworking/reservation/${id}`)
        .pipe(
          map(parseReservationJSON),
          shareReplay({ windowTime: 1000, refCount: true })
        );
      reservation = new RxReservation(loader);
      this.reservations.set(id, reservation);
    }
    return reservation;
  }
}
