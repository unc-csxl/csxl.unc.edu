/** Constructs the Admin Organization List page and stores/retrieves any necessary data for it. */

import { Component, inject } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { permissionGuard } from 'src/app/permission.guard';
import { OrganizationsAdminService } from '../organizations-admin.service';
import { Organization } from 'src/app/models.module';

@Component({
    selector: 'app-admin-organizations-list',
    templateUrl: './admin-organizations-list.component.html',
    styleUrls: ['./admin-organizations-list.component.css']
})
export class AdminOrganizationsListComponent {

    /** Organizations List */
    public organizations: Organization[];

    public displayedColumns: string[] = ['name'];

    /** Route information to be used in Admin Routing Module */
    public static Route = {
        path: 'organizations',
        component: AdminOrganizationsListComponent,
        title: 'Organization Administration',
        canActivate: [permissionGuard('organizations.list', 'organizations/')],
        resolve: { organizations: () => inject(OrganizationsAdminService).list() },
    }

    constructor(
        private router: Router,
        route: ActivatedRoute,
    ) {
        let data = route.snapshot.data as { organizations: Organization[] };
        this.organizations = data.organizations;
    }

    onClick(organization: Organization) {
        this.router.navigate(['admin', 'organizations', organization.id]);
    }

}