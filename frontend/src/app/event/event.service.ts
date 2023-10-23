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
import { Observable } from 'rxjs';
import { Event } from './event.model';
import { DatePipe } from '@angular/common';
import { EventFilterPipe } from './event-filter/event-filter.pipe';

@Injectable({
  providedIn: 'root'
})
export class EventService {

  constructor(protected http: HttpClient, public datePipe: DatePipe, public eventFilterPipe: EventFilterPipe) { }

  /** Returns all event entries from the backend database table using the backend HTTP get request. 
   * @returns {Observable<Event[]>}
   */
  getEvents(): Observable<Event[]> {
    return this.http.get<Event[]>("/api/events");
  }

  /** Returns the event object from the backend database table using the backend HTTP get request. 
   * @param id: ID of the event to retrieve
   * @returns {Observable<Event>}
   */
  getEvent(id: number): Observable<Event> {
    return this.http.get<Event>("/api/events/" + id);
  }

  /** Returns the event object from the backend database table using the backend HTTP get request. 
  * @param id: ID of the organization to retrieve
  * @returns {Observable<Event[]>}
  */
  getEventsByOrganization(id: number): Observable<Event[]> {
    return this.http.get<Event[]>("/api/events/organization/" + id);
  }

  /** Returns the new event object from the backend database table using the backend HTTP get request. 
   * @param event: model of the event to be created
   * @returns {Observable<Event>}
   */
  createEvent(event: Event): Observable<Event> {
    return this.http.post<Event>("/api/events", event);
  }

  /** Returns the updated event object from the backend database table using the backend HTTP put request. 
   * @param event: Event representing the updated event
   * @returns {Observable<Event>}
   */
  updateEvent(event: Event): Observable<Event> {
    return this.http.put<Event>("/api/events", event);
  }

  /** Delete the given event object using the backend HTTP delete request. W
   * @param event: Event representing the updated event
   * @returns void
   */
  deleteEvent(event: Event): Observable<Event> {
    return this.http.delete<Event>("/api/events/" + event.id);
  }

  /** Helper function to group a list of events by date,
 * filtered based on the input query string.
 * @param events: List of the input events
 * @param query: Search bar query to filter the items
 */
  groupEventsByDate(events: Event[], query: string = ""): [string, Event[]][] {
    // Initialize an empty map
    let groups: Map<string, Event[]> = new Map();

    // Transform the list of events based on the event filter pipe and query
    this.eventFilterPipe.transform(events, query)
      .forEach((event) => {
        // Find the date to group by
        let dateString = this.datePipe.transform(event.time, 'EEEE, MMMM d, y') ?? ""
        // Add the event
        let newEventsList = groups.get(dateString) ?? []
        newEventsList.push(event)
        groups.set(dateString, newEventsList)
      })

    // Return the groups
    return [...groups.entries()]
  }
}