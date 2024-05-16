/**
 * The Office Hours Resolver allows office hours sections and events to be injected into the routes
 * of components.
 *
 * @author Sadie Amato, Madelyn Andrews, Bailey DeSouza, Meghan Sun
 * @copyright 2024
 * @license MIT
 */

import { inject } from '@angular/core';
import { ResolveFn } from '@angular/router';
import { OfficeHoursSectionDetails } from './office-hours.models';
import { OfficeHoursService } from './office-hours.service';
import { catchError, of } from 'rxjs';

/** This resolver injects a section into the Office Hours Section component. */
export const ohSectionResolver: ResolveFn<
  OfficeHoursSectionDetails | undefined
> = (route) => {
  return inject(OfficeHoursService)
    .getSection(route.params['id']!)
    .pipe(
      catchError((error) => {
        console.log(error);
        return of(undefined);
      })
    );
};
