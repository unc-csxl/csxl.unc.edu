/**
 * The Academics Resolver allows courses data to be injected into the routes
 * of components.
 *
 * @author Ajay Gandecha
 * @copyright 2023
 * @license MIT
 */

import { inject } from '@angular/core';
import { ResolveFn } from '@angular/router';
import { AcademicsService } from './academics.service';
import { Course, Term } from './academics.models';
import { catchError, of } from 'rxjs';

/** This resolver injects the list of courses into the catalog component. */
export const coursesResolver: ResolveFn<Course[] | undefined> = (
  route,
  state
) => {
  return inject(AcademicsService).getCourses();
};

/** This resolver injects the list of courses into the catalog component. */
export const courseResolver: ResolveFn<Course | undefined> = (route, state) => {
  // If the course is new, return a blank one
  if (route.paramMap.get('id')! == 'new') {
    return {
      id: '',
      subject_code: '',
      number: '',
      title: '',
      description: '',
      credit_hours: -1,
      sections: null
    };
  }

  // Otherwise, return the course.
  // If there is an error, return undefined
  return inject(AcademicsService)
    .getCourse(route.paramMap.get('id')!)
    .pipe(
      catchError((error) => {
        console.log(error);
        return of(undefined);
      })
    );
};

/** This resolver injects the list of terms into the offerings component. */
export const termsResolver: ResolveFn<Term[] | undefined> = (route, state) => {
  return inject(AcademicsService).getTerms();
};
