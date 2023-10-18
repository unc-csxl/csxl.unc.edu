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
import { Organization } from '../organization/organization.service';

/** Interface for Event Type (used on frontend for event detail) */
export interface Event {
    id: number | null;
    name: string;
    time: Date;
    location: string;
    description: string;
    public: boolean;
    organization_id: number;
    organization: Organization;
}

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