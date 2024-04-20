/**
 * The Group Reservation Widget allows users to add other users while drafting a reservation.
 *
 * @author Matt Vu
 * @copyright 2024
 * @license MIT
 */
import { Component, Inject } from '@angular/core';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';
import { Profile, PublicProfile } from 'src/app/profile/profile.service';
import { ProfileService } from 'src/app/profile/profile.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'group-reservation',
  templateUrl: './group-reservation-card.widget.html',
  styleUrls: ['./group-reservation-card.widget.css']
})
export class GroupReservation {
  selectedUsers: PublicProfile[] = [];
  public loggedInUser: Profile | undefined;
  private subscription: Subscription;

  constructor(
    public dialogRef: MatDialogRef<GroupReservation>,
    public profileService: ProfileService
  ) {
    this.subscription = this.profileService.profile$.subscribe((profile) => {
      if (profile) {
        this.loggedInUser = profile;
        const loggedInPublicProfile = this.convertToPublicProfile(profile);

        if (
          !this.selectedUsers.find(
            (user) => user.id === loggedInPublicProfile.id
          )
        ) {
          this.selectedUsers.unshift(loggedInPublicProfile);
        }
      }
    });
  }

  onUsersChanged(newUsers: PublicProfile[]) {
    if (this.loggedInUser) {
      const loggedInUserProfile = this.convertToPublicProfile(
        this.loggedInUser
      );
      const filteredNewUsers = newUsers.filter(
        (user) => user.id !== loggedInUserProfile.id
      );
      this.selectedUsers = [loggedInUserProfile, ...filteredNewUsers];
    } else {
      this.selectedUsers = [...newUsers];
    }
  }

  addUsers() {
    this.dialogRef.close(this.selectedUsers);
    console.log(this.selectedUsers);
  }

  private convertToPublicProfile(profile: Profile): PublicProfile {
    // Converts Profile object into a PublicProfile object.
    return {
      id: profile.id ?? 0,
      first_name: profile.first_name ?? 'N/A',
      last_name: profile.last_name ?? 'N/A',
      pronouns: profile.pronouns ?? 'N/A',
      email: profile.email ?? 'N/A',
      github_avatar: profile.github_avatar
    };
  }
}
