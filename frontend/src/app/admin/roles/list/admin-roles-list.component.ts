import { Component, inject } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { permissionGuard } from 'src/app/permission.guard';
import { Role } from 'src/app/role';
import { RoleAdminService } from '../role-admin.service';
import { NavigationService } from 'src/app/navigation/navigation.service';

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
        private roleService: RoleAdminService,
        private navService: NavigationService,
        private router: Router,
        route: ActivatedRoute,
    ) {
        let data = route.snapshot.data as { roles: Role[] };
        this.roles = data.roles;
    }

    onClick(role: Role) {
        this.router.navigate(['admin', 'roles', role.id]);
    }

    onClickAddRole() {
        let name = window.prompt("What is the name of the role?");
        if (name) {
            this.roleService.create(name).subscribe({
                next: (role) => this.router.navigate(['admin', 'roles', role.id]),
                error: (err) => this.navService.error(err)
            });
        }
    }

}