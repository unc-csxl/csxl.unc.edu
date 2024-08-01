/**
 * The Event Service abstracts HTTP requests to the backend
 * from the components.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2024
 * @license MIT
 */

import { Injectable } from '@angular/core';
import {
  DEFAULT_TIME_RANGE_PARAMS,
  Paginated,
  PaginationParams,
  Paginator,
  TimeRangePaginationParams,
  TimeRangePaginator
} from '../pagination';
import {
  EventOverview,
  EventRegistration,
  EventStatusOverview,
  EventStatusOverviewJson,
  parseEventOverviewJson,
  parseEventStatusOverviewJson,
  EventDraft,
  EventOverviewJson
} from './event.model';
import { Observable, map } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { Profile } from '../models.module';

@Injectable({
  providedIn: 'root'
})
export class EventService {
  /** Encapsulated paginators */
  private eventsPaginator: TimeRangePaginator<EventOverview> =
    new TimeRangePaginator<EventOverview>('/api/events/paginate');
  private unauthenticatedEventsPaginator: TimeRangePaginator<EventOverview> =
    new TimeRangePaginator<EventOverview>(
      '/api/events/unauthenticated/paginate'
    );

  /** Constructor */
  constructor(protected http: HttpClient) {}

  // Methods for event data.

  /**
   * Retrieves a page of events based on pagination parameters.
   * @param params: Pagination parameters.
   * @returns {Observable<Paginated<EventOverview, TimeRangePaginationParams>>}
   */
  getEvents(
    params: TimeRangePaginationParams = DEFAULT_TIME_RANGE_PARAMS,
    authenticated: boolean
  ) {
    if (authenticated) {
      return this.eventsPaginator.loadPage(params, parseEventOverviewJson);
    } else {
      return this.unauthenticatedEventsPaginator.loadPage(
        params,
        parseEventOverviewJson
      );
    }
  }

  /**
   * Gets an event based on its id.
   * @param id: ID for the event.
   * @returns {Observable<Event | undefined>}
   */
  getEvent(id: number): Observable<EventOverview | undefined> {
    return this.http
      .get<EventOverviewJson>('/api/events/' + id)
      .pipe(map((eventJson) => parseEventOverviewJson(eventJson)));
  }

  /**
   * Returns the new event from the backend database table using the HTTP post request
   * and refreshes the current paginated events page.
   * @param event Event to add
   * @returns {Observable<EventOverview>}
   */
  createEvent(event: EventDraft): Observable<EventOverview> {
    return this.http.post<EventOverview>('/api/events', event);
  }

  /**
   * Returns the updated event from the backend database table using the HTTP put request
   * and refreshes the current paginated events page.
   * @param event Event to update
   * @returns {Observable<EventOverview>}
   */
  updateEvent(event: EventDraft): Observable<EventOverview> {
    return this.http.put<EventOverview>('/api/events', event);
  }

  /**
   * Returns the deleted event from the backend database table using the HTTP delete request
   * and refreshes the current paginated events page.
   * @param event Event to delete
   * @returns {Observable<EventOverview>}
   */
  deleteEvent(eventId: number): Observable<EventOverview> {
    return this.http.delete<EventOverview>('/api/events/' + eventId);
  }

  // Methods for event registration data.

  // TODO: Refactor to remove, load event registrations instead.

  /**
   * Loads a paginated list of registered users for a given event.
   * @param event: Event to load registrations for.
   * @param params: Pagination parameters.
   * @returns {Observable<Paginated<Profile, PaginationParams>>}
   */
  getRegisteredUsersForEvent(
    event: EventOverview,
    params: PaginationParams
  ): Observable<Paginated<Profile, PaginationParams>> {
    const paginator: Paginator<Profile> = new Paginator<Profile>(
      `/api/events/${event.id}/registrations/users`
    );
    return paginator.loadPage(params);
  }

  /**
   * Registers the current user to an event.
   * @param event: Event to register to.
   * @returns {Observable<EventRegistration>}
   */
  registerForEvent(eventId: number): Observable<EventRegistration> {
    return this.http.post<EventRegistration>(
      `/api/events/${eventId}/registration`,
      {}
    );
  }

  /**
   * Unregisters the current user from an event.
   * @param event: Event to unregister from.
   * @returns {Observable<EventRegistration>}
   */
  unregisterForEvent(eventId: number): Observable<EventRegistration> {
    return this.http.delete<EventRegistration>(
      `/api/events/${eventId}/registration`
    );
  }

  /**
   * Returns the event status, which includes featured events and registrations.
   * @returns {Observable<EventStatusOverview>}
   */
  getEventStatus(authenticated: boolean): Observable<EventStatusOverview> {
    return this.http
      .get<EventStatusOverviewJson>(
        `/api/events/${!authenticated ? 'unauthenticated/' : ''}status`
      )
      .pipe(map(parseEventStatusOverviewJson));
  }
}
