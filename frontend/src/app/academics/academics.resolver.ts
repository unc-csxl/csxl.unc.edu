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
import { CourseService } from './academics.service';
import { Course, Term } from './academics.models';

/** This resolver injects the list of courses into the catalog component. */
export const courseResolver: ResolveFn<Course[] | undefined> = (
  route,
  state
) => {
  return inject(CourseService).getCourses();
};

/** This resolver injects the list of terms into the offerings component. */
export const termResolver: ResolveFn<Term[] | undefined> = (route, state) => {
  return inject(CourseService).getTerms();
};
