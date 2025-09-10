import { Component } from '@angular/core';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { NewRoomReservationService } from './new-room-reservation.service';
import { GetRoomAvailabilityResponse } from '../coworking.models';

@Component({
    selector: 'app-new-room-reservation',
    templateUrl: './new-room-reservation.component.html',
    styleUrl: './new-room-reservation.component.css',
    standalone: false
})
export class NewRoomReservationComponent {
  public static Route = {
    path: 'new-reservation',
    title: 'New Reservation',
    component: NewRoomReservationComponent,
    canActivate: [isAuthenticated],
    resolve: { profile: profileResolver }
  };

  availability: GetRoomAvailabilityResponse | undefined = undefined;

  constructor(private roomReservationService: NewRoomReservationService) {
    this.roomReservationService.getAvailability().subscribe((result) => {
      this.availability = result;
    });
  }
}
