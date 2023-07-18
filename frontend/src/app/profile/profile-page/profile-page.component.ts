/** Constructs the Profile page and stores/retrieves any necessary data for it. */

import { Component } from '@angular/core';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import { profileResolver } from '../profile.resolver';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { ProfileService } from '../profile.service';
import { Event, OrganizationSummary, Profile } from 'src/app/models.module';
import { MatSnackBar } from '@angular/material/snack-bar';
import { OrgDetailsService } from 'src/app/org-details/org-details.service';

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
  public events: Event[];

    /** Store the list of organizations. */
  public organizations: OrganizationSummary[];

  constructor(route: ActivatedRoute, private router: Router, protected profileService: ProfileService, protected orgDetailsService: OrgDetailsService, protected snackBar: MatSnackBar) {
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
  ngOnInit() {
    let profile = this.profile;
  }

  /** Event handler to delete a registration when "Cancel Registration" button is clicked.
   * @param event_id: number representing the event registration to be deleted for the user
   * @returns {void}
  */
  cancelRegistration = async (event_id: number) => {
    // Call the profileService's deleteRegistration() method.
    this.profileService.deleteRegistration(event_id);

    // Open snack bar to notify user that the registration was canceled.
    this.snackBar.open("Registration Canceled", "", { duration: 2000 })
    await new Promise(f => setTimeout(f, 750));

    // Reload the window to update the events.
    location.reload();
  }

  /** Event handler to toggle the star status of an organization.
   * @param orgId: a number representing the ID of the organiztion of to delete membership from
   */
  deleteOrgMembership = async (orgId: number) => {

    // If user is an admin/exec, they should not be able to unstar the organization.
    const filter = this.profile.organization_associations.filter(oa => oa.org_id == orgId);
    if(filter && filter.length > 0 && filter[0].membership_type !== 0) {
      if (filter[0].membership_type == 1) {
        this.snackBar.open("You cannot unstar this organization because you are an executive.", "", { duration: 2000 });
      } else if (filter[0].membership_type == 2) {
        this.snackBar.open("You cannot unstar this organization because you are an manager", "", { duration: 2000 })
      }
    }
    else {
      if(this.profile && this.profile.first_name) {
        // Call the orgDetailsService's starOrganization() method.
        this.orgDetailsService.starOrganization(orgId);
          
        // Set slight delay so page reloads after API calls finish running.
        await new Promise(f => setTimeout(f, 200));

        // Reload the window to update the events.
        location.reload();
      }
    }
  }
  
}