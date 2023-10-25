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
import { Observable, tap } from 'rxjs';
import { RxOrganization } from '../../organization/rx-organization';
import { Organization } from '../../organization/organization.model';

@Injectable({ providedIn: 'root' })
export class AdminOrganizationService {
  private organizations: RxOrganization = new RxOrganization();
  public organizations$: Observable<Organization[]> = this.organizations.value$;

  constructor(protected http: HttpClient) {}

  /** Returns a list of all Organizations
   * @returns {Observable<Organization[]>}
   */
  list(): void {
    this.http
      .get<Organization[]>('/api/organizations')
      .subscribe((organizations) => this.organizations.set(organizations));
  }

  /** Creates an organization
   * @param newOrganization: Organization object that you want to add to the database
   * @returns {Observable<Organization>}
   */
  createOrganization(newOrganization: Organization): Observable<Organization> {
    return this.http
      .post<Organization>('/api/organizations', newOrganization)
      .pipe(
        tap((organization) => this.organizations.pushOrganization(organization))
      );
  }

  /** Deletes an organization
   * @param organization_id: id of the organization object to delete
   * @returns {Observable<Organization>}
   */
  deleteOrganization(
    organizationToRemove: Organization
  ): Observable<Organization> {
    return this.http
      .delete<Organization>(`/api/organizations/${organizationToRemove.slug}`)
      .pipe(
        tap((_) => {
          this.organizations.removeOrganization(organizationToRemove);
        })
      );
  }
}
