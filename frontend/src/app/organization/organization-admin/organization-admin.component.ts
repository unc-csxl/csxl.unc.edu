/**
 * The Admin Organization List page retrieves and displays a list of
 * CS organizations and provides functionality to create/delete them.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2024
 * @license MIT
 */

import { Component, Signal } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Organization } from '../organization.model';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable } from 'rxjs';
import { Profile } from '.../profile/profile.service';
import { profileResolver } from '.../profile/profile.resolver';
import { OrganizationService } from '../organization.service';
import { PermissionService } from '.../permission.service';

@Component({
  selector: 'app-organization-admin',
  templateUrl: './organization-admin.component.html',
  styleUrls: ['./organization-admin.component.css']
})
export class OrganizationAdminComponent {
  /** Organizations List */
  public organizations: Signal<Organization[]>;

  public displayedColumns: string[] = ['name'];
  /** Profile of signed in user */
  protected profile: Profile;
  /** List of displayed organizations for the signed in user */
  protected displayedOrganizations: Signal<Organization[]>;

  /** Route information to be used in Organization Routing Module */
  public static Route = {
    path: 'admin',
    component: OrganizationAdminComponent,
    title: 'Organization Administration',
    resolve: { profile: profileResolver }
  };

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private snackBar: MatSnackBar,
    private organizationService: OrganizationService,
    private permissionService: PermissionService
  ) {
    this.organizations = organizationService.organizations;
    this.displayedOrganizations = organizationService.adminOrganizations;

    /** Get the profile data of the signed in user */
    const data = this.route.snapshot.data as {
      profile: Profile;
    };
    this.profile = data.profile;
  }

  /** Resposible for generating delete and create buttons in HTML code when admin signed in.
   * @returns {Observable<boolean>}
   */
  adminPermissions(): Observable<boolean> {
    return this.permissionService.check('organization.create', '*');
  }

  /** Event handler to open Organization Editor for the selected organization.
   * @param organization: organization to be edited
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
   */
  deleteOrganization(organization: Organization): void {
    let confirmDelete = this.snackBar.open(
      'Are you sure you want to delete this organization?',
      'Delete',
      { duration: 15000 }
    );
    confirmDelete.onAction().subscribe(() => {
      this.organizationService
        .deleteOrganization(organization)
        .subscribe(() => {
          this.snackBar.open('This organization has been deleted.', '', {
            duration: 2000
          });
        });
    });
  }
}
