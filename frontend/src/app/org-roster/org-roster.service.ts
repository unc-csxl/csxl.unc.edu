/** Abstracts HTTP request functionality for organizations away from the backend database */

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { OrgRole, OrgRoleSummary } from '../models.module';

@Injectable({
    providedIn: 'root'
})

export class OrgRosterService {

    constructor(private http: HttpClient) { }

    /** Returns the organization roles for an organization using the backend HTTP get request.
     * @param orgId: Number representing the organization ID
     * @returns {Observable<OrgRoleSummary>}
     */
    getRolesForOrganization = (orgId: number) => {
        return this.http.get<OrgRole[]>("/api/orgroles/org/" + orgId);
    }

    /** Delete an organization role based on the role's ID using the backend HTTP delete request.
     * @param orgId: Number representing the organization ID
     */
    deleteRoleFromOrganization = (orgId: number) => {
        return this.http.delete<void>("/api/orgroles/" + orgId);
    }

    /** Promotes a role
     * @param orgRole: Role to promote
     * @returns {Observable<OrgRoleSummary>}
     */
    promoteRole = (orgRole: OrgRoleSummary) => {
        let newSummary: OrgRoleSummary = {
            id: orgRole.id,
            user_id: orgRole.user_id,
            org_id: orgRole.org_id,
            membership_type: 1,
            timestamp: orgRole.timestamp
        }
        return this.http.post<OrgRoleSummary>("/api/orgroles", newSummary);
    }

    demoteRole = (orgRole: OrgRoleSummary) => {
        let newSummary: OrgRoleSummary = {
            id: orgRole.id,
            user_id: orgRole.user_id,
            org_id: orgRole.org_id,
            membership_type: 0,
            timestamp: orgRole.timestamp
        }
        return this.http.post<OrgRoleSummary>("/api/orgroles", newSummary);
    }


    // /** Returns the updated organization object from the backend database table using the backend HTTP put request. 
    //  * @param org: OrganizationSummary representing the updated organization
    //  * @returns {Observable<OrganizationSummary>}
    //  */
    // updateOrganization = (org: OrganizationSummary) => {
    //     if (org.id) {
    //         return this.http.put<OrganizationSummary>("/api/organizations", org);
    //     } else {
    //         return this.http.post<OrganizationSummary>("/api/organizations", org);
    //     }
    // }
}
