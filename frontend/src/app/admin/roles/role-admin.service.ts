import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Role, RoleDetails } from 'src/app/role';
import { Permission, Profile } from 'src/app/profile/profile.service';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class RoleAdminService {

    constructor(protected http: HttpClient) { }

    list() {
        return this.http.get<Role[]>("/api/admin/roles");
    }

    details(id: number) {
        return this.http.get<RoleDetails>(`/api/admin/roles/${id}`);
    }

    grant(roleId: number, permission: Permission): Observable<RoleDetails> {
        return this.http.post<RoleDetails>(`/api/admin/roles/${roleId}/permission`, permission);
    }

    revoke(roleId: number, permissionId: number) {
        return this.http.delete(`/api/admin/roles/${roleId}/permission/${permissionId}`);
    }

    add(roleId: number, user: Profile) {
        return this.http.post<RoleDetails>(`/api/admin/roles/${roleId}/member`, user);
    }

    remove(roleId: number, userId: number) {
        return this.http.delete(`/api/admin/roles/${roleId}/member/${userId}`);
    }

}