import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Profile } from 'src/app/profile/profile.service';
import { Role } from 'src/app/role';

@Injectable({ providedIn: 'root' })
export class RoleAdminService {

    constructor(protected http: HttpClient) { }

    list() {
        return this.http.get<Role[]>("/api/admin/roles");
    }

}