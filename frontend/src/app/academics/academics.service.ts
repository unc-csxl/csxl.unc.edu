/**
 * The Academics Service abstracts HTTP requests to the backend
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
import { Course, Term } from './academics.models';

@Injectable({
  providedIn: 'root'
})
export class AcademicsService {
  constructor(
    protected http: HttpClient,
    protected auth: AuthenticationService,
    protected snackBar: MatSnackBar
  ) {}

  /** Returns all term entries from the backend database.
   * @returns {Observable<Term[]>}
   */
  getTerms(): Observable<Term[]> {
    return this.http.get<Term[]>('/api/academics/term');
  }

  /** Returns one term from the backend database.
   * @param id ID of the course to look up
   * @returns {Observable<Term>}
   */
  getTerm(id: string): Observable<Term> {
    return this.http.get<Term>(`/api/academics/term/${id}`);
  }

  /** Creates a new term.
   * @param term: Term to create
   * @returns {Observable<Term>}
   */
  createTerm(term: Term): Observable<Term> {
    return this.http.post<Term>('/api/academics/term', term);
  }

  /** Update a term.
   * @param term: Term to update
   * @returns {Observable<Term>}
   */
  updateTerm(term: Term): Observable<Term> {
    return this.http.put<Term>('/api/academics/term', term);
  }

  /** Delete a term.
   * @param course: Term to update
   * @returns {Observable<Term>}
   */
  deleteTerm(term: Term): Observable<Term> {
    return this.http.delete<Term>(`/api/academics/term/${term.id}`);
  }

  /** Returns all course entries from the backend database.
   * @returns {Observable<Course[]>}
   */
  getCourses(): Observable<Course[]> {
    return this.http.get<Course[]>('/api/academics/course');
  }

  /** Returns one course from the backend database.
   * @param id ID of the course to look up
   * @returns {Observable<Course>}
   */
  getCourse(id: string): Observable<Course> {
    return this.http.get<Course>(`/api/academics/course/${id}`);
  }

  /** Creates a new course.
   * @param course: Course to create
   * @returns {Observable<Course>}
   */
  createCourse(course: Course): Observable<Course> {
    return this.http.post<Course>('/api/academics/course', course);
  }

  /** Update a course.
   * @param course: Course to update
   * @returns {Observable<Course>}
   */
  updateCourse(course: Course): Observable<Course> {
    return this.http.put<Course>('/api/academics/course', course);
  }

  /** Delete a course.
   * @param course: Course to delete
   * @returns {Observable<Course>}
   */
  deleteCourse(course: Course): Observable<Course> {
    return this.http.delete<Course>(`/api/academics/course/${course.id}`);
  }
}
