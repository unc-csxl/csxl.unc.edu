/** Abstracts HTTP request functionality away from the backend database */

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { mergeMap, Observable, shareReplay, of, subscribeOn } from 'rxjs';
import { Profile, RegistrationSummary, Event, Registration, EventSummary } from '../models.module';
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
  checkIsRegistered = (eventId: number) => {
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
  getEvents = () => {
    return this.http.get<Event[]>("/api/events");
  }

  /** Create a registration from the backend
   * @param id: Number representing the event id
   * @returns {Observer<RegistrationSummary>}
  */
  register = (id: number, userId: number) => {

    const registration: RegistrationSummary = {
      id: null,
      user_id: userId,
      event_id: id,
      status: 0
    };

    return this.http.post<RegistrationSummary>("/api/registrations", registration);
  }

  unregister = (id: number) => {
    return this.http.delete<void>(`/api/registrations/registration/${id}`);
  }

  /** Returns the event object from the backend database table using the backend HTTP get request. 
 * @param id: Number representing the event id
 * @returns {Observable<EventSummary>}
 */
  getEvent = (id: Number) => {
    return this.http.get<EventSummary>("/api/events/" + id);
  }

  /** Returns the updated event object from the backend database table using the backend HTTP put request. 
   * @param event: EventSummary representing the updated event
   * @returns {Observable<EventSummary>}
   */
  updateEvent = (event: EventSummary) => {
    return this.http.put<EventSummary>("/api/events", event);
  }
}