/**
 * The Hiring Service abstracts HTTP requests to the backend
 * from the components.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { HttpClient } from '@angular/common/http';
import { computed, Injectable, signal, WritableSignal } from '@angular/core';
import { Observable, tap } from 'rxjs';
import {
  HiringAdminOverview,
  HiringAssignmentDraft,
  HiringAssignmentOverview,
  HiringLevel,
  HiringStatus
} from './hiring.models';

@Injectable({
  providedIn: 'root'
})
export class HiringService {
  /** Constructor */
  constructor(protected http: HttpClient) {
    this.getHiringLevels();
  }

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

  /**
   * Returns the state of hiring to the admin.
   * @param termId: ID for the term to get the hiring data for.
   * @returns { Observable<HiringAdminOverview> }
   */
  getHiringAdminOverview(termId: string): Observable<HiringAdminOverview> {
    return this.http.get<HiringAdminOverview>(`/api/hiring/admin/${termId}`);
  }

  private hiringLevelsSignal: WritableSignal<HiringLevel[]> = signal([]);
  hiringLevels = this.hiringLevelsSignal.asReadonly();
  activeHiringlevels = computed(() => {
    return this.hiringLevels().filter((h) => h.is_active);
  });
  getHiringLevels() {
    this.http.get<HiringLevel[]>(`/api/hiring/level`).subscribe((levels) => {
      this.hiringLevelsSignal.set(levels);
    });
  }

  getHiringLevel(id: number): HiringLevel | undefined {
    return this.hiringLevels().find((level) => level.id === id);
  }

  createHiringLevel(level: HiringLevel): Observable<HiringLevel> {
    return this.http.post<HiringLevel>(`/api/hiring/level`, level).pipe(
      tap((level) =>
        this.hiringLevelsSignal.update((old) => {
          return [...old, level];
        })
      )
    );
  }

  updateHiringLevel(level: HiringLevel): Observable<HiringLevel> {
    return this.http.put<HiringLevel>(`/api/hiring/level`, level);
  }

  createHiringAssignment(
    assignment: HiringAssignmentDraft
  ): Observable<HiringAssignmentOverview> {
    return this.http.post<HiringAssignmentOverview>(
      `/api/hiring/assignment`,
      assignment
    );
  }

  updateHiringAssignment(
    assignment: HiringAssignmentDraft
  ): Observable<HiringAssignmentOverview> {
    return this.http.put<HiringAssignmentOverview>(
      `/api/hiring/assignment`,
      assignment
    );
  }

  deleteHiringAssignment(assignmentId: number) {
    return this.http.delete(`/api/hiring/assignment/${assignmentId}`);
  }

  updateEnrollmentTotals() {
    return this.http.get(`/api/academics/section/update-enrollments`);
  }
}
