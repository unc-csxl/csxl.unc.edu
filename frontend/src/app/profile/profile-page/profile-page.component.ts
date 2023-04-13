/** Constructs the Profile page and stores/retrieves any necessary data for it. */

import { Component } from '@angular/core';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import { profileResolver } from '../profile.resolver';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { ProfileService } from '../profile.service';
import { EventSummary, OrganizationSummary, Profile } from 'src/app/models.module';
import { MatSnackBar } from '@angular/material/snack-bar';
import { waitForAsync } from '@angular/core/testing';
import { delay } from 'rxjs';

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

  constructor(route: ActivatedRoute, private router: Router, protected profileService: ProfileService, protected snackBar: MatSnackBar) {
    /** Get currently-logged-in user. */
    const data = route.snapshot.data as { profile: Profile };
    this.profile = data.profile;

    /** Switch to Profile Editor Page if the user hasn't filled out any information yet. */
    if (this.profile.first_name == "") {
      this.router.navigate(['/profile-editor']);
    }

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
  async cancelRegistration(event_id: Number): Promise<void> {
    // Call the profileService's deleteRegistration() method.
    this.profileService.deleteRegistration(event_id);

    // Open snack bar to notify user that the registration was canceled.
    this.snackBar.open("Registration Canceled", "", { duration: 2000 })
    await new Promise(f => setTimeout(f, 750));

    // Reload the window to update the events.
    location.reload();
  }

  async deleteOrgMembership(org_id: Number): Promise<void> {
    this.profileService.deleteOrgMembership(org_id);

    // Open snack bar to notify user that the organization membership was deleted.
    this.snackBar.open("Organization Unfollowed", "", { duration: 2000 })
    await new Promise(f => setTimeout(f, 750));

    // Reload the window to update the organizations.
    location.reload();
  }
}
