import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Role, RoleDetails } from 'src/app/role';
import { Permission } from 'src/app/profile/profile.service';

@Injectable({ providedIn: 'root' })
export class RoleAdminService {

    constructor(protected http: HttpClient) { }

    list() {
        return this.http.get<Role[]>("/api/admin/roles");
    }

    details(id: number) {
        return this.http.get<RoleDetails>(`/api/admin/roles/${id}`);
    }

    revoke(roleId: number, permissionId: number) {
        return this.http.delete(`/api/admin/roles/${roleId}/permission/${permissionId}`)
    }

}