/**
 * The My Courses Service abstracts HTTP requests to the backend
 * from the components.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { Injectable, WritableSignal, computed, signal } from '@angular/core';

import { HttpClient } from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';
import {
  OfficeHourEventOverview,
  OfficeHourEventOverviewJson,
  TermOverview,
  TermOverviewJson,
  parseOfficeHourEventOverviewJson,
  parseTermOverviewJsonList
} from './my-courses.model';
import { Observable, map } from 'rxjs';
import { Paginator } from '../pagination';

@Injectable({
  providedIn: 'root'
})
export class MyCoursesService {
  /** Encapsulated terms signal */
  private termsSignal: WritableSignal<TermOverview[]> = signal([]);

  /** Exposed computed signals based on date */
  currentTerms = computed(() => {
    return this.termsSignal().filter((term) => {
      let currentDate = new Date();
      return term.start <= currentDate && currentDate <= term.end;
    });
  });

  pastTerms = computed(() => {
    return this.termsSignal().filter((term) => {
      let currentDate = new Date();
      return term.end < currentDate;
    });
  });

  /** Constructor */
  constructor(
    protected http: HttpClient,
    protected snackBar: MatSnackBar
  ) {
    this.getTermOverviews();
  }

  /** Refreshes the my courses data emitted by the signals. */
  getTermOverviews() {
    this.http
      .get<TermOverviewJson[]>('/api/academics/my-courses')
      .pipe(map(parseTermOverviewJsonList))
      .subscribe((terms) => {
        this.termsSignal.set(terms);
      });
  }

  /**
   * Returns the current and upcoming office hour events for a given course.
   *
   * @param termId: ID for the term of the course
   * @param courseId: ID for the course
   * @returns { Observable<OfficeHourEventOverview[]> }
   */
  getCurrentOfficeHourEvents(
    termId: string,
    courseId: string
  ): Observable<OfficeHourEventOverview[]> {
    return this.http
      .get<OfficeHourEventOverviewJson[]>(
        `/api/academics/my-courses/${termId}/${courseId}/oh-events/current`
      )
      .pipe(
        map((responseModel) => {
          return responseModel.map(parseOfficeHourEventOverviewJson);
        })
      );
  }
}
