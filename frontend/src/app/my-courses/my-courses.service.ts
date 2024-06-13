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
  TermOverview,
  TermOverviewJson,
  parseTermOverviewJsonList
} from './my-courses.model';
import { map } from 'rxjs';

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
}