import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import {
  NewRoomReservationBlock,
  RoomReservationBlock
} from './coworking.models';

@Injectable({ providedIn: 'root' })
export class RoomReservationBlockService {
  private readonly api = '/api/coworking/room-reservation-blocks';

  constructor(private http: HttpClient) {}

  list(includeDisabled = true): Observable<RoomReservationBlock[]> {
    const params = new HttpParams().set('include_disabled', includeDisabled);
    return this.http.get<RoomReservationBlock[]>(this.api, { params });
  }

  create(block: NewRoomReservationBlock): Observable<RoomReservationBlock> {
    return this.http.post<RoomReservationBlock>(this.api, block);
  }

  update(
    id: number,
    block: NewRoomReservationBlock
  ): Observable<RoomReservationBlock> {
    return this.http.put<RoomReservationBlock>(`${this.api}/${id}`, block);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.api}/${id}`);
  }
}
