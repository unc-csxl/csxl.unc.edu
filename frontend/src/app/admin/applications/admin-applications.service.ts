/**
 * The Admin Organization Service abstracts backend calls from the
 * Admin organization List Component.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Application } from './admin-application.model';
import { RxApplications } from './rx-applications';

@Injectable({ providedIn: 'root' })
export class AdminApplicationsService {
  private applications: RxApplications = new RxApplications();
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
}