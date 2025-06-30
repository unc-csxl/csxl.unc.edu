// Service for direct CRUD operations on an organization's roster.
// Located in the base organization directory since it is used by both roster widget and details card.
import { Observable } from 'rxjs';
import {
  OrganizationMembership,
  OrganizationMembershipPermissionLevel,
  OrganizationMembershipStatus
} from './organization.model';
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
    user_id: number,
    organization_id: number
  ): Observable<OrganizationMembership | undefined> {
    return this.http.post<OrganizationMembership>(
      '/api/organizations/' + slug + '/roster',
      { user_id, organization_id }
    );
  }

  /** Removes a membership represented by a membership_id from an organization represented by a slug.
   * @param slug: String representing the organization slug
   * @param membership_id: String representing the membership's ID
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
   * @param membership_id: String representing the membership's ID
   * @param user_id: String representing the user's ID
   * @param organization_id: String representing the organization's ID
   * @param term_id: String representing the term ID
   * @param new_title: String representing the new title
   * @param new_permission_level: OrganizationMembershipPermissionLevel representing the new permission level
   * @param new_status: OrganizationMembershipStatus representing the new status
   * @returns { Observable<void> }
   */
  updateOrganizationMembership(
    slug: string,
    membership_id: number,
    user_id: number | null,
    organization_id: number,
    term_id: string,
    new_title?: string,
    new_permission_level?: OrganizationMembershipPermissionLevel,
    new_status?: OrganizationMembershipStatus
  ): Observable<OrganizationMembership> {
    const updatePayload: any = {};
    updatePayload.id = membership_id;
    updatePayload.user_id = user_id;
    updatePayload.organization_id = organization_id;
    updatePayload.term_id = term_id;
    if (new_title !== undefined) updatePayload.title = new_title;
    if (new_permission_level !== undefined)
      updatePayload.permission_level = new_permission_level;
    if (new_status !== undefined) updatePayload.status = new_status;

    return this.http.put<OrganizationMembership>(
      '/api/organizations/' + slug + '/roster',
      updatePayload
    );
  }
}
