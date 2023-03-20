import { Component, inject } from '@angular/core';
import { ActivatedRoute, ActivatedRouteSnapshot, Router } from '@angular/router';
import { permissionGuard } from 'src/app/permission.guard';
import { RoleDetails } from 'src/app/role';
import { RoleAdminService } from '../role-admin.service';

@Component({
    selector: 'app-admin-role-details',
    templateUrl: './admin-role-details.component.html',
    styleUrls: []
})
export class AdminRoleDetailsComponent {

    public role: RoleDetails;

    public static Route = {
        path: 'roles/:id',
        component: AdminRoleDetailsComponent,
        title: 'Role Administration',
        canActivate: [permissionGuard('role.details', 'role/{id}')],
        resolve: { 
            role: (route: ActivatedRouteSnapshot) => {
                const id = parseInt(route.paramMap.get('id')!);
                return inject(RoleAdminService).details(id); 
            }
        }
    }

    constructor(
        private router: Router,
        route: ActivatedRoute,
    ) {
        let data = route.snapshot.data as { role: RoleDetails };
        this.role = data.role;
    }

}