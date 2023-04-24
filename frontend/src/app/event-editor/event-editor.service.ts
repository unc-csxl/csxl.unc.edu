/** Abstracts HTTP request functionality for events away from the backend database */

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { EventSummary } from '../models.module';

@Injectable({
  providedIn: 'root'
})

export class EventEditorService {

  constructor(private http: HttpClient) { }

  /** Returns the event object from the backend database table using the backend HTTP get request. 
   * @param id: Number representing the event id
   * @returns {Observable<EventSummary>}
  */
  getEvent(id: Number): Observable<EventSummary> {
    return this.http.get<EventSummary>("/api/events/" + id);
  }

  /** Returns the updated event object from the backend database table using the backend HTTP put request. 
   * @param event: EventSummary representing the updated event
   * @returns {Observable<EventSummary>}
  */

  updateEvent(event: EventSummary): Observable<EventSummary> {
    return this.http.put<EventSummary>("/api/events", event);
  }
}
