/** Abstracts HTTP request functionality for profiles away from the backend database */

/** Abstracts HTTP request functionality for profiles away from the backend database */

import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { mergeMap, Observable, of, shareReplay } from 'rxjs';
import { AuthenticationService } from '../authentication.service';
import { Event, OrganizationSummary, OrgRole, Profile, Registration } from '../models.module';

@Injectable({
  providedIn: 'root'
})
export class ProfileService {

  /** Store profile */
  public profile$!: Observable<Profile | undefined>;

  constructor(protected http: HttpClient, protected auth: AuthenticationService) {
    this.refreshProfile();
  }

  private refreshProfile() {
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

  /** Updates the profile and returns the updated version of the profile.
   * @returns {Observable<Profile>}
   */
  put = (profile: Profile) => {
    return this.http.put<Profile>("/api/profile", profile);
  }

  /** Gets and returns a profile.
   * @returns {Observable<Profile>}
   */
  search = (query: string) => {
    let encodedQuery = encodeURIComponent(query);
    return this.http.get<Profile[]>(`/api/user?q=${encodedQuery}`);
  }

  /** Returns all organization entries for the current user from the backend database table 
   * using the backend HTTP get request. 
   * @returns {OrganizationSummary[]}
   */
  getUserOrganizations = () => {
    var organizations: OrganizationSummary[] = [];
    if (this.profile$) {
      this.profile$.subscribe(profile => organizations = profile!.organizations);
    }
    return organizations;
  }

  /** Returns all event entries for the current user from the backend database table 
   * using the backend HTTP get request. 
   * @returns {Event[]}
   */
  getUserEvents = () => {
    var events: Event[] = [];
    if (this.profile$) {
      this.profile$.subscribe(profile => events = profile!.events)
    }
    return events;
  }

  /** Delete a registration from the backend
   * @param event_id: number representing the event registration to be deleted for the user
   * @returns {void}
   */
  deleteRegistration = (event_id: number) => {
    // Store the list of registrations from the profile.
    var registrations: Registration[] = [];
    // Store the current user's ID.
    var user_id: number | null = null;

    // If a user is currently logged in, get their registrations and delete the appropriate registration.
    if (this.profile$) {
      // Get the registrations (event associations) from the profile Observable.
      this.profile$.subscribe(profile => registrations = profile!.event_associations);
      // Get the user_id from the profile Observable.
      this.profile$.subscribe(profile => user_id = profile!.id);

      // For each registration in the list of registrations
      for (let reg of registrations) {
        // If the registration's event and user IDs match the desired event and user IDs
        if (reg.event_id == event_id && reg.user_id == user_id) {
          // Make the call to delete the registration.
          this.http.delete<void>(`/api/registrations/registration/${reg.id}`).subscribe(() => console.log('Delete successful.'));
          break;
        }
      }
    }
  }

  /** Delete an org role from the backend
   * @param org_id: number representing the org role to be deleted for the user
   * @returns {void}
   */
  deleteOrgMembership = (org_id: number) => {
    // Store the list of registrations from the profile.
    var org_roles: OrgRole[] = [];
    // Store the current user's ID.
    var user_id: number | null = null;

    // If a user is currently logged in, get their organizations and delete the appropriate organization.
    if (this.profile$) {
      // Get the organizations (ogranization associations) from the profile Observable.
      this.profile$.subscribe(profile => org_roles = profile!.organization_associations);
      // Get the user_id from the profile Observable.
      this.profile$.subscribe(profile => user_id = profile!.id);

      // For each organization in the list of organizations
      for (let org of org_roles) {
        // If the organization's event and user IDs match the desired org and user IDs
        if (org.org_id == org_id && org.user_id == user_id) {
          // Make the call to delete the organization
          this.http.delete<void>(`/api/orgroles/${org.id}`).subscribe(() => console.log('Delete successful.'));
          break;
        }
      }
    }
  }

  getGitHubOAuthLoginURL(): Observable<string> {
    return this.http.get<string>("/oauth/github_oauth_login_url");
  }

  unlinkGitHub() {
    return this.http.delete("/oauth/github");
  }

}