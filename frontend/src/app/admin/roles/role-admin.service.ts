import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Role, RoleDetails } from 'src/app/role';

@Injectable({ providedIn: 'root' })
export class RoleAdminService {

    constructor(protected http: HttpClient) { }

    list() {
        return this.http.get<Role[]>("/api/admin/roles");
    }

    details(id: number) {
        return this.http.get<RoleDetails>(`/api/admin/roles/${id}`);
    }

}