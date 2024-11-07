/**
 * The Office Hours Resolver allows the office hours data to be injected into the routes
 * of components.
 *
 * @author Ajay Gandecha
 * @copyright 2024
 * @license MIT
 */

import { inject } from '@angular/core';
import { ResolveFn } from '@angular/router';
import { catchError, map, of } from 'rxjs';
import { NewOfficeHours, OfficeHours } from '../../my-courses.model';
import { MyCoursesService } from '../../my-courses.service';

// TODO: Explore if this can be replaced by a signal.
export const officeHoursResolver: ResolveFn<OfficeHours | undefined> = (
  route,
  _state
) => {
  // If the organization is new, return a blank one
  if (route.paramMap.get('event_id')! == 'new') {
    return {
      id: -1,
      type: 0,
      mode: 0,
      description: '',
      location_description: '',
      start_time: new Date(),
      end_time: new Date(),
      course_site_id: +route.paramMap.get('course_site_id')!,
      room_id: '',
      recurrence_id: -1
    };
  }

  // Otherwise, return the organization.
  // If there is an error, return undefined
  return inject(MyCoursesService)
    .getOfficeHours(
      +route.parent!.paramMap.get('course_site_id')!,
      +route.paramMap.get('event_id')!
    )
    .pipe(
      catchError((error) => {
        console.log(error);
        return of(undefined);
      })
    );
};
