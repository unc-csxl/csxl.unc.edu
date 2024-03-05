import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import {
  Reservation,
  ReservationJSON,
  SeatAvailability,
  parseReservationJSON
} from '../../coworking.models';
import { RxReservations } from '../rx-reservations';

@Injectable({
  providedIn: 'root'
})
export class AmbassadorXlService {
  private reservations: RxReservations = new RxReservations();
  public reservations$: Observable<Reservation[]> = this.reservations.value$;

  constructor(private http: HttpClient) {}

  fetchReservations(): void {
    this.http
      .get<ReservationJSON[]>('/api/coworking/ambassador/xl')
      .subscribe((reservations) => {
        this.reservations.set(reservations.map(parseReservationJSON));
      });
  }

  checkIn(reservation: Reservation): void {
    this.http
      .put<ReservationJSON>(`/api/coworking/ambassador/checkin`, {
        id: reservation.id,
        state: 'CHECKED_IN'
      })
      .subscribe((reservationJson) => {
        this.reservations.updateReservation(
          parseReservationJSON(reservationJson)
        );
      });
  }

  checkOut(reservation: Reservation) {
    this.http
      .put<ReservationJSON>(`/api/coworking/reservation/${reservation.id}`, {
        id: reservation.id,
        state: 'CHECKED_OUT'
      })
      .subscribe((reservationJson) => {
        this.reservations.updateReservation(
          parseReservationJSON(reservationJson)
        );
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
          this.reservations.remove(reservation);
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
