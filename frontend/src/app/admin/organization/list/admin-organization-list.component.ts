/**
 * The Admin Organization List page retrieves and displays a list of
 * CS organizations and provides functionality to create/delete them.
 * 
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { permissionGuard } from 'src/app/permission.guard';
import { Organization } from 'src/app/organization/organization.service';
import { MatTableDataSource } from '@angular/material/table';
import { MatSnackBar } from '@angular/material/snack-bar';
import { adminOrganizationResolver } from "/workspace/frontend/src/app/admin/organization/admin-organization.resolver";
import { AdminOrganizationService } from '../admin-organization.service';

@Component({
    selector: 'app-admin-organization-list',
    templateUrl: './admin-organization-list.component.html',
    styleUrls: ['./admin-organization-list.component.css']
})
export class AdminOrganizationListComponent {

    /** Organizations List */
    public organizations: Organization[];

    public displayedColumns: string[] = ['name'];

    /** Route information to be used in Admin Routing Module */
    public static Route = {
        path: 'organizations',
        component: AdminOrganizationListComponent,
        title: 'Organization Administration',
        canActivate: [permissionGuard('organization.list', 'organization/')],
        resolve: { organizations: adminOrganizationResolver }
    }

    constructor(
        private router: Router,
        private snackBar: MatSnackBar,
        private adminOrganizationService: AdminOrganizationService,
        private route: ActivatedRoute
    ) {
        const data = this.route.snapshot.data as { organizations: Organization[] };
        this.organizations = data.organizations;
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
            this.adminOrganizationService.deleteOrganization(slug).subscribe(() => {
                this.organizations = this.organizations.filter(o => o.slug !== slug);
                this.snackBar.open("This organization has been deleted.", "", { duration: 2000 });
          })
        });
    }
}