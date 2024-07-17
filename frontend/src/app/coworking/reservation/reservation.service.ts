/**
 * This service handles retrieving and manipulating reservations.
 *
 * @author Kris Jordan <kris@cs.unc.edu>, Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2023 - 2024
 * @license MIT
 */

import { HttpClient } from '@angular/common/http';
import { Injectable, WritableSignal, signal } from '@angular/core';
import { Observable, map, tap } from 'rxjs';
import {
  Reservation,
  ReservationJSON,
  parseReservationJSON
} from '../coworking.models';

@Injectable({
  providedIn: 'root'
})
export class ReservationService {
  private reservationSignal: WritableSignal<Reservation | undefined> =
    signal(undefined);
  reservation = this.reservationSignal.asReadonly();

  constructor(protected http: HttpClient) {}

  cancel(reservation: Reservation) {
    let endpoint = `/api/coworking/reservation/${reservation.id}`;
    let payload = { id: reservation.id, state: 'CANCELLED' };
    return this.http.put<ReservationJSON>(endpoint, payload).pipe(
      map(parseReservationJSON),
      tap((reservation) => {
        this.reservationSignal.set(reservation);
      })
    );
  }

  confirm(reservation: Reservation) {
    let endpoint = `/api/coworking/reservation/${reservation.id}`;
    let payload = { id: reservation.id, state: 'CONFIRMED' };
    return this.http.put<ReservationJSON>(endpoint, payload).pipe(
      map(parseReservationJSON),
      tap((reservation) => {
        this.reservationSignal.set(reservation);
      })
    );
  }

  checkout(reservation: Reservation) {
    let endpoint = `/api/coworking/reservation/${reservation.id}`;
    let payload = { id: reservation.id, state: 'CHECKED_OUT' };
    return this.http.put<ReservationJSON>(endpoint, payload).pipe(
      map(parseReservationJSON),
      tap((reservation) => {
        this.reservationSignal.set(reservation);
      })
    );
  }

  checkin(reservation: Reservation) {
    let endpoint = `/api/coworking/reservation/${reservation.id}`;
    let payload = { id: reservation.id, state: 'CHECKED_IN' };
    return this.http.put<ReservationJSON>(endpoint, payload).pipe(
      map(parseReservationJSON),
      tap((reservation) => {
        this.reservationSignal.set(reservation);
      })
    );
  }

  getReservation(id: number) {
    return this.http
      .get<ReservationJSON>(`/api/coworking/reservation/${id}`)
      .pipe(map(parseReservationJSON))
      .subscribe((reservation) => {
        this.reservationSignal.set(reservation);
      });
  }

  getReservationObservable(id: number): Observable<Reservation> {
    return this.http
      .get<ReservationJSON>(`/api/coworking/reservation/${id}`)
      .pipe(map(parseReservationJSON));
  }
}
