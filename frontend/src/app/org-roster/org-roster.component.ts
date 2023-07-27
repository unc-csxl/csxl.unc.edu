import { Component } from '@angular/core';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { profileResolver } from '../profile/profile.resolver';
import { Observable } from 'rxjs';
import { OrgRole, OrgRoleSummary, OrganizationSummary, Profile } from '../models.module';
import { PermissionService } from '../permission.service';
import { OrgRosterService } from './org-roster.service';
import { OrgDetailsService } from '../org-details/org-details.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-org-roster',
  templateUrl: './org-roster.component.html',
  styleUrls: ['./org-roster.component.css']
})
export class OrgRosterComponent {
  public static Route: Route = {
    path: 'organization/:id/roster',
    component: OrgRosterComponent,
    title: 'Organization Roster',
    resolve: { profile: profileResolver }
  };

  /** Store the organization and its observable.  */
  public organization$: Observable<OrganizationSummary> | null = null;
  public org: OrganizationSummary;

  /** Store the org roles. */
  public orgRoles: OrgRole[] = [];

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile | null = null;

  /** Stores the user permission value for current organization. */
  public permValue: number = -1;

  /** Stores whether the user has admin permission over the current organization. */
  public adminPermission: boolean = false;

  /** Stores whether the user has manager permission over the current organization. */
  public managerPermission: boolean = false;


  /** Store the organization id. */
  org_id: number = -1;

  constructor(private route: ActivatedRoute, private router: Router, private orgRosterService: OrgRosterService, private orgDetailService: OrgDetailsService, private permission: PermissionService, protected snackBar: MatSnackBar) {

    /** Get currently-logged-in user. */
    const data = this.route.snapshot.data as { profile: Profile };
    this.profile = data.profile;

    /** Get id from the url */
    let org_id = this.route.snapshot.params['id'];
    this.org_id = org_id;

    /** Set permission value if profile exists */
    if (this.profile) {
      let assocFilter = this.profile.organization_associations.filter((orgRole) => orgRole.org_id == +this.org_id);
      if (assocFilter.length > 0) {
        this.permValue = assocFilter[0].membership_type;
        this.managerPermission = (this.permValue >= 1);
        this.adminPermission = (this.permValue >= 2);
      }
    }

    /** Initialize organization */
    this.org = {
      id: null,
      name: "",
      slug: "",
      logo: "",
      short_description: "",
      long_description: "",
      email: "",
      website: "",
      instagram: "",
      linked_in: "",
      youtube: "",
      heel_life: "",
      public: false
    };

    /** Retrieve the organization with the orgDetailService */
    if (this.org_id != -1) {
      orgDetailService.getOrganization(`${this.org_id}`).subscribe((org) => this.org = org);

      /** Retrieve the organization roles  */
      orgRosterService.getRolesForOrganization(this.org_id).subscribe((orgRoles) => {
        this.orgRoles = orgRoles.sort((a, b) => b.membership_type - a.membership_type)
      })
    }
  }

  /** Event handler to delete a membership. */
  deleteMember = async (id: number) => {

    if (this.managerPermission) {
      // First, ask user to confirm using a snackbar.
      let deleteRoleSnackBarRef = this.snackBar.open("Are you sure you want to remove this member?", "Yes");
      deleteRoleSnackBarRef.onAction().subscribe(() => {
        this.orgRosterService.deleteRoleFromOrganization(id).subscribe(() => {
          console.log('Delete successful.');
          location.reload();
        })
      })
    }
  }

  /** Event handler to promote a membership. */
  promoteMember = async (role: OrgRoleSummary) => {

    if (this.adminPermission) {
      this.orgRosterService.promoteRole(role).subscribe(() => {
        console.log('Promotion successful.');
        location.reload();
      });
    }
  }

  /** Event handler to demote a membership. */
  demoteMember = async (role: OrgRoleSummary) => {

    if (this.adminPermission) {
      // First, ask user to confirm using a snackbar.
      let demoteRoleSnackBarRef = this.snackBar.open("Are you sure you want to demote this member?", "Yes");
      demoteRoleSnackBarRef.onAction().subscribe(() => {
        this.orgRosterService.demoteRole(role).subscribe(() => {
          console.log('Demotion successful.');
          location.reload();
        });
      })

    }
  }
}

