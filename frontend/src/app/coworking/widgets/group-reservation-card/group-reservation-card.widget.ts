import { Component, Inject } from '@angular/core';
import { PublicProfile } from 'src/app/profile/profile.service';

@Component({
  selector: 'group-reservation',
  templateUrl: './group-reservation-card.widget.html',
  styleUrls: ['./group-reservation-card.widget.css']
})
export class GroupReservation {
  selectedUsers: PublicProfile[] = [];

  constructor() {}

  onUsersChanged(users: PublicProfile[]) {
    this.selectedUsers = users;
  }
}
