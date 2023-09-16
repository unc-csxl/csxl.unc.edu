/** Abstracts HTTP request functionality for organizations away from the backend database */

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AuthenticationService } from '../authentication.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable, mergeMap, of, shareReplay } from 'rxjs';
import { Profile } from '../profile/profile.service';


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

  /** Store profile observable*/
  public profile$: Observable<Profile | undefined>;

  constructor(protected http: HttpClient, protected auth: AuthenticationService, protected snackBar: MatSnackBar) {
    /** If profile is authenticated, display profile page. */
    this.profile$ = this.auth.isAuthenticated$.pipe(
      mergeMap(isAuthenticated => {
        if (isAuthenticated) {
          return this.http.get<Profile>('/api/profile');
        } else {
          return of(undefined);
        }
      }),
      shareReplay(1)
    );
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
