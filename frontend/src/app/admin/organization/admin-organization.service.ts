/**
 * The Admin Organization Service abstracts backend calls from the
 * Admin organization List Component.
 * 
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Organization } from "/workspace/frontend/src/app/organization/organization.service";
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class AdminOrganizationService {

    constructor(protected http: HttpClient) { }

    /** Returns a list of all Organizations
     * @returns {Observable<Organization[]>}
     */
    list(): Observable<Organization[]> {
        return this.http.get<Organization[]>("/api/organizations");
    }

    /** Creates an organization
     * @param newOrganization: Organization object that you want to add to the database
     * @returns {Observable<Organization>}
     */
    createOrganization(newOrganization: Organization): Observable<Organization> {
        return this.http.post<Organization>("/api/organizations", newOrganization)
    }

    /** Deletes an organization
     * @param organization_id: id of the organization object to delete
     * @returns {Observable<Organization>}
     */
    deleteOrganization(slug: string): Observable<Organization> {
        return this.http.delete<Organization>(`/api/organizations/${slug}`);
    }
}

export { Organization };
