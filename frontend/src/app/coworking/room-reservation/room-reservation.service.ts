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
import { catchError, map, Observable, of } from 'rxjs';
import {
  parseReservationJSON,
  Reservation,
  ReservationJSON
} from '../coworking.models';
import { ReservationService } from '../reservation/reservation.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { RxUpcomingReservation } from '../rx-coworking-status';

@Injectable({
  providedIn: 'root'
})
export class RoomReservationService extends ReservationService {
  private upcomingReservations: RxUpcomingReservation = new RxUpcomingReservation();
  public upcomingReservations$: Observable<Reservation[]> = this.upcomingReservations.value$
  public findActiveReservationPredicate: (r: Reservation) => boolean = (r:Reservation) => {
    let now = new Date();
    const activeStates = ["CONFIRMED","CHECKED_IN"];
    return r.start <= now && r.end > now && activeStates.includes(r.state)
  }
  
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

  // private findActiveReservationPredicate(reservation:Reservation){
  //   let now = new Date();
  //   const activeStates = ["CONFIRMED","CHECKED_IN"];
  //   return reservation.start <= now && reservation.end > now && activeStates.includes(reservation.state)
  // }

  pollUpcomingRoomReservation(snackBar: MatSnackBar){
    console.log("running poll UpcomingRoomReservations");

    // predicate to determine if this is a non active upcoming room reservation
    const isUpcomingRoomReservation = (r:Reservation) => !this.findActiveReservationPredicate(r) && !!r && !!r.room
    
    this.getReservationsByState('CONFIRMED').pipe(
      map(reservations => reservations.filter(r => isUpcomingRoomReservation(r))),
      catchError((err: Error) => {
        const message = 'Error while fetching upcoming reservations.';
        snackBar.open(message, '', { duration: 8000 });
        console.error(err);
        return of([]);
      })
    ).subscribe((upcomingRoomReservations) => this.upcomingReservations.set(upcomingRoomReservations));
  }
}
