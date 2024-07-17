import { HttpClient } from '@angular/common/http';
import { Injectable, WritableSignal, signal } from '@angular/core';
import { Observable, map } from 'rxjs';
import {
  Reservation,
  ReservationJSON,
  SeatAvailability,
  parseReservationJSON
} from '../../coworking.models';
import { PublicProfile } from 'src/app/profile/profile.service';

const ONE_HOUR = 60 * 60 * 1000;

@Injectable({
  providedIn: 'root'
})
export class AmbassadorXlService {
  private reservationsSignal: WritableSignal<Reservation[]> = signal([]);
  public reservations = this.reservationsSignal.asReadonly();

  constructor(private http: HttpClient) {}

  fetchReservations(): void {
    this.http
      .get<ReservationJSON[]>('/api/coworking/ambassador/xl')
      .subscribe((reservations) => {
        this.reservationsSignal.set(reservations.map(parseReservationJSON));
      });
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

  makeDropinReservation(
    seatSelection: SeatAvailability[],
    users: PublicProfile[]
  ) {
    let start = seatSelection[0].availability[0].start;
    let end = new Date(start.getTime() + 2 * ONE_HOUR);
    let reservation = {
      users: users,
      seats: seatSelection.map((seatAvailability) => {
        return { id: seatAvailability.id };
      }),
      start,
      end
    };

    return this.http
      .post<ReservationJSON>(
        '/api/coworking/ambassador/reservation',
        reservation
      )
      .pipe(map(parseReservationJSON));
  }
}
