/** Constructs the Profile page and stores/retrieves any necessary data for it. */

import { Component } from '@angular/core';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import { profileResolver } from '../profile.resolver';
import { ActivatedRoute, Route } from '@angular/router';
import { ProfileService } from '../profile.service';
import { EventSummary, OrganizationSummary, Profile } from 'src/app/models.module';

@Component({
  selector: 'app-profile-page',
  templateUrl: './profile-page.component.html',
  styleUrls: ['./profile-page.component.css']
})
export class ProfilePageComponent {

  /** Route information to be used in App Routing Module */
  public static Route: Route = {
    path: 'profile',
    component: ProfilePageComponent, 
    title: 'Profile', 
    canActivate: [isAuthenticated], 
    resolve: { profile: profileResolver }
  };

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;
  /** Store the list of events. */
  public events: EventSummary[];
  public organizations: OrganizationSummary[];

  constructor(route: ActivatedRoute, protected profileService: ProfileService) {
    /** Get currently-logged-in user. */
    const data = route.snapshot.data as { profile: Profile };
    this.profile = data.profile;

    /** Get events associated with the user. */
    this.events = profileService.getUserEvents()!;

    /** Get organizations associated with the user. */
    this.organizations = profileService.getUserOrganizations()!;
  }

  /** Initialize the profile to be the currently-logged-in user's profile. */
  ngOnInit(): void {
    let profile = this.profile;
  }

  /** Event handler to delete a registration when "Cancel Registration" button is clicked.
   * @param event_id: Number representing the event registration to be deleted for the user
   * @returns {void}
  */
  cancelRegistration(event_id: Number): void {
    // Call the profileService's deleteRegistration() method.
    this.profileService.deleteRegistration(event_id);

    // Reload the window to update the events.
    location.reload();
  }
}
