import { HttpClient } from '@angular/common/http';
import { Injectable, WritableSignal, signal } from '@angular/core';
import {
  Reservation,
  ReservationJSON,
  parseReservationJSON
} from '../../coworking.models';

@Injectable({
  providedIn: 'root'
})
export class AmbassadorRoomService {
  private reservationsSignal: WritableSignal<Reservation[]> = signal([]);
  public reservations = this.reservationsSignal.asReadonly();

  constructor(private http: HttpClient) {}

  fetchReservations(): void {
    this.http
      .get<ReservationJSON[]>('/api/coworking/ambassador/rooms')
      .subscribe((reservations) => {
        this.reservationsSignal.set(reservations.map(parseReservationJSON));
      });
  }

  isCheckInDisabled(reservation: Reservation): boolean {
    const currentTime = new Date();
    const reservationStartTime = new Date(reservation.start);
    return reservationStartTime > currentTime;
  }

  checkIn(reservation: Reservation): void {
    this.http
      .put<ReservationJSON>(`/api/coworking/ambassador/checkin`, {
        id: reservation.id,
        state: 'CHECKED_IN'
      })
      .subscribe((_) => {
        this.fetchReservations();
      });
  }

  checkOut(reservation: Reservation) {
    this.http
      .put<ReservationJSON>(`/api/coworking/reservation/${reservation.id}`, {
        id: reservation.id,
        state: 'CHECKED_OUT'
      })
      .subscribe((_) => {
        this.fetchReservations();
      });
  }

  cancel(reservation: Reservation) {
    this.http
      .put<ReservationJSON>(`/api/coworking/reservation/${reservation.id}`, {
        id: reservation.id,
        state: 'CANCELLED'
      })
      .subscribe({
        next: (_) => {
          this.fetchReservations();
        },
        error: (err) => {
          alert(err);
        }
      });
  }
}
