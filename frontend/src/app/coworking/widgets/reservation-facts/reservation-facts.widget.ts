import { Component, Input } from '@angular/core';
import { Reservation } from '../../coworking.models';
import { PublicProfile } from 'src/app/profile/profile.service';

@Component({
  selector: 'coworking-reservation-facts',
  templateUrl: './reservation-facts.widget.html',
  styleUrl: './reservation-facts.widget.css',
  standalone: false
})
export class ReservationFactsWidget {
  @Input() reservation!: Reservation;

  checkinDeadline(reservationStart: Date, reservationEnd: Date): Date {
    return new Date(
      Math.min(
        reservationStart.getTime() + 10 * 60 * 1000,
        reservationEnd.getTime()
      )
    );
  }

  usersList() {
    return this.reservation.users.map((profile) => profile as PublicProfile);
  }
}
