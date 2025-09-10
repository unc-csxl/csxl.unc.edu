import { Component } from '@angular/core';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import { profileResolver } from 'src/app/profile/profile.resolver';

@Component({
  selector: 'app-new-room-reservation',
  templateUrl: './new-room-reservation.component.html',
  styleUrl: './new-room-reservation.component.css'
})
export class NewRoomReservationComponent {
  public static Route = {
    path: 'new-reservation',
    title: 'New Reservation',
    component: NewRoomReservationComponent,
    canActivate: [isAuthenticated],
    resolve: { profile: profileResolver }
  };
}
