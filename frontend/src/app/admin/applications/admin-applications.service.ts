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
import { Observable } from 'rxjs';
import { Application } from './admin-application.model';
import { RxApplication } from './rx-applications';

@Injectable({ providedIn: 'root' })
export class AdminApplicationsService {
  private applications: RxApplication = new RxApplication();
  public applications$: Observable<Application[]> = this.applications.value$;

  constructor(protected http: HttpClient) {}

  /** Returns a list of all Applications
   * @returns {Observable<Application[]>}
   */
  list(): void {
    this.http
      .get<Application[]>('/api/applications')
      .subscribe((applications) => this.applications.set(applications));
  }

  // /** Creates an organization
  //  * @param newOrganization: Organization object that you want to add to the database
  //  * @returns {Observable<Organization>}
  //  */
  // createOrganization(newOrganization: Organization): Observable<Organization> {
  //   return this.http
  //     .post<Organization>('/api/organizations', newOrganization)
  //     .pipe(
  //       tap((organization) => this.organizations.pushOrganization(organization))
  //     );
  // }

  // /** Deletes an organization
  //  * @param organization_id: id of the organization object to delete
  //  * @returns {Observable<Organization>}
  //  */
  // deleteOrganization(
  //   organizationToRemove: Organization
  // ): Observable<Organization> {
  //   return this.http
  //     .delete<Organization>(`/api/organizations/${organizationToRemove.slug}`)
  //     .pipe(
  //       tap((_) => {
  //         this.organizations.removeOrganization(organizationToRemove);
  //       })
  //     );
  // }
}
