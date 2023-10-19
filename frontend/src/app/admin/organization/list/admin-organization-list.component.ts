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
import { Organization } from '../../../organization/organization.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AdminOrganizationService } from '../admin-organization.service';
import { Observable } from 'rxjs';

@Component({
    selector: 'app-admin-organization-list',
    templateUrl: './admin-organization-list.component.html',
    styleUrls: ['./admin-organization-list.component.css']
})
export class AdminOrganizationListComponent {

    /** Organizations List */
    public organizations$: Observable<Organization[]>;

    public displayedColumns: string[] = ['name'];

    /** Route information to be used in Admin Routing Module */
    public static Route = {
        path: 'organizations',
        component: AdminOrganizationListComponent,
        title: 'Organization Administration',
        canActivate: [ permissionGuard('organization.list', 'organization/') ]
    }

    constructor(
        private router: Router,
        private snackBar: MatSnackBar,
        private adminOrganizationService: AdminOrganizationService
    ) {
        this.organizations$ = adminOrganizationService.organizations$;
        adminOrganizationService.list();
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
        let confirmDelete = this.snackBar.open("Are you sure you want to delete this organization?", "Delete");
        confirmDelete.onAction().subscribe(() => {
            this.adminOrganizationService.deleteOrganization(organization).subscribe(() => {
            this.snackBar.open("This organization has been deleted.", "", { duration: 2000 });
          })
        });
    }
}