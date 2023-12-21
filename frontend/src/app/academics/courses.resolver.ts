/**
 * The Courses Resolver allows courses data to be injected into the routes
 * of components.
 *
 * @author Ajay Gandecha
 * @copyright 2023
 * @license MIT
 */

import { inject } from '@angular/core';
import { ResolveFn } from '@angular/router';
import { CourseService } from './courses.service';
import { Course } from './courses.models';

/** This resolver injects the list of courses into the organization component. */
export const courseResolver: ResolveFn<Course[] | undefined> = (
  route,
  state
) => {
  return inject(CourseService).getCourses();
};
