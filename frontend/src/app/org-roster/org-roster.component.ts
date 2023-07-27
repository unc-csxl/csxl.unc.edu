import { Component, inject } from '@angular/core';
import { ActivatedRoute, ResolveFn, Route, Router } from '@angular/router';
import { profileResolver } from '../profile/profile.resolver';
import { Observable, ReplaySubject, debounceTime, filter, map, mergeMap, startWith } from 'rxjs';
import { OrgRole, OrgRoleSummary, Organization, OrganizationSummary, Profile } from '../models.module';
import { PermissionService } from '../permission.service';
import { OrgRosterService } from './org-roster.service';
import { OrgDetailsService } from '../org-details/org-details.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { OrganizationsAdminService } from '../admin/organizations/organizations-admin.service';
import { FormControl } from '@angular/forms';
import { MatAutocompleteSelectedEvent } from '@angular/material/autocomplete';
import { ProfileService } from '../profile/profile.service';

let titleResolver: ResolveFn<string> = () => {
  let route = inject(ActivatedRoute);
  let orgId = route.snapshot.params['id'];
  if (orgId) {
    let orgDetailSvc = inject(OrgDetailsService);
    let org$ = orgDetailSvc.getOrganization(orgId);
    return org$.pipe(map(org => {
      if (org) {
        return `${org.name} Roster`;
      } else {
        return "Oranization Roster (undefined org)"
      }
    }))
  } else {
    return "Organization Roster (undefined route)";
  }
}

@Component({
  selector: 'app-org-roster',
  templateUrl: './org-roster.component.html',
  styleUrls: ['./org-roster.component.css']
})
export class OrgRosterComponent {
  public static Route: Route = {
    path: 'organization/:id/roster',
    component: OrgRosterComponent,
    title: titleResolver,
    resolve: { profile: profileResolver }
  };

  /** Store the organization and its observable.  */
  public organization$: Observable<OrganizationSummary> | null = null;
  public org: Organization;

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

  // User Lookup Form Data
  public userLookup: FormControl = new FormControl();
  protected filteredUsers: ReplaySubject<Profile[]> = new ReplaySubject();
  public filteredUsers$: Observable<Profile[]> = this.filteredUsers.asObservable();
  public selectedUser?: Profile;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private orgRosterService: OrgRosterService,
    private orgDetailService: OrgDetailsService,
    private organizationsAdminService: OrganizationsAdminService,
    private permission: PermissionService,
    private profileService: ProfileService,
    protected snackBar: MatSnackBar
  ) {

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
      public: false,
      events: [],
      users: [],
      user_associations: []
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

  /** Retrieves the list of users for the Add User dropdown. */
  public ngOnInit() {
    this.filteredUsers$ = this.userLookup.valueChanges.pipe(
      startWith(''),
      filter((search: string) => search.length > 2),
      debounceTime(100),
      mergeMap((search) => this.profileService.search(search))
    );
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

  /** Handler for when a user is selected in the autocomplete list. */
  public onOptionSelected = (event: MatAutocompleteSelectedEvent) => {
    let user = event.option.value as Profile;
    this.selectedUser = user;
    this.userLookup.setValue('');
  }

  /** Handler for when a user is changed in the autocomplete list. */
  public changeSelectedMember = () => {
    this.selectedUser = undefined;
    this.userLookup.setValue('');
  }

  /** Event handler for adding a manager to the organization */
  public onAddManager = (selectedUser: Profile) => {
    if (!selectedUser) { return; }
    // Handle if user is already in organization
    if (this.orgRoles.map((orgRole) => orgRole.user_id).filter((e) => e == selectedUser.id).length > 0) {
      this.snackBar.open("This member is already in your roster!", "", { duration: 2000 })
      return;
    }
    // Add the manager based on the selectedUser (from the form) and the current organization id
    this.organizationsAdminService.addMember(selectedUser, this.org)
      .subscribe((org_role: OrgRole) => {
        // Update the organization in the component
        this.organizationsAdminService.details(org_role.org_id).subscribe(org => this.org = org);
        location.reload();
      })
  }
}

