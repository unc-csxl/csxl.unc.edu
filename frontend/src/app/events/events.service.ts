import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Event {
    id: Number
    name: String
    time: Date
    location: String
    description: String
    public: Boolean
    org_id: Number
    organization: Organization
}

interface Organization {
    id: Number
    name: String
    logo: String
    short_description: String
    long_description: String
    website: String
    email: String
    instagram: String
    linked_in: String
    youtube: String
    heel_life: String
  }

@Injectable({
  providedIn: 'root'
})

export class EventsService {

  constructor(private http: HttpClient) { }

  getEvents(): Observable<Event[]> {
    return this.http.get<Event[]>("/api/events");
  }
}
