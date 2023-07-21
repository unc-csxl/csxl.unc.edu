/** Abstracts HTTP request functionality for organizations away from the backend database */

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { OrganizationSummary } from '../models.module';

@Injectable({
  providedIn: 'root'
})

export class OrganizationsService {

  constructor(private http: HttpClient) { }

  /** Returns all organization entries from the backend database table using the backend HTTP get request. 
   * @returns {Observable<OrganizationSummary[]>}
   */
  getOrganizations = () => {
    return this.http.get<OrganizationSummary[]>("/api/organizations");
  }
}
