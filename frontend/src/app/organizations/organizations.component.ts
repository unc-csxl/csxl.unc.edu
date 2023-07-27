/** Constructs the Organizations page and stores/retrieves any necessary data for it. */

import { Component } from '@angular/core';
import { Observable } from 'rxjs';
import { profileResolver } from '../profile/profile.resolver';
import { OrganizationsService } from './organizations.service';
import { OrganizationSummary, Profile } from '../models.module';
import { OrgDetailsService } from '../org-details/org-details.service';
import { ActivatedRoute } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-organizations',
  templateUrl: './organizations.component.html',
  styleUrls: ['./organizations.component.css']
})
export class OrganizationsComponent {

  /** Route information to be used in App Routing Module */
  public static Route = {
    path: 'organizations',
    title: 'CS Organizations',
    component: OrganizationsComponent,
    canActivate: [],
    resolve: { profile: profileResolver }
  }

  /** Store Observable list of Organizations */
  public organizations$: Observable<OrganizationSummary[]>;

  /** Store searchBarQuery */
  searchBarQuery = "";


  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;

  /** Stores the user permission value for current organization. */
  public permValues: Map<number, number> = new Map();

  constructor(private organizationService: OrganizationsService, protected orgDetailService: OrgDetailsService, private route: ActivatedRoute, protected snackBar: MatSnackBar) {

    /** Get currently-logged-in user. */
    const data = route.snapshot.data as { profile: Profile };
    this.profile = data.profile;

    /** Retrieve Organizations using OrganizationsService */
    this.organizations$ = this.organizationService.getOrganizations();

    /** Retrieve all permission values for organizations */
    this.organizations$.subscribe((orgs) => {
      orgs.map((org) => {
        const filter = this.profile.organization_associations.filter(oa => oa.org_id == org.id);
        if (filter && filter.length > 0) {
          this.permValues.set(org.id!, filter[0].membership_type);
        }
        else {
          this.permValues.set(org.id!, -1)
        }
      })
    })
  }

  /** Initialize the profile to be the currently-logged-in user's profile. */
  ngOnInit() {
    let profile = this.profile;
  }

  /**
   * Event handler to toggle membership status of an organization.
   * @param orgId: a number representing the ID of the organization to be starred
   */
  toggleOrganizationMembership = async (orgId: number) => {

    // If user is an admin, they should not be able to unstar the organization.
    const filter = this.profile.organization_associations.filter(oa => oa.org_id == orgId);
    if (filter && filter.length > 0 && filter[0].membership_type !== 0) {
      if (filter[0].membership_type == 1) {
        this.snackBar.open("You cannot unstar this organization because you are an executive.", "", { duration: 2000 });
      } else if (filter[0].membership_type == 2) {
        this.snackBar.open("You cannot unstar this organization because you are a manager.", "", { duration: 2000 })
      }
    }
    else {
      if (this.profile && this.profile.first_name) {
        // Call the orgDetailsService's toggleOrganizationMembership() method.
        this.orgDetailService.toggleOrganizationMembership(orgId);
      }
    }
  }

  /** Event handler to toggle the star status of an organization.
   * @deprecated
   * @param orgId: a number representing the ID of the organization to be starred
   */
  starOrganization = async (orgId: number) => {

    // If user is an admin, they should not be able to unstar the organization.
    const filter = this.profile.organization_associations.filter(oa => oa.org_id == orgId);
    if (filter && filter.length > 0 && filter[0].membership_type !== 0) {
      if (filter[0].membership_type == 1) {
        this.snackBar.open("You cannot unstar this organization because you are an executive.", "", { duration: 2000 });
      } else if (filter[0].membership_type == 2) {
        this.snackBar.open("You cannot unstar this organization because you are a manager.", "", { duration: 2000 })
      }
    }
    else {
      if (this.profile && this.profile.first_name) {
        // Call the orgDetailsService's starOrganization() method.
        this.orgDetailService.starOrganization(orgId);

        // Set slight delay so page reloads after API calls finish running.
        await new Promise(f => setTimeout(f, 200));

        // Reload the window to update the events.
        location.reload();
      }
    }
  }
}
