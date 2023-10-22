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

@Injectable({
    providedIn: 'root'
})
export class EventService {
  
  constructor(protected http: HttpClient) {}

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
  updateEvent = (event: Event) => {
    return this.http.put<Event>("/api/events", event);
  }
}