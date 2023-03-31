import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

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

  getOrganizations(): Observable<Organization[]> {
    return this.http.get<Organization[]>("/api/organizations");
  }
}
