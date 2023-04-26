/** Constructs the Admin Organization List page and stores/retrieves any necessary data for it. */

import { ChangeDetectorRef, Component, ViewChild, inject } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { permissionGuard } from 'src/app/permission.guard';
import { OrganizationsAdminService } from '../organizations-admin.service';
import { Organization } from 'src/app/models.module';
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
    }
    ngOnInit() {
        this.orgAdminService.list().subscribe(organizations => {
            this.dataSource.data = organizations;
            this._cd.detectChanges();
        });
    }
    onClick(organization: Organization) {
        this.router.navigate(['admin', 'organizations', organization.id]);
    }

    createOrganization() {
        this.router.navigate(['organization', '-1', 'org-editor']);
    }

}