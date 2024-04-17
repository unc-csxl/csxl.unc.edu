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
  private upcomingReservations: RxUpcomingReservation =
    new RxUpcomingReservation();
  public upcomingReservations$: Observable<Reservation[]> =
    this.upcomingReservations.value$;
  public findActiveReservationPredicate: (r: Reservation) => boolean = (
    r: Reservation
  ) => {
    let now = new Date();
    let soon = new Date(
      Date.now() + 10 /* minutes */ * 60 /* seconds */ * 1000 /* milliseconds */
    );
    const activeStates = ['DRAFT', 'CONFIRMED', 'CHECKED_IN'];
    return r.start <= soon && r.end > now && activeStates.includes(r.state);
  };

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

  getNumHoursStudyRoomReservations(): Observable<string> {
    return this.http.get<string>('/api/coworking/user-reservations/');
  }

  /**
   * Polls for upcoming room reservations with a 'CONFIRMED' state that are not currently active.
   *
   * This method fetches reservations and filters them to find upcoming reservations based on a specific predicate.
   * The predicate checks that the reservation is not active and that it has a defined room.
   * In case of an error while fetching reservations, it displays an error message using `MatSnackBar`.
   *
   * @param {MatSnackBar} snackBar - The MatSnackBar service used to display notifications or error messages.
   *
   * @example
   * pollUpcomingRoomReservation(this.snackBar);
   *
   * @remarks
   * This method utilizes RxJS operators to process the stream of reservations. The `map` operator is used to filter
   * reservations based on the provided predicate. The `catchError` operator handles any errors during the fetching process,
   * displaying an error message and logging the error to the console.
   *
   * @returns {void} - This method does not return a value; it sets the upcoming reservations in a state management variable.
   */
  pollUpcomingRoomReservation(snackBar: MatSnackBar) {
    // predicate to determine if this is a non active upcoming room reservation
    const isUpcomingRoomReservation = (r: Reservation) =>
      !this.findActiveReservationPredicate(r) && !!r && !!r.room;

    this.getReservationsByState('CONFIRMED')
      .pipe(
        map((reservations) =>
          reservations.filter((r) => isUpcomingRoomReservation(r))
        ),
        catchError((err: Error) => {
          const message = 'Error while fetching upcoming reservations.';
          snackBar.open(message, '', { duration: 8000 });
          console.error(err);
          return of([]);
        })
      )
      .subscribe((upcomingRoomReservations) =>
        this.upcomingReservations.set(upcomingRoomReservations)
      );
  }
}
