/**
 * The Admin Organization List page retrieves and displays a list of
 * CS organizations and provides functionality to create/delete them.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { permissionGuard } from 'src/app/permission.guard';
import { Organization } from '../../organization.model';
import { MatSnackBar } from '@angular/material/snack-bar';
import { OrganizationAdminService } from '../organization-admin.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-organization-list-admin',
  templateUrl: './organization-list-admin.component.html',
  styleUrls: ['./organization-list-admin.component.css']
})
export class OrganizationListAdminComponent {
  /** Organizations List */
  public organizations$: Observable<Organization[]>;

  public displayedColumns: string[] = ['name'];

  /** Route information to be used in Organization Routing Module */
  public static Route = {
    path: 'list/admin',
    component: OrganizationListAdminComponent,
    title: 'Organization Administration',
    canActivate: [permissionGuard('organization.list', 'organization')]
  };

  constructor(
    private router: Router,
    private snackBar: MatSnackBar,
    private organizationAdminService: OrganizationAdminService
  ) {
    this.organizations$ = organizationAdminService.organizations$;
    organizationAdminService.list();
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
