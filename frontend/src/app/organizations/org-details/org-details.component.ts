/**
 * The Organization Detail Component displays more information and options regarding
 * UNC CS organizations.
 * 
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { Component, inject } from '@angular/core';
import { ActivatedRoute, ActivatedRouteSnapshot, ResolveFn, Route } from '@angular/router';
import { MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';
import { Observable, Subscription, map, tap } from 'rxjs';
import { Organization, OrgRole, Profile } from 'src/app/models.module';
import { MatSnackBar } from '@angular/material/snack-bar';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { OrganizationsService } from '../organizations.service';
import { ProfileService } from 'src/app/profile/profile.service';

let titleResolver: ResolveFn<string> = (route: ActivatedRouteSnapshot) => {
  let orgId = route.params['id'];

  let orgDetailSvc = inject(OrganizationsService);
  let org$ = orgDetailSvc.getOrganization(orgId);
  return org$.pipe(map(org => {
    if (org) {
      return `${org.name}`;
    } else {
      return "Organization Details"
    }
  }))
}

@Component({
  selector: 'app-org-details',
  templateUrl: './org-details.component.html',
  styleUrls: ['./org-details.component.css']
})
export class OrgDetailsComponent {
  public static Route: Route = {
    path: 'organization/:id',
    component: OrgDetailsComponent,
    title: titleResolver,
    resolve: { profile: profileResolver }
  };

  public organization$: Observable<Organization>;
  public organization: Organization | undefined = undefined;
  id: string = '';

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;

  /** Stores the user permission value for current organization. */
  public permValue: number = -1;

  /** Stores whether the user has admin permission over the current organization. */
  public adminPermission: boolean = false;

  /** Stores executives of the current organization */
  public executives: OrgRole[] = [];

  constructor(
    private orgService: OrganizationsService,
    private profileService: ProfileService,
    iconRegistry: MatIconRegistry,
    sanitizer: DomSanitizer,
    private route: ActivatedRoute,
    protected snackBar: MatSnackBar) {
    /** Import Logos using MatIconRegistry */
    iconRegistry.addSvgIcon('instagram', sanitizer.bypassSecurityTrustResourceUrl('https://simpleicons.org/icons/instagram.svg'));
    iconRegistry.addSvgIcon('github', sanitizer.bypassSecurityTrustResourceUrl('https://simpleicons.org/icons/github.svg'));
    iconRegistry.addSvgIcon('linkedin', sanitizer.bypassSecurityTrustResourceUrl('https://simpleicons.org/icons/linkedin.svg'))
    iconRegistry.addSvgIcon('youtube', sanitizer.bypassSecurityTrustResourceUrl('https://simpleicons.org/icons/youtube.svg'))

    /** Get currently-logged-in user. */
    const data = route.snapshot.data as { profile: Profile };
    this.profile = data.profile;

    /** Load current route ID */
    this.route.params.subscribe(params => this.id = params["id"]);

    /** Retrieve Organization using OrgDetailsService */
    this.organization$ = this.orgService.getOrganizationDetail(this.id);
    this.organization$.subscribe(org => this.organization = org);
    this.organization$.subscribe(org => {
      this.organization = org;
      this.orgService.getRolesForOrganization(org.id!).subscribe((associations) => {
        associations.forEach((association) => {
          if (association.membership_type >= 1) {
            this.executives.push(association);
          }
        })
      })
    })

    /** Set permission value if profile exists */
    if (this.profile) {
      let assocFilter = this.profile.organization_associations.filter((orgRole) => orgRole.org_id == +this.id);
      if (assocFilter.length > 0) {
        this.permValue = assocFilter[0].membership_type;
        this.adminPermission = (this.permValue >= 2);
      }
    }
  }

  /** Initialize the profile to be the currently-logged-in user's profile. */
  ngOnInit() {
    let profile = this.profile;
  }

  /**
   * Event handler to toggle membership status of an organization.
   * @param orgId: a number representing the ID of the organization to be starred
   */
  toggleOrganizationMembership = async () => {

    // If user is an admin, they should not be able to unstar the organization.
    const filter = this.profile.organization_associations.filter(oa => oa.org_id == this.organization!.id);
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
          this.orgService.deleteOrganizationRole(orgRoleId).subscribe(() => {
            this.snackBar.open("You have left the organization.", "", { duration: 2000 });
            this.profileService.refreshProfile();
            this.profileService.profile$.subscribe(profile => this.profile = profile!);
            this.permValue = -1;
          })
        })
      }
    }
    else {
      // Check if user is authenticated
      if (this.profile && this.profile.first_name) {
        // Get data on organization we are adding to.
        this.organization$.subscribe((org) => {

          // Then, check if organization is public or not.
          if (org.public) {
            // If public, join organization.
            this.orgService.createOrganizationRole(this.profile!.id!, this.organization!.id!).subscribe((newOrgRole) => {
              this.snackBar.open(`Welcome to ${org.slug}!`, "", { duration: 2000 });
              this.profileService.refreshProfile();
              this.profileService.profile$.subscribe(profile => this.profile = profile!);
              this.permValue = 0;
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

  /** Event handler to delete an event.
   * @param event_id: Number representing the event to be deleted.
   * @returns {void}
   */
  deleteEvent = async (event_id: number) => {
    // Call the orgDetailsService's deleteEvent() method.
    this.orgService.deleteEvent(event_id).subscribe(_ => {
      this.organization$ = this.orgService.getOrganizationDetail(this.id);
      this.organization$.subscribe(organization => {
        this.organization = organization;
        this.snackBar.open("Deleted event", "", { duration: 2000 });
      });
    })
  }
}