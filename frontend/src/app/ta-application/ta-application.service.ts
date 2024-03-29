/**
 * The TA Application Service abstracts backend calls from the
 * Admin organization List Component.
 *
 * @author Ben Goulet
 * @copyright 2024
 * @license MIT
 */

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Application } from '../admin/applications/admin-application.model';
import { RxApplication } from '../admin/applications/rx-applications';
import { Profile } from '../profile/profile.service';

@Injectable({ providedIn: 'root' })
export class ApplicationsService {
  private applications: RxApplication = new RxApplication();
  public applications$: Observable<Application[]> = this.applications.value$;

  constructor(protected http: HttpClient) {}

  /** Returns a list of all Applications
   * @returns {Observable<Application[]>}
   */
  list(): void {
    this.http
      .get<Application[]>('/api/applications')
      .subscribe((applications) => this.applications.set(applications));
  }

  /** Creates an application
   * @param application: Application object that you want to add to the database
   * @returns {Observable<Application>}
   */
  createApplication(application: Application): Observable<Application> {
    return this.http.post<Application>('/api/applications', application);
  }

  getProfile(): Observable<Profile> {
    return this.http.get<Profile>('/api/profile');
  }
}
