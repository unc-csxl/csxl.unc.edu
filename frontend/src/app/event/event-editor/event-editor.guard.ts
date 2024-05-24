/**
 * The Event Editor Guard ensures that the page can open if the user has
 * the correct permissions.
 *
 * @author Ajay Gandecha
 * @copyright 2024
 * @license MIT
 */

import { inject } from '@angular/core';
import { CanActivateFn } from '@angular/router';
import { PermissionService } from 'src/app/permission.service';
import { Event } from '../event.model';
import { combineLatest, map } from 'rxjs';
import { EventService } from '../event.service';

// TODO: Refactor with a new event permission API so that we do not
// duplicate calls to the event API here.

/** Determines whether the user can access the event editor.
 * @param route Active route when the user enters the component.
 * @returns {CanActivateFn}
 */
export const eventEditorGuard: CanActivateFn = (route, _) => {
  /** Determine if page is viewable by user based on permissions */

  // Load IDs from the route
  let organizationId: string = route.params['orgid'];
  let eventId: string = route.params['id'];

  // Create two observables for each check

  // Checks if the user has permissions to update events for
  // the organization hosting this event
  const permissionCheck = inject(PermissionService).check(
    'organization.events.update',
    `organization/${organizationId}`
  );

  // Checks if the user is the organizer for the event
  const isOrganizerCheck = inject(EventService)
    .getEvent(+eventId)
    .pipe(map((event) => event?.is_organizer ?? false));

  // Since only one check has to be true for the user to see the page,
  // we combine the results of these observables into a single
  // observable that returns true if either were true.
  return combineLatest([permissionCheck, isOrganizerCheck]).pipe(
    map(([hasPermission, isOrganizer]) => hasPermission || isOrganizer)
  );
};
