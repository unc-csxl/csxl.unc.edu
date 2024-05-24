import {
  Injectable,
  Signal,
  WritableSignal,
  computed,
  signal
} from '@angular/core';
import {
  DEFAULT_TIME_RANGE_PARAMS,
  Paginated,
  PaginationParams,
  Paginator,
  TimeRangePaginationParams,
  TimeRangePaginator
} from '../pagination';
import {
  Event,
  EventJson,
  EventRegistration,
  parseEventJson
} from './event.model';
import { Observable, map, tap } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { Profile } from '../models.module';
import { GroupEventsPipe } from './pipes/group-events.pipe';
import { DatePipe } from '@angular/common';

@Injectable({
  providedIn: 'root'
})
export class NewEventService {
  /** Encapsulated paginators */
  private eventsPaginator: TimeRangePaginator<Event> =
    new TimeRangePaginator<Event>('/api/events/paginate');

  /** Constructor */
  constructor(protected http: HttpClient) {}

  // Methods for event data.

  /**
   * Retrieves a page of events based on pagination parameters.
   * @param params: Pagination parameters.
   * @returns {Observable<Paginated<Event, TimeRangePaginationParams>>}
   */
  getEvents(params: TimeRangePaginationParams = DEFAULT_TIME_RANGE_PARAMS) {
    return this.eventsPaginator.loadPage(params, parseEventJson);
  }

  /**
   * Gets an event based on its id.
   * @param id: ID for the event.
   * @returns {Observable<Event | undefined>}
   */
  getEvent(id: number): Observable<Event | undefined> {
    return this.http
      .get<EventJson>('/api/events/' + id)
      .pipe(map((eventJson) => parseEventJson(eventJson)));
  }

  /**
   * Returns the new event from the backend database table using the HTTP post request
   * and refreshes the current paginated events page.
   * @param event Event to add
   * @returns {Observable<Event>}
   */
  createEvent(event: Event): Observable<Event> {
    return this.http.post<Event>('/api/events', event);
  }

  /**
   * Returns the updated event from the backend database table using the HTTP put request
   * and refreshes the current paginated events page.
   * @param event Event to update
   * @returns {Observable<Event>}
   */
  updateEvent(event: Event): Observable<Event> {
    return this.http.put<Event>('/api/events', event);
  }

  /**
   * Returns the deleted event from the backend database table using the HTTP delete request
   * and refreshes the current paginated events page.
   * @param event Event to delete
   * @returns {Observable<Event>}
   */
  deleteEvent(event: Event): Observable<Event> {
    return this.http.delete<Event>('/api/events/' + event.id);
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
    event: Event,
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
  registerForEvent(event: Event): Observable<EventRegistration> {
    return this.http.post<EventRegistration>(
      `/api/events/${event.id}/registration`,
      {}
    );
  }

  /**
   * Unregisters the current user from an event.
   * @param event: Event to unregister from.
   * @returns {Observable<EventRegistration>}
   */
  unregisterForEvent(event: Event): Observable<EventRegistration> {
    return this.http.delete<EventRegistration>(
      `/api/events/${event.id}/registration`
    );
  }
}
