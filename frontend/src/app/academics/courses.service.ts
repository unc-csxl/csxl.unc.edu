/**
 * The Courses Service abstracts HTTP requests to the backend
 * from the components.
 *
 * @author Ajay Gandecha
 * @copyright 2023
 * @license MIT
 */

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AuthenticationService } from '../authentication.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable } from 'rxjs';
import { Course, Term } from './courses.models';

@Injectable({
  providedIn: 'root'
})
export class CourseService {
  constructor(
    protected http: HttpClient,
    protected auth: AuthenticationService,
    protected snackBar: MatSnackBar
  ) {}

  /** Returns all term entries from the backend database.
   * @returns {Observable<Term[]>}
   */
  getTerms(): Observable<Term[]> {
    return this.http.get<Term[]>('/api/courses/term');
  }

  /** Returns all course entries from the backend database.
   * @returns {Observable<Course[]>}
   */
  getCourses(): Observable<Course[]> {
    return this.http.get<Course[]>('/api/courses/course');
  }
}
