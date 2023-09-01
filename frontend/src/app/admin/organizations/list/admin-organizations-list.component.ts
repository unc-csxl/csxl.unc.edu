/** Constructs the Admin Organization List page and stores/retrieves any necessary data for it. */

import { ChangeDetectorRef, Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { permissionGuard } from 'src/app/permission.guard';
import { OrganizationsAdminService } from '../organizations-admin.service';
import { Organization } from 'src/app/organizations/organizations.service';
import { Observable } from 'rxjs';
import { MatTableDataSource } from '@angular/material/table';

@Component({
    selector: 'app-admin-organizations-list',
    templateUrl: './admin-organizations-list.component.html',
    styleUrls: ['./admin-organizations-list.component.css']
})
export class AdminOrganizationsListComponent {

    /** Organizations List */
    public organizations$: Observable<Organization[]>;

    public displayedColumns: string[] = ['name'];

    dataSource = new MatTableDataSource<Organization>();

    /** Route information to be used in Admin Routing Module */
    public static Route = {
        path: 'organizations',
        component: AdminOrganizationsListComponent,
        title: 'Organization Administration',
        canActivate: [permissionGuard('organizations.list', 'organizations/')],
    }

    constructor(
        private router: Router,
        route: ActivatedRoute,
        private orgAdminService: OrganizationsAdminService,
        private _cd: ChangeDetectorRef
    ) {
        this.organizations$ = orgAdminService.list();

        this.orgAdminService.list().subscribe(organizations => {
            this.dataSource.data = organizations;
            this._cd.detectChanges();
        });
    }

    /** Event handler for opening the Admin Organization Details for the given organization
     * @param organization: a valid Organization model
     */
    onClick = (organization: Organization) => {
        // Navigate to the organization's detail page
        this.router.navigate(['admin', 'organizations', organization.id]);
    }

    /** Event handler to open the Organization Editor to create a new organization */
    createOrganization = () => {
        // Navigate to the org editor for a new organization (id = -1)
        this.router.navigate(['organization', '-1', 'org-editor']);
    }

    /** Deletes an organization
     * @param org: organization object to delete
     * @returns {Observable<Organization>}
     */
    deleteOrganization = (org: Organization) => {
        return this.orgAdminService.deleteOrganization(org.id!);
    }

}