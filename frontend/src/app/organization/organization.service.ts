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

/** Interface for Organization Type (used on frontend for organization detail) */
export interface Organization {
    id: number | null;
    name: string;
    logo: string;
    short_description: string;
    long_description: string;
    website: string;
    email: string;
    instagram: string;
    linked_in: string;
    youtube: string;
    heel_life: string;
    public: boolean;
    slug: string;
}

@Injectable({
    providedIn: 'root'
})
export class OrganizationService {
  constructor(protected http: HttpClient, 
              protected auth: AuthenticationService, 
              protected snackBar: MatSnackBar) {
  }

  /** Returns all organization entries from the backend database table using the backend HTTP get request. 
   * @returns {Observable<Organization[]>}
   */
  getOrganizations(): Observable<Organization[]> {
    return this.http.get<Organization[]>("/api/organizations");
  }

  /** Returns the organization object from the backend database table using the backend HTTP get request. 
   * @param slug: String representing the organization slug
   * @returns {Observable<Organization>}
   */
  getOrganization(slug: string): Observable<Organization> {
    return this.http.get<Organization>("/api/organizations/" + slug);
  }

  /** Returns the new organization object from the backend database table using the backend HTTP post request. 
   * @param org: OrganizationSummary representing the updated organization
   * @returns {Observable<Organization>}
   */
    createOrganization(organization: Organization): Observable<Organization> {
      return this.http.post<Organization>("/api/organizations", organization);
    }

}
