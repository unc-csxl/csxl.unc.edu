/**
 * The Organization Service abstracts HTTP requests to the backend
 * from the components.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AuthenticationService } from '../authentication.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable } from 'rxjs';
import { Organization } from './organization.model';
import { Role } from '../role';

@Injectable({
  providedIn: 'root'
})
export class OrganizationService {
  constructor(
    protected http: HttpClient,
    protected auth: AuthenticationService,
    protected snackBar: MatSnackBar
  ) {}

  /** Returns all organization entries from the backend database table using the backend HTTP get request.
   * @returns {Observable<Organization[]>}
   */
  getOrganizations(): Observable<Organization[]> {
    return this.http.get<Organization[]>('/api/organizations');
  }

  /** Returns the organization object from the backend database table using the backend HTTP get request.
   * @param slug: String representing the organization slug
   * @returns {Observable<Organization>}
   */
  getOrganization(slug: string): Observable<Organization> {
    return this.http.get<Organization>('/api/organizations/' + slug);
  }

  /** Returns the new organization object from the backend database table using the backend HTTP post request.
   * @param organization: OrganizationSummary representing the new organization
   * @returns {Observable<Organization>}
   */
  createOrganization(organization: Organization): Observable<Organization> {
    return this.http.post<Organization>('/api/organizations', organization);
  }

  /** Returns the updated organization object from the backend database table using the backend HTTP put request.
   * @param organization: OrganizationSummary representing the updated organization
   * @returns {Observable<Organization>}
   */
  updateOrganization(organization: Organization): Observable<Organization> {
    return this.http.put<Organization>('/api/organizations', organization);
  }

  /** Returns the new role object from the backend database table using the backend HTTP post request.
   * @param role: Role representing the new role
   * @returns {Observable<Role>}
   */
  createRole(role: Role): Observable<Role> {
    return this.http.post<Role>('/api/admin/roles', role);
  }
}
