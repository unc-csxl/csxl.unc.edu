/**
 * The Admin Organization List page retrieves and displays a list of
 * CS organizations and provides functionality to create/delete them.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { OrganizationAdminPermissionGuard } from 'src/app/organization/organization-admin/organization-admin-permission.guard';
import { Organization } from '../../organization.model';
import { MatSnackBar } from '@angular/material/snack-bar';
import { OrganizationAdminService } from '../organization-admin.service';
import { Observable, map } from 'rxjs';
import {
  Permission,
  Profile
} from '/workspace/frontend/src/app/profile/profile.service';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { organizationResolver } from '../../organization.resolver';

@Component({
  selector: 'app-organization-list-admin',
  templateUrl: './organization-list-admin.component.html',
  styleUrls: ['./organization-list-admin.component.css']
})
export class OrganizationListAdminComponent implements OnInit {
  /** Organizations List */
  public organizations$: Observable<Organization[]>;

  public displayedColumns: string[] = ['name'];
  /** Profile of signed in user */
  protected profile: Profile;
  /** List of displayed organizations for the signed in user */
  protected displayedOrganizations$: Observable<Organization[]>;

  /** Route information to be used in Organization Routing Module */
  public static Route = {
    path: 'admin',
    component: OrganizationListAdminComponent,
    title: 'Organization Administration',
    canActivate: [OrganizationAdminPermissionGuard()],
    resolve: { profile: profileResolver, organizations: organizationResolver }
  };

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private snackBar: MatSnackBar,
    private organizationAdminService: OrganizationAdminService
  ) {
    this.organizations$ = organizationAdminService.organizations$;
    organizationAdminService.list();
    this.displayedOrganizations$ = this.organizations$;

    /** Get the profile data of the signed in user */
    const data = this.route.snapshot.data as {
      profile: Profile;
    };
    this.profile = data.profile;
  }

  ngOnInit() {
    let profilePermissions: Permission[] = this.profile.permissions;
    if (profilePermissions[0].resource !== '*') {
      /** Filter and return the slug of the users organization permissions */
      let userOrganizationPermissions: string[] = profilePermissions
        .filter((element) => element.resource.includes('organization'))
        .map((element) => {
          return element.resource.substring(13);
        });
      /** Update displayedOrganizations$ to only include the organizations the user has permissions for */
      this.displayedOrganizations$ = this.organizations$.pipe(
        map((organizations) =>
          organizations.filter((organization) =>
            userOrganizationPermissions.includes(organization.slug)
          )
        )
      );
    }
  }

  /** Resposible for generating delete and create buttons in HTML code when admin signed in */
  adminPermissions(): boolean {
    return this.profile.permissions[0].resource === '*';
  }

  /** Event handler to open Organization Editor for the selected organization.
   * @param organization: organization to be edited
   * @returns void
   */
  editOrganization(organization: Organization): void {
    this.router.navigate(['organizations', organization.slug, 'edit']);
  }

  /** Event handler to open the Organization Editor to create a new organization */
  createOrganization(): void {
    // Navigate to the org editor for a new organization (slug = create)
    this.router.navigate(['organizations', 'new', 'edit']);
  }

  /** Delete an organization object from the backend database table using the backend HTTP post request.
   * @param organization_id: unique number representing the updated organization
   * @returns void
   */
  deleteOrganization(organization: Organization): void {
    let confirmDelete = this.snackBar.open(
      'Are you sure you want to delete this organization?',
      'Delete',
      { duration: 15000 }
    );
    confirmDelete.onAction().subscribe(() => {
      this.organizationAdminService
        .deleteOrganization(organization)
        .subscribe(() => {
          this.snackBar.open('This organization has been deleted.', '', {
            duration: 2000
          });
        });
    });
  }
}
