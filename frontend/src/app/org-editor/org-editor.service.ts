/** Abstracts HTTP request functionality for organizations away from the backend database */

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { OrganizationSummary } from '../models.module';

@Injectable({
  providedIn: 'root'
})

export class OrgEditorService {

  constructor(private http: HttpClient) { }

  /** Returns the organization object from the backend database table using the backend HTTP get request. 
   * @param id: Number representing the organization id
   * @returns {Observable<OrganizationSummary>}
   */
  getOrganization = (id: Number) => {
    return this.http.get<OrganizationSummary>("/api/organizations/" + id);
  }

  /** Returns the updated organization object from the backend database table using the backend HTTP put request. 
   * @param org: OrganizationSummary representing the updated organization
   * @returns {Observable<OrganizationSummary>}
   */
  updateOrganization = (org: OrganizationSummary) => {
    if (org.id) {
      return this.http.put<OrganizationSummary>("/api/organizations", org);
    } else {
      return this.http.post<OrganizationSummary>("/api/organizations", org);
    }
    
  }
}
