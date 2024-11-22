import { Observable } from 'rxjs';
import { OrganizationMembership } from '../../organization.model';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class OrganizationRosterService {
  /** Constructor */
  constructor(protected http: HttpClient) {}

  /** Gets an organization's roster (represented as an array of OrganizationMemberships) based on its slug.
   * @param slug: String representing the organization slug
   * @returns {Observable<OrganizationMembership[] | undefined>}
   */
  getOrganizationRoster(
    slug: string
  ): Observable<OrganizationMembership[] | undefined> {
    return this.http.get<OrganizationMembership[]>(
      '/api/organizations/' + slug + '/roster'
    );
  }

  /** Adds a student represented by a user_id to an organization represented by a slug.
   * @param slug: String representing the organization slug
   * @param user_id: String representing the user's ID
   * @returns {Observable<OrganizationMembership | undefined>}
   */
  addOrganizationMembership(
    slug: string,
    user_id: number
  ): Observable<OrganizationMembership | undefined> {
    return this.http.post<OrganizationMembership>(
      '/api/organizations/' + slug + '/roster',
      user_id
    );
  }
}
