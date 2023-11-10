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
import { EventFilterPipe } from './event-filter/event-filter.pipe';

@Injectable({
  providedIn: 'root'
})
export class EventService {
  constructor(
    protected http: HttpClient,
    public datePipe: DatePipe,
    public eventFilterPipe: EventFilterPipe
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

  /** Delete the given event object using the backend HTTP delete request.
   * @param event: Event representing the updated event
   * @returns void
   */
  deleteEvent(event: Event): Observable<Event> {
    return this.http.delete<Event>('/api/events/' + event.id);
  }

  /** Add a certain number of days to a date
   * @param date: Date object
   * @param days: Number of days to be added
   * @returns {Date}
   */
  addDays(date: Date, days: number) {
    var result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
  }

  /** Creates an array of all the days between startDate and endDate inclusive
   * @param startDate: Date object representing the start of the range
   * @param endDate: Date object representing the end of the range
   * @returns {Array<Event>}
   */
  getDates(startDate: Date, endDate: Date) {
    var dateArray = new Array();
    var currentDate = startDate;
    while (currentDate <= endDate) {
      dateArray.push(
        this.datePipe.transform(currentDate, 'EEEE, MMMM d, y') ?? ''
      );
      currentDate = this.addDays(currentDate, 1);
    }
    return dateArray;
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
      // Set multi_day flag to true if event spans multiple days
      if (event.time.toDateString() !== event.end_time.toDateString()) {
        event.multi_day = true;
      }
      // Find the date(s) to group by
      let dateStrings;
      if (event.multi_day) {
        dateStrings = this.getDates(event.time, event.end_time);
      } else {
        dateStrings = [
          this.datePipe.transform(event.time, 'EEEE, MMMM d, y') ?? ''
        ];
      }
      // Add the event to the appropriate date groups
      for (let i = 0; i < dateStrings.length; i++) {
        let newEventsList = groups.get(dateStrings[i]) ?? [];
        newEventsList.push(event);
        groups.set(dateStrings[i], newEventsList);
      }
    });

    // Return the groups
    return [...groups.entries()];
  }
}
