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
import { BehaviorSubject, Observable, switchMap, take, tap } from 'rxjs';
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

  private new_uta$ = new BehaviorSubject<boolean>(true);
  public new_uta: Observable<boolean> = this.new_uta$.asObservable();

  private courses: RxCourseList = new RxCourseList();
  public courses$: Observable<Course[]> = this.courses.value$;

  private sections: RxSectionList = new RxSectionList();
  public sections$: Observable<Section[]> = this.sections.value$;

  constructor(protected http: HttpClient) {
    this.initializeApplicationState();
  }

  /** Returns a list of all Applications
   * @returns {Observable<Application[]>}
   */
  list(): void {
    this.http
      .get<Application[]>('/api/applications')
      .subscribe((applications) => this.applications.set(applications));
  }

  initializeApplicationState(): void {
    this.getApplication().subscribe((application) => {
      this.user_application.set(application);
      this.new_uta$.next(!application);
    });
  }

  getApplication(): Observable<Application | null> {
    return this.http
      .get<Application | null>('/api/applications/user')
      .pipe(
        tap((application) => console.log('Fetched application:', application))
      );
  }

  submitApplication(
    application: Omit<Application, 'id'>
  ): Observable<Application> {
    return this.user_application.value$.pipe(
      take(1),
      switchMap((currentApplication) => {
        return currentApplication
          ? this.updateApplication(
              application,
              currentApplication.id.toString()
            )
          : this.createApplication(application);
      })
    );
  }

  private updateApplication(
    application: Omit<Application, 'id'>,
    appId: string
  ): Observable<Application> {
    return this.http
      .put<Application>(`/api/applications/${appId}`, application)
      .pipe(
        tap((updatedApplication) => {
          this.user_application.set(updatedApplication);
          console.log('Application updated:', updatedApplication);
        })
      );
  }

  private createApplication(
    application: Omit<Application, 'id'>
  ): Observable<Application> {
    return this.http.post<Application>('/api/applications', application).pipe(
      tap((newApplication) => {
        this.user_application.set(newApplication);
        this.new_uta$.next(false);
        console.log('Application created:', newApplication);
      })
    );
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
