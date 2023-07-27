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
    list = () => {
        return this.http.get<Organization[]>("/api/organizations");
    }

    /** Returns a single Organization based on the given organization id
     * @param id: a number representing an Organization id
     * @returns {Organization}
     */
    details = (id: number) => {
        return this.http.get<Organization>(`/api/organizations/${id}`);
    }

    /** Revokes manager status from the provided OrgRole
     * @param org_role: a valid OrgRole model
     * @returns {OrgRole}
     */
    removeManager = (org_role: OrgRole) => {
        const updatedRole: OrgRoleSummary = {
            id: org_role.id,
            user_id: org_role.user_id,
            org_id: org_role.org_id,
            membership_type: 1,
            timestamp: org_role.timestamp
        }
        // update the manager role (type = 0) rather than deleting them
        return this.http.post<OrgRole>(`/api/orgroles`, updatedRole);
    }

    /** Adds a manager to an organization
     * @param user: Profile of the user you want to add as a manager
     * @param organization: Organization that you want to add a manager to
     * @returns {Observable<OrgRole>}
     */
    addManager = (user: Profile, organization: Organization) => {
        const newRole: OrgRoleSummary = {
            id: null,
            user_id: user.id!,
            org_id: organization.id!,
            membership_type: 1,
            timestamp: new Date()
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

    /** Adds a member to an organization
     * @param user: Profile of the user you want to add as a member
     * @param organization: Organization that you want to add a member to
     * @returns {Observable<OrgRole>}
     */
    addMember = (user: Profile, organization: Organization) => {
        const newRole: OrgRoleSummary = {
            id: null,
            user_id: user.id!,
            org_id: organization.id!,
            membership_type: 0,
            timestamp: new Date()
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

    /** Adds an admin to an organization
 * @param user: Profile of the user you want to add as an admin
 * @param organization: Organization that you want to add an admin to
 * @returns {Observable<OrgRole>}
 */
    addAdmin = (user: Profile, organization: Organization) => {
        const newRole: OrgRoleSummary = {
            id: null,
            user_id: user.id!,
            org_id: organization.id!,
            membership_type: 2,
            timestamp: new Date()
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

    /** Creates an organization
     * @param newOrg: Organization object that you want to add to the database
     * @returns {Observable<Organization>}
     */
    createOrganization = (newOrg: OrganizationSummary) => {
        return this.http.post<Organization>("/api/organizations", newOrg)
    }

    /** Deletes an organization
     * @param org_id: id of the organization object to delete
     * @returns {Observable<Organization>}
     */
    deleteOrganization = (org_id: number) => {
        return this.http.delete<Organization>(`/api/organizations/${org_id}`);
    }

}