/**
 * The Organization Page Component serves as a hub for students to browse all of the CS
 * organizations at UNC. Students are also able to join public organizations, filter
 * based on interests, and access social media pages of organizations to stay up-to-date.
 * 
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { ChangeDetectionStrategy, ChangeDetectorRef, Component } from '@angular/core';
import { Observable, Subject } from 'rxjs';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { OrganizationsService } from '../organizations.service';
import { OrganizationSummary, Profile } from 'src/app/models.module';
import { ActivatedRoute } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ProfileService } from 'src/app/profile/profile.service';

@Component({
  selector: 'app-organizations-page',
  templateUrl: './organizations-page.component.html',
  styleUrls: ['./organizations-page.component.css']
})
export class OrganizationsPageComponent {

  /** Route information to be used in App Routing Module */
  public static Route = {
    path: 'organizations',
    title: 'CS Organizations',
    component: OrganizationsPageComponent,
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

  constructor(
    private organizationService: OrganizationsService,
    private profileService: ProfileService,
    private route: ActivatedRoute,
    protected snackBar: MatSnackBar,
    private _cd: ChangeDetectorRef) {

    /** Get currently-logged-in user. */
    const data = route.snapshot.data as { profile: Profile };
    this.profile = data.profile;

    /** Retrieve Organizations using OrganizationsService */
    this.organizations$ = this.organizationService.getOrganizations();

    /** Retrieve all permission values for organizations */
    this.organizations$.subscribe((orgs) => {
      this.generatePermValues(orgs);
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
    if (filter && filter.length > 0 && filter[0].membership_type >= 0) {
      if (filter[0].membership_type == 1) {
        this.snackBar.open("You cannot unstar this organization because you are an executive.", "", { duration: 2000 });
      } else if (filter[0].membership_type == 2) {
        this.snackBar.open("You cannot unstar this organization because you are a manager.", "", { duration: 2000 })
      }
      else {
        // If here, the memership can be deleted
        // First, confirm with the user in a snackbar
        let deleteMembershipSnackBarRef = this.snackBar.open("Are you sure you want to leave this organization?", "Leave");
        deleteMembershipSnackBarRef.onAction().subscribe(() => {
          // If snackbar button pressed, delete membership
          const orgRoleId = filter[0].id!;
          this.organizationService.deleteOrganizationRole(orgRoleId).subscribe(() => {
            this.snackBar.open("You have left the organization.", "", { duration: 2000 });
            this.profileService.refreshProfile();
            this.profileService.profile$.subscribe(profile => this.profile = profile!);
            this.permValues.set(orgId, -1)
          })
        })
      }
    }
    else {
      // Check if user is authenticated
      if (this.profile && this.profile.first_name) {
        // Get data on organization we are adding to.
        this.organizations$.subscribe((orgs) => {
          const org = orgs.filter((o) => o.id == orgId)[0]!
          // Then, check if organization is public or not.
          if (org.public) {
            // If public, join organization.
            this.organizationService.createOrganizationRole(this.profile!.id!, orgId).subscribe((newOrgRole) => {
              this.snackBar.open(`Welcome to ${org.slug}!`, "", { duration: 2000 });
              this.profileService.refreshProfile();
              this.profileService.profile$.subscribe(profile => this.profile = profile!);
              this.permValues.set(org.id!, 0)
            })
          }
          else {
            // If not public, show a snackbar.
            this.snackBar.open(`To join ${org.slug}, you must be added manually by the organization!`, "Close");
          }
        })
      }
    }
  }

  generatePermValues = (organizations: OrganizationSummary[]) => {
    organizations.map((org) => {
      const filter = this.profile.organization_associations.filter(oa => oa.org_id == org.id);
      if (filter && filter.length > 0) {
        this.permValues.set(org.id!, filter[0].membership_type);
      }
      else {
        this.permValues.set(org.id!, -1)
      }
    })
  }

}
