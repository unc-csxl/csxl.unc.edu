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
import { BehaviorSubject, Observable } from 'rxjs';
import { Application } from '../admin/applications/admin-application.model';
import {
  RxApplications,
  RxApplication
} from '../admin/applications/rx-applications';
import { Profile } from '../profile/profile.service';
import { Course, Section } from '../academics/academics.models';
import {
  RxCourseList,
  RxSectionList
} from '../academics/academics-admin/rx-academics-admin';

@Injectable({ providedIn: 'root' })
export class ApplicationsService {
  private applications: RxApplications = new RxApplications();
  public applications$: Observable<Application[]> = this.applications.value$;

  private user_application: RxApplication = new RxApplication();
  public user_application$: Observable<Application | null> =
    this.user_application.value$;

  public new_uta$ = new BehaviorSubject<boolean>(false);

  public new_uta: boolean;

  private courses: RxCourseList = new RxCourseList();
  public courses$: Observable<Course[]> = this.courses.value$;

  private sections: RxSectionList = new RxSectionList();
  public sections$: Observable<Section[]> = this.sections.value$;

  constructor(protected http: HttpClient) {
    this.new_uta = this.getApplication();
  }

  /** Returns a list of all Applications
   * @returns {Observable<Application[]>}
   */
  list(): void {
    this.http
      .get<Application[]>('/api/applications')
      .subscribe((applications) => this.applications.set(applications));
  }

  getApplication(): boolean {
    this.http
      .get<Application>('/api/applications/user')
      .subscribe((application) => {
        console.log(application);
        if (application !== null) {
          this.user_application.set(application);
          this.new_uta$.next(false);
          this.new_uta = false;
          console.log('false');
          return false;
        } else {
          this.user_application.set(null);
          this.new_uta$.next(true);
          this.new_uta = true;
          console.log('true');
          return true;
        }
      });
    return true;
  }

  /** Creates an application
   * @param application: Application object that you want to add to the database
   * @returns {Observable<Application>}
   */
  createApplication(application: Application): Observable<Application> {
    return this.http.post<Application>('/api/applications', application);
  }

  updateApplication(application: Application): Observable<Application> {
    return this.http.put<Application>('/api/applications/update', application);
  }

  deleteApplication(): void {
    this.http.delete('/api/application/delete');
  }

  getProfile(): Observable<Profile> {
    return this.http.get<Profile>('/api/profile');
  }

  getCourses(): void {
    this.http
      .get<Course[]>('/api/academics/course')
      .subscribe((courses) => this.courses.set(courses));
  }

  getSections(): void {
    this.http
      .get<Section[]>('/api/academics/section')
      .subscribe((sections) => this.sections.set(sections));
  }
}
