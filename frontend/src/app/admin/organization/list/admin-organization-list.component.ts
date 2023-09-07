/** Constructs the Admin Organization List page and stores/retrieves any necessary data for it. */

import { ChangeDetectorRef, Component, inject } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { permissionGuard } from 'src/app/permission.guard';
import { OrganizationAdminService } from '/workspace/frontend/src/app/admin/organization/organization-admin.service';
import { Organization } from 'src/app/organization/organization.service';
import { Observable } from 'rxjs';
import { MatTableDataSource } from '@angular/material/table';

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
        private _cd: ChangeDetectorRef
    ) {
        this.organizations$ = organizationAdminService.list();

        this.organizationAdminService.list().subscribe(organizations => {
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
}