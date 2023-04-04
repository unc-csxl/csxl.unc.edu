/** Abstracts HTTP request functionality away from the backend database */

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

/** Interface for Organization Type */
export interface Organization {
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

export class OrganizationsService {

  constructor(private http: HttpClient) { }

  /** Returns all organization entries from the backend database table using the backend HTTP get request. 
   * @returns {Observable<Organization[]>}
  */
  getOrganizations(): Observable<Organization[]> {
    return this.http.get<Organization[]>("/api/organizations");
  }
}
