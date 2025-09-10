import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { GetRoomAvailabilityResponse } from '../coworking.models';
import { Observable } from 'rxjs';

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
}
