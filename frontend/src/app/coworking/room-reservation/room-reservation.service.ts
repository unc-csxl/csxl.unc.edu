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

  getNumHoursStudyRoomReservations(): Observable<string> {
    return this.http.get<string>('/api/coworking/user-reservations/');
  }
}