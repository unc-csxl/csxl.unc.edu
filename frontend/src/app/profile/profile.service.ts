/** Abstracts HTTP request functionality for profiles away from the backend database */

import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { mergeMap, Observable, of, shareReplay } from 'rxjs';
import { AuthenticationService } from '../authentication.service';
import { EventSummary, OrganizationSummary, Profile, Registration } from '../models.module';

@Injectable({
  providedIn: 'root'
})
export class ProfileService {

  /** Store profile */
  public profile$: Observable<Profile | undefined>;

  constructor(protected http: HttpClient, protected auth: AuthenticationService) {
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

  /** Updates the profile and returns the updated version of the profile.
  * @returns {Observable<Profile>}
  */
  put(profile: Profile) {
    return this.http.put<Profile>("/api/profile", profile);
  }

  /** Gets and returns a profile.
  * @returns {Observable<Profile>}
  */
  search(query: string) {
    let encodedQuery = encodeURIComponent(query);
    return this.http.get<Profile[]>(`/api/user?q=${encodedQuery}`);
  }

  /** Returns all organization entries for the current user from the backend database table 
   * using the backend HTTP get request. 
   * @returns {OrganizationSummary[]}
  */
  getUserOrganizations(): OrganizationSummary[] {
    var organizations: OrganizationSummary[] = [];
    if (this.profile$) {
      this.profile$.subscribe(profile => organizations = profile!.organizations);
    }
    return organizations;
  }

  /** Returns all organization entries for the current user from the backend database table 
   * using the backend HTTP get request. 
   * @returns {EventSummary[]}
  */
  getUserEvents(): EventSummary[] {
    var events: EventSummary[] = [];
    if (this.profile$) {
      this.profile$.subscribe(profile => events = profile!.events)
    }
    return events;
  }

  /** Delete a registration from the backend
   * @param event_id: Number representing the event registration to be deleted for the user
   * @returns {void}
  */
  deleteRegistration(event_id: Number) {
    // Store the list of registrations from the profile.
    var registrations: Registration[] = [];
    // Store the current user's ID.
    var user_id: Number | null = null;

    // If a user is currently logged in, get their registrations and delete the appropriate registration.
    if (this.profile$) {
      // Get the registrations (event associations) from the profile Observable.
      this.profile$.subscribe(profile => registrations = profile!.event_associations);
      // Get the user_id from the profile Observable.
      this.profile$.subscribe(profile => user_id = profile!.id);

      // For each registration in the list of registrations
      for (let reg of registrations) {
        // If the registration's event and user IDs much the desired event and user IDs
        if (reg.event_id == event_id && reg.user_id == user_id) {
          // Make the call to delete the registration.
          this.http.delete<void>(`/api/registrations/registration/${reg.id}`).subscribe(() => console.log('Delete successful.'));
          break;
        }
      }
    }
  }

}