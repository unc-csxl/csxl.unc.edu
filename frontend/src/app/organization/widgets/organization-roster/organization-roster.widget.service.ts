import { Observable } from 'rxjs';
import {
  OrganizationMembership,
  OrganizationRole
} from '../../organization.model';
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

  /** Removes a student represented by a membership_id from an organization represented by a slug.
   * @param slug: String representing the organization slug
   * @param membership_id: String representing the user's ID
   * @returns { Observable<void> }
   */
  deleteOrganizationMembership(
    slug: string,
    membership_id: number
  ): Observable<void> {
    return this.http.delete<void>(
      '/api/organizations/' + slug + '/roster/' + membership_id
    );
  }

  /** Updates a student represented by a member_id's role (enum) in an organization represented by a slug.
   * @param slug: String representing the organization slug
   * @param membership_id: String representing the user's ID
   * @param new_role: Enum representing the new role
   * @returns { Observable<void> }
   */
  updateOrganizationMembership(
    slug: string,
    membership_id: number,
    new_role: OrganizationRole
  ): Observable<OrganizationMembership> {
    return this.http.put<OrganizationMembership>(
      '/api/organizations/' + slug + '/roster/' + membership_id,
      new_role as string
    );
  }
}
