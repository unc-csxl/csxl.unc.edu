/** Abstracts HTTP request functionality away from the backend database */

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { mergeMap, Observable, shareReplay, of, subscribeOn } from 'rxjs';
import { Profile, RegistrationSummary, EventSummary } from '../models.module';
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

  /** Returns all event entries from the backend database table using the backend HTTP get request. 
   * @returns {Observable<EventSummary[]>}
  */
  getEvents(): Observable<EventSummary[]> {
    return this.http.get<EventSummary[]>("/api/events");
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

        // Get the registrations from user id and status
        this.http.get<RegistrationSummary[]>("/api/registrations/user/" + user_id + "/0").subscribe((registrations) => {
          // Store boolean for whether a user is already registered or not
          var registered: boolean = false;
          
          // For each registration in the list of registrations
          for (let reg of registrations) {
            // If the registration's event ID matches the desired event ID
            if (reg.event_id == id) {
              // Change user registration boolean to true
              registered = true;
              break;
            }
          }

          if(!registered) {
            this.http.post<RegistrationSummary>("/api/registrations", registration).subscribe((res) => console.log("succesfully registered!"));
          }
        });
      }); 
    }
  }
}