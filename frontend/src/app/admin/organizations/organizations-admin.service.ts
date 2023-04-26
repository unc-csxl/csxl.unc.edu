import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { OrgRole, OrgRoleSummary, Organization, OrganizationSummary, Profile } from 'src/app/models.module';

@Injectable({ providedIn: 'root' })
export class OrganizationsAdminService {

    constructor(protected http: HttpClient) { }

    /** Returns a list of all Organizations
     * @returns {Organization[]}
     */
    list(): Observable<Organization[]> {
        return this.http.get<Organization[]>("/api/organizations");
    }

    /** Returns a single Organization based on the given organization id
     * @param id: a number representing an Organization id
     * @returns {Organization}
     */
    details(id: Number) {
        return this.http.get<Organization>(`/api/organizations/${id}`);
    }

    /** Revokes manager status from the provided OrgRole
     * @param org_role: a valid OrgRole model
     * @returns {OrgRole}
     */
    removeManager(org_role: OrgRole) {
        const updatedRole: OrgRoleSummary = {
            id: org_role.id,
            user_id: org_role.user_id,
            org_id: org_role.org_id,
            membership_type: 1
        }
        // update the manager role (type = 0) rather than deleting them
        return this.http.post<OrgRole>(`/api/orgroles`, updatedRole);
    }

    /** Updates manager status for the specified user in the organization
     * @param user_id: a number representing the id of the user to be given manager status
     * @param org_id: a number representing the organization the user should get access to
     * @returns {Observable<OrgRole>}
     */
    addManager(user: Profile, organization: Organization): Observable<OrgRole> {
        const newRole: OrgRoleSummary = {
            id: null,
            user_id: user.id!,
            org_id: organization.id!,
            membership_type: 2
        }
        // Check if the user role already exists
        for (let role of organization.user_associations) {
            if (role.user_id == user.id && role.org_id == organization.id) {
                // Set the newRole model id to the id of the role that matches the user and org
                newRole.id = role.id;
                // Update the org role with the post request
                return this.http.post<OrgRole>(`/api/orgroles`, newRole);
            }
        }
        return this.http.post<OrgRole>(`/api/orgroles`, newRole);
    }

    createOrganization(newOrg: OrganizationSummary) {
        return this.http.post<Organization>("/api/organizations", newOrg)
    }

    deleteOrganization(org_id: number) {
        return this.http.delete<Organization>(`/api/organizations/${org_id}`);
    }

}