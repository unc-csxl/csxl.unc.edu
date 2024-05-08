/**
 * The Showcase Service abstracts HTTP requests to the backend
 * from the components.
 *
 * @author Ajay Gandecha
 * @copyright 2024
 * @license MIT
 */

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ShowcaseProject } from './showcaseproject.model';

@Injectable({
  providedIn: 'root'
})
export class ShowcaseService {
  constructor(protected http: HttpClient) {}

  /** Returns all of the projects using the backend HTTP get request.
   * @returns {Observable<Organization[]>}
   */
  getProjects(): Observable<ShowcaseProject[]> {
    return this.http.get<ShowcaseProject[]>('/api/showcase');
  }
}
