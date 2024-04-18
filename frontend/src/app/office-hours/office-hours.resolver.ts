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

/** This resolver injects the list of sections in the current term into the Office Hours Home component. */
export const sectionsListResolver: ResolveFn<
  OfficeHoursSectionDetails[] | undefined
> = (route) => {
  return inject(OfficeHoursService).getUserSectionsByTerm('S24');
};

/** This resolver injects a section into the Office Hours Section component. */
export const sectionResolver: ResolveFn<
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
