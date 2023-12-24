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
import { Observable, map } from 'rxjs';
import { Event, EventJson, parseEventJson } from './event.model';
import { DatePipe } from '@angular/common';
import { EventPaginationParams, PaginatedEvent } from 'src/app/pagination';

@Injectable({
  providedIn: 'root'
})
export class EventService {
  constructor(
    protected http: HttpClient,
    public datePipe: DatePipe
  ) {}

  /** Returns all event entries from the backend database table using the backend HTTP get request.
   * @returns {Observable<Event[]>}
   */
  getEvents(): Observable<Event[]> {
    return this.http
      .get<EventJson[]>('/api/events')
      .pipe(map((eventJsons) => eventJsons.map(parseEventJson)));
  }

  /** Returns the event object from the backend database table using the backend HTTP get request.
   * @param id: ID of the event to retrieve
   * @returns {Observable<Event>}
   */
  getEvent(id: number): Observable<Event> {
    return this.http
      .get<EventJson>('/api/events/' + id)
      .pipe(map((eventJson) => parseEventJson(eventJson)));
  }

  /** Returns the event object from the backend database table using the backend HTTP get request.
   * @param slug: Slug of the organization to retrieve
   * @returns {Observable<Event[]>}
   */
  getEventsByOrganization(slug: string): Observable<Event[]> {
    return this.http
      .get<EventJson[]>('/api/events/organization/' + slug)
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
    events.forEach((event) => {
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

  list(params: EventPaginationParams) {
    let paramStrings = {
      order_by: params.order_by,
      ascending: params.ascending,
      filter: params.filter,
      range_start: params.range_start,
      range_end: params.range_end
    };
    let query = new URLSearchParams(paramStrings);
    return this.http
      .get<PaginatedEvent<EventJson>>(
        '/api/events/paginate?' + query.toString()
      )
      .pipe(
        map((paginated) => ({
          ...paginated,
          items: paginated.items.map(parseEventJson)
        }))
      );
  }
}
