/**
 * The Instructor Editor Guard ensures that the page can open if the user
 * is an instructor.
 *
 * @author Ajay Gandecha
 * @copyright 2024
 * @license MIT
 */

import { HttpClient } from '@angular/common/http';
import { inject } from '@angular/core';
import { CanActivateFn } from '@angular/router';
import { PermissionService } from 'src/app/permission.service';
import {
  parseTermOverviewJsonList,
  TermOverviewJson
} from './my-courses.model';
import { map } from 'rxjs';

export const myCoursesInstructorGuard: CanActivateFn = (route, _) => {
  /** Determine if page is viewable by user based on permissions */
  let id = +route.parent!.params['course_site_id'];
  return inject(HttpClient)
    .get<TermOverviewJson[]>('/api/my-courses')
    .pipe(map(parseTermOverviewJsonList))
    .pipe(
      map(
        (terms) =>
          terms.flatMap((term) => term.sites).find((site) => site.id === id)
            ?.role == 'Instructor'
      )
    );
};
