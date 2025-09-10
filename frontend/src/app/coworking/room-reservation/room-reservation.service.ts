import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import {
  GetRoomAvailabilityResponse,
  Reservation,
  ReservationRequest
} from '../coworking.models';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class NewRoomReservationService {
  protected http = inject(HttpClient);

  getAvailability(date?: Date): Observable<GetRoomAvailabilityResponse> {
    const params: { [key: string]: string } = {};
    if (date) {
      params['date'] = date.toISOString();
    }
    return this.http.get<GetRoomAvailabilityResponse>(
      '/api/coworking/rooms/availability',
      { params }
    );
  }

  draftRoomReservation(request: ReservationRequest) {
    return this.http.post<Reservation>(`/api/coworking/reservation`, request);
  }
}
