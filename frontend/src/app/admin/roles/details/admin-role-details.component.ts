import { Component, inject } from '@angular/core';
import { ActivatedRoute, ActivatedRouteSnapshot, Router } from '@angular/router';
import { permissionGuard } from 'src/app/permission.guard';
import { Permission, Profile } from 'src/app/profile/profile.service';
import { RoleDetails } from 'src/app/role';
import { RoleAdminService } from '../role-admin.service';

@Component({
    selector: 'app-admin-role-details',
    templateUrl: './admin-role-details.component.html',
    styleUrls: ['./admin-role-details.component.css']
})
export class AdminRoleDetailsComponent {

    public role: RoleDetails;

    public grantPermissionForm: Permission = {
        action: '',
        resource: ''
    };

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
        private roleAdminService: RoleAdminService,
        private router: Router,
        route: ActivatedRoute,
    ) {
        let data = route.snapshot.data as { role: RoleDetails };
        this.role = data.role;
    }

    public grantPermission() {
        if (this.grantPermissionForm.action === '' || this.grantPermissionForm.resource === '') {
            return;
        }
        this.roleAdminService.grant(this.role.id, this.grantPermissionForm).subscribe((role: RoleDetails) => {
            this.role = role;
            this.grantPermissionForm = { action: '', resource: '' };
        });
    }

    public onRevokePermission(permission: Permission) {
        this.roleAdminService.revoke(this.role.id, permission.id!).subscribe(() => {
            this.role.permissions = this.role.permissions.filter(p => p !== permission);
        });
    }

    public onRemoveUser(user: Profile) {
        this.roleAdminService.remove(this.role.id, user.id!).subscribe(() => {
            this.role.users = this.role.users.filter(u => u !== user);
        });
    }

}