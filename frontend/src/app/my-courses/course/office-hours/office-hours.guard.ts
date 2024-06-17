/**
 * The Office Hour Guard ensures that the page can open based on a user's
 * role in an office hour event.
 *
 * @author Ajay Gandecha
 * @copyright 2024
 * @license MIT
 */

import { inject } from '@angular/core';
import { CanActivateFn } from '@angular/router';
import { MyCoursesService } from '../../my-courses.service';
import { catchError, map, of } from 'rxjs';

/** Determines whether the user has the right role to access a office hour page.
 * @param route Active route when the user enters the component.
 * @returns {CanActivateFn}
 */
export const officeHourPageGuard = (roles: string[]): CanActivateFn => {
  return (route, _) => {
    let event_id: number = route.params['event_id'];

    return inject(MyCoursesService)
      .getOfficeHoursRole(event_id)
      .pipe(map((roleOverview) => roles.includes(roleOverview.role)))
      .pipe(catchError((_) => of(false)));
  };
};
