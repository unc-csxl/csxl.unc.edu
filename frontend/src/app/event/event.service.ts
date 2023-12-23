/**
 * The Event Service abstracts HTTP requests to the backend
 * from the components.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, Subscription, map, tap } from 'rxjs';
import {
  Event,
  EventJson,
  EventRegistration,
  parseEventJson
} from './event.model';
import { DatePipe } from '@angular/common';
import { EventFilterPipe } from './event-filter/event-filter.pipe';
import { Profile, ProfileService } from '../profile/profile.service';

@Injectable({
  providedIn: 'root'
})
export class EventService {
  private profile: Profile | undefined;
  private profileSubscription!: Subscription;

  constructor(
    protected http: HttpClient,
    protected profileSvc: ProfileService,
    public datePipe: DatePipe,
    public eventFilterPipe: EventFilterPipe
  ) {
    this.profileSubscription = this.profileSvc.profile$.subscribe(
      (profile) => (this.profile = profile)
    );
  }

  /** Returns all event entries from the backend database table using the backend HTTP get request.
   * @returns {Observable<Event[]>}
   */
  getEvents(): Observable<Event[]> {
    return this.http
      .get<EventJson[]>('/api/events/registration/status')
      .pipe(map((eventJsons) => eventJsons.map(parseEventJson)));
  }

  /** Returns the event object from the backend database table using the backend HTTP get request.
   * @param id: ID of the event to retrieve
   * @returns {Observable<Event>}
   */
  getEvent(id: number): Observable<Event> {
    return this.http
      .get<EventJson>('/api/events/' + id + '/registration/status')
      .pipe(map((eventJson) => parseEventJson(eventJson)));
  }

  /** Returns the event object from the backend database table using the backend HTTP get request.
   * @param slug: Slug of the organization to retrieve
   * @returns {Observable<Event[]>}
   */
  getEventsByOrganization(slug: string): Observable<Event[]> {
    return this.http
      .get<EventJson[]>(
        '/api/events/organization/' + slug + '/registration/status'
      )
      .pipe(map((eventJsons) => eventJsons.map(parseEventJson)));
  }

  /** Returns the new event object from the backend database table using the backend HTTP get request.
   * @param event: model of the event to be created
   * @returns {Observable<Event>}
   */
  createEvent(event: Event): Observable<Event> {
    return this.http.post<Event>('/api/events', event);
  }

  /** Returns the updated event object from the backend database table using the backend HTTP put request.
   * @param event: Event representing the updated event
   * @returns {Observable<Event>}
   */
  updateEvent(event: Event): Observable<Event> {
    return this.http.put<Event>('/api/events', event);
  }

  /** Delete the given event object using the backend HTTP delete request. W
   * @param event: Event representing the updated event
   * @returns void
   */
  deleteEvent(event: Event): Observable<Event> {
    return this.http.delete<Event>('/api/events/' + event.id);
  }

  /** Helper function to group a list of events by date,
   * filtered based on the input query string.
   * @param events: List of the input events
   * @param query: Search bar query to filter the items
   */
  groupEventsByDate(events: Event[], query: string = ''): [string, Event[]][] {
    // Initialize an empty map
    let groups: Map<string, Event[]> = new Map();

    // Transform the list of events based on the event filter pipe and query
    this.eventFilterPipe.transform(events, query).forEach((event) => {
      // Find the date to group by
      let dateString =
        this.datePipe.transform(event.time, 'EEEE, MMMM d, y') ?? '';
      // Add the event
      let newEventsList = groups.get(dateString) ?? [];
      newEventsList.push(event);
      groups.set(dateString, newEventsList);
    });

    // Return the groups
    return [...groups.entries()];
  }

  // Event Registration Methods
  /** Return an event registration if the user is registered for an event using the backend HTTP get request.
   * @param event_id: number representing the Event ID
   * @returns Observable<EventRegistration>
   */
  getEventRegistrationOfUser(event_id: number): Observable<EventRegistration> {
    return this.http.get<EventRegistration>(
      `/api/events/${event_id}/registration`
    );
  }

  /** Return all event registrations an event using the backend HTTP get request.
   * @param event_id: number representing the Event ID
   * @returns Observable<EventRegistration[]>
   */
  getEventRegistrations(event_id: number): Observable<EventRegistration[]> {
    return this.http.get<EventRegistration[]>(
      `/api/events/${event_id}/registrations`
    );
  }

  /** Return number of event registrations for an event
   * @param event_id: number representing the Event ID
   * @returns Observable<number>
   */
  getEventRegistrationCount(event_id: number): Observable<number> {
    return this.http.get<number>(`/api/events/${event_id}/registration/count`);
  }

  /** Create a new registration for an event using the backend HTTP create request.
   * @param event_id: number representing the Event ID
   * @returns Observable<EventRegistration>
   */
  registerForEvent(event_id: number): Observable<EventRegistration> {
    if (this.profile === undefined) {
      throw new Error('Only allowed for logged in users.');
    }

    return this.http.post<EventRegistration>(
      `/api/events/${event_id}/registration`,
      {}
    );
  }

  /** Delete an existing registration for an event using the backend HTTP delete request.
   * @param event_registration_id: number representing the Event Registration ID
   * @returns void
   */
  unregisterForEvent(event_id: number) {
    if (this.profile === undefined) {
      throw new Error('Only allowed for logged in users.');
    }

    return this.http.delete<EventRegistration>(
      `/api/events/${event_id}/registration`
    );
  }
}
