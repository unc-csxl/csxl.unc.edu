import { Component, inject } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { permissionGuard } from 'src/app/permission.guard';
import { Role } from 'src/app/role';
import { AdminRoleDetailsComponent } from '../details/admin-role-details.component';
import { RoleAdminService } from '../role-admin.service';

@Component({
    selector: 'app-admin-roles-list',
    templateUrl: './admin-roles-list.component.html',
    styleUrls: ['./admin-roles-list.component.css']
})
export class AdminRolesListComponent {

    public roles: Role[];

    public displayedColumns: string[] = ['name'];

    public static Route = {
        path: 'roles',
        component: AdminRolesListComponent,
        title: 'Role Administration',
        canActivate: [permissionGuard('role.list', 'role/')],
        resolve: { roles: () => inject(RoleAdminService).list() },
    }

    constructor(
        private router: Router,
        route: ActivatedRoute,
    ) {
        let data = route.snapshot.data as { roles: Role[] };
        this.roles = data.roles;
    }

    onClick(role: Role) {
        this.router.navigate(['admin', 'roles', role.id]);
    }

}