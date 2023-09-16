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
import { OrganizationAdminService } from '/workspace/frontend/src/app/admin/organization/organization-admin.service';
import { Organization } from 'src/app/organization/organization.service';
import { Observable } from 'rxjs';
import { MatTableDataSource } from '@angular/material/table';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
    selector: 'app-admin-organization-list',
    templateUrl: './admin-organization-list.component.html',
    styleUrls: ['./admin-organization-list.component.css']
})
export class AdminOrganizationListComponent {

    /** Organizations List */
    public organizations$: Observable<Organization[]>;

    public displayedColumns: string[] = ['name'];

    dataSource = new MatTableDataSource<Organization>();

    /** Route information to be used in Admin Routing Module */
    public static Route = {
        path: 'organizations',
        component: AdminOrganizationListComponent,
        title: 'Organization Administration',
        canActivate: [permissionGuard('organization.list', 'organization/')],
    }

    constructor(
        private router: Router,
        private organizationAdminService: OrganizationAdminService,
        private snackBar: MatSnackBar
    ) {
        this.organizations$ = organizationAdminService.list();

        this.organizationAdminService.list().subscribe(organizations => {
            this.dataSource.data = organizations;
        });
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
    deleteOrganization(slug: string): void {
        let confirmDelete = this.snackBar.open("Are you sure you want to delete this organization?", "Delete");
        confirmDelete.onAction().subscribe(() => {
            this.organizationAdminService.deleteOrganization(slug).subscribe(() => {
            this.snackBar.open("This organization has been deleted.", "", { duration: 2000 });
          })
        });
    }
}