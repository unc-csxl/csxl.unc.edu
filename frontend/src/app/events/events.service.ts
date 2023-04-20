/** Abstracts HTTP request functionality away from the backend database */

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { mergeMap, Observable, shareReplay, of, subscribeOn } from 'rxjs';
import { Profile, RegistrationSummary, Event, Registration } from '../models.module';
import { AuthenticationService } from '../authentication.service';

@Injectable({
  providedIn: 'root'
})

export class EventsService {

  /** Store profile */
  public profile$: Observable<Profile | undefined>;

  constructor(private http: HttpClient, protected auth: AuthenticationService) { 
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

  /** Returns whether or not the user is registered for an event
   * @param eventId: a valid Number representing the ID of the event
   * @returns {boolean}
  */
  checkIsRegistered(eventId: Number): boolean {
    var registrations: Registration[] = [];
    // Store the current user's ID.
    var user_id: Number | null = null;

    // If a user is currently logged in, get their registrations and determine if the registration is valid
    if (this.profile$) {
      // Get the registrations (event associations) from the profile Observable.
      this.profile$.subscribe(profile => registrations = profile!.event_associations);
      // Get the user_id from the profile Observable.
      this.profile$.subscribe(profile => user_id = profile!.id);

      // For each registration in the list of registrations
      for (let reg of registrations) {
        // If the registration's event and user IDs match the desired event and user IDs
        if (reg.event_id == eventId && reg.user_id == user_id && reg.status == 0) {
          // Make the call to delete the registration.
          return true;
        }
      }
    }
    return false;
  }


  /** Returns all event entries from the backend database table using the backend HTTP get request. 
   * @returns {Observable<Event[]>}
  */
  getEvents(): Observable<Event[]> {
    return this.http.get<Event[]>("/api/events");
  }

  /** Create a registration from the backend
   * @param event_id: Number representing the event id
   * @returns {void}
  */
  async register(id: Number) {
    // Store the current user's ID.
    var user_id: Number = -1;
    
    // If a user is currently logged in, register them for the appropriate event.
    if (this.profile$) {
      // Get the correct user id
      this.profile$.subscribe(profile => {
        user_id = profile!.id!;
        // Create Registration
        const registration: RegistrationSummary = {
          id: null,
          user_id: user_id,
          event_id: id,
          status: 0
        };

        if (!this.checkIsRegistered(registration.event_id)) {
          this.http.post<RegistrationSummary>("/api/registrations", registration).subscribe((res) => console.log("succesfully registered!"));
        }
      }); 
    }
  }
}