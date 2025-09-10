import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import {
  GetRoomAvailabilityResponse,
  Reservation,
  ReservationRequest
} from '../coworking.models';
import { Observable } from 'rxjs';
import { PublicProfile } from 'src/app/profile/profile.service';

@Injectable({
  providedIn: 'root'
})
export class NewRoomReservationService {
  protected http = inject(HttpClient);

  getAvailability(): Observable<GetRoomAvailabilityResponse> {
    return this.http.get<GetRoomAvailabilityResponse>(
      '/api/coworking/rooms/availability'
    );
  }

  draftRoomReservation(request: ReservationRequest) {
    return this.http.post<Reservation>(`/api/coworking/reservation`, request);
  }
}
