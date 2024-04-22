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
import {
  BehaviorSubject,
  Observable,
  Subscription,
  switchMap,
  take,
  tap
} from 'rxjs';

import { Profile, ProfileService } from '../profile/profile.service';
import { Course, Section } from '../academics/academics.models';
import {
  RxCourseList,
  RxSectionList
} from '../academics/academics-admin/rx-academics-admin';
import { Application } from './application.model';
import { RxApplication, RxApplications } from './rx-applications';

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

  constructor(
    protected http: HttpClient,
    protected profileSvc: ProfileService
  ) {
    this.initializeApplicationState();
  }

  initializeApplicationState(): void {
    this.getApplication().subscribe((application) => {
      this.user_application.set(application);
      this.new_uta$.next(!application);
    });
  }

  getApplication(): Observable<Application | null> {
    return this.http
      .get<Application | null>('/api/applications/ta/user')
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
          ? this.updateApplication(application)
          : this.createApplication(application);
      })
    );
  }

  private updateApplication(
    application: Omit<Application, 'id'>
  ): Observable<Application> {
    return this.http
      .put<Application>(`/api/applications/ta/update`, application)
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
    return this.http
      .post<Application>('/api/applications/ta', application)
      .pipe(
        tap((newApplication) => {
          this.user_application.set(newApplication);
          this.new_uta$.next(false);
          console.log('Application created:', newApplication);
        })
      );
  }

  deleteApplication(): void {
    this.http.delete('/api/application/ta/delete');
  }

  getProfile(): Observable<Profile> {
    return this.http.get<Profile>('/api/profile');
  }

  getSections(): void {
    this.http
      .get<Section[]>('/api/academics/section')
      .subscribe((sections) => this.sections.set(sections));
  }
}
