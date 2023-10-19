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
   * @param id: ID of the organization to retrieve
   * @returns {Observable<Event>}
   */
  getEvent(id: number): Observable<Event> {
    return this.http.get<Event>("/api/events/" + id);
  }
}