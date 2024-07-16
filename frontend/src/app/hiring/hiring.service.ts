/**
 * The Hiring Service abstracts HTTP requests to the backend
 * from the components.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HiringStatus } from './hiring.models';

@Injectable({
  providedIn: 'root'
})
export class HiringService {
  /** Constructor */
  constructor(protected http: HttpClient) {}

  /**
   * Retrieves the hiring status for a course site.
   * @param courseSiteId: ID of the course site to get the hiring status for.
   * @returns the hiring status.
   */
  getStatus(courseSiteId: number): Observable<HiringStatus> {
    return this.http.get<HiringStatus>(`/api/hiring/${courseSiteId}`);
  }

  /**
   * Updates the hiring status for a course site.
   * @param courseSiteId: ID of the course site to update the hiring status for.
   * @param status: New status.
   * @returns the new hiring status.
   */
  updateStatus(
    courseSiteId: number,
    status: HiringStatus
  ): Observable<HiringStatus> {
    return this.http.put<HiringStatus>(`/api/hiring/${courseSiteId}`, status);
  }
}
