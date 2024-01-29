/**
 * The Room Reservation Service abstracts HTTP requests to the backend
 * from the components.
 *
 * @author Aarjav Jain, John Schachte, Nick Wherthey, Yuvraj Jain
 * @copyright 2023
 * @license MIT
 */

import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { map, Observable } from 'rxjs';
import {
  parseReservationJSON,
  Reservation,
  ReservationJSON
} from '../coworking.models';
import { ReservationService } from '../reservation/reservation.service';

@Injectable({
  providedIn: 'root'
})
export class RoomReservationService extends ReservationService {
  constructor(http: HttpClient) {
    super(http);
  }

  /** Returns all room reservations from the backend database table using the backend HTTP get request.
   * @returns {Observable<RoomReservation[]>}
   */

  getReservationsByState(state: string): Observable<Reservation[]> {
    // Create HttpParams with the state
    let params = new HttpParams().set('state', state);
    return this.http
      .get<ReservationJSON[]>('/api/coworking/room-reservations/', {
        params
      })
      .pipe(map((reservations) => reservations.map(parseReservationJSON)));
  }

  checkin(reservation: Reservation): Observable<Reservation> {
    let endpoint = `/api/coworking/reservation/${reservation.id}`;
    let payload = { id: reservation.id, state: 'CHECKED_IN' };
    return this.http
      .put<ReservationJSON>(endpoint, payload)
      .pipe(map(parseReservationJSON));
  }

  deleteRoomReservation(reservation: Reservation): Observable<Reservation> {
    return this.http.delete<Reservation>(
      `/api/coworking/reservation/${reservation.id}`
    );
  }
}
