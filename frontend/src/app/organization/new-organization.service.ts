/**
 * The Organization Service abstracts HTTP requests to the backend
 * from the components.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { Injectable, Signal, WritableSignal, signal } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';

import { HttpClient } from '@angular/common/http';
import { AuthenticationService } from '../authentication.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable, tap } from 'rxjs';
import { Organization } from './organization.model';
import { Role } from '../role';

@Injectable({
  providedIn: 'root'
})
export class NewOrganizationsService {
  /** Organizations signal */
  private organizationsSignal: WritableSignal<Organization[]> = signal([]);
  organizations = this.organizationsSignal.asReadonly();

  /** Constructor */
  constructor(
    protected http: HttpClient,
    protected auth: AuthenticationService,
    protected snackBar: MatSnackBar
  ) {
    this.getOrganizations();
  }

  /** Refreshes the organization data emitted by the .organizations signal. */
  getOrganizations() {
    this.http
      .get<Organization[]>('/api/organizations')
      .subscribe((organizations) => {
        this.organizationsSignal.set(organizations);
      });
  }

  /** Returns the organization object from the backend database table using the backend HTTP get request.
   * @param slug: String representing the organization slug
   * @returns {Signal<Organization | undefined>}
   */
  getOrganization(slug: string): Signal<Organization | undefined> {
    return toSignal(this.http.get<Organization>('/api/organizations/' + slug));
  }

  /** Returns the new organization object from the backend database table using the backend HTTP post request
   *  and updates the organizations signal to include the new organization.
   * @param organization: Organization to add
   * @returns {Signal<Organization | undefined>}
   */
  createOrganization(
    organization: Organization
  ): Signal<Organization | undefined> {
    return toSignal(
      this.http
        .post<Organization>('/api/organizations', organization)
        .pipe(
          tap((organization) =>
            this.organizationsSignal.update((organizations) => [
              ...organizations,
              organization
            ])
          )
        )
    );
  }

  /** Returns the updated organization object from the backend database table using the backend HTTP put request
   *  and update the organizations signal to include the updated organization.
   * @param organization: Represents the updated organization
   * @returns {Signal<Organization | undefined>}
   */
  updateOrganization(
    organization: Organization
  ): Signal<Organization | undefined> {
    return toSignal(
      this.http
        .put<Organization>('/api/organizations', organization)
        .pipe(
          tap((updatedOrganization) =>
            this.organizationsSignal.update((organizations) => [
              ...organizations.filter((o) => o.id != updatedOrganization.id),
              updatedOrganization
            ])
          )
        )
    );
  }

  /** Returns the deleted organization object from the backend database table using the backend HTTP put request
   *  and updates the organizations signal to exclude the deleted organization.
   * @param organization: Represents the deleted organization
   * @returns {Signal<Organization | undefined>}
   */
  deleteOrganization(
    organization: Organization
  ): Signal<Organization | undefined> {
    return toSignal(
      this.http
        .delete<Organization>(`/api/organizations/${organization.slug}`)
        .pipe(
          tap((deletedOrganization) => {
            this.organizationsSignal.update((organizations) =>
              organizations.filter((o) => o.id != deletedOrganization.id)
            );
          })
        )
    );
  }

  /** Returns the new role object from the backend database table using the backend HTTP post request.
   * @param role: Role representing the new role
   * @returns {Observable<Role>}
   */
  createRole(role: Role): Observable<Role> {
    return this.http.post<Role>('/api/admin/roles', role);
  }
}
