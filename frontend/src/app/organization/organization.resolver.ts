/**
 * The Organization Resolver allows the organization to be injected into the routes
 * of components.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { inject } from '@angular/core';
import { ResolveFn } from '@angular/router';
import { Organization } from './organization.model';
import { OrganizationService } from './organization.service';
import { EventService } from '../event/event.service';
import { Event } from '../event/event.model';
import { catchError, map, of } from 'rxjs';

/** This resolver injects the list of organizations into the organization component. */
export const organizationResolver: ResolveFn<Organization[] | undefined> = (
  route,
  state
) => {
  return inject(OrganizationService).getOrganizations();
};

/** This resolver injects an organization into the organization detail component. */
export const organizationDetailResolver: ResolveFn<Organization | undefined> = (
  route,
  state
) => {
  // If the organization is new, return a blank one
  if (route.paramMap.get('slug')! == 'new') {
    return {
      id: null,
      name: '',
      shorthand: '',
      slug: '',
      logo: '',
      short_description: '',
      long_description: '',
      email: '',
      website: '',
      instagram: '',
      linked_in: '',
      youtube: '',
      heel_life: '',
      public: false,
      events: null
    };
  }

  // Otherwise, return the organization.
  // If there is an error, return undefined
  return inject(OrganizationService)
    .getOrganization(route.paramMap.get('slug')!)
    .pipe(
      catchError((error) => {
        console.log(error);
        return of(undefined);
      })
    );
};

/** This resolver injects the events for a given organization into the organization component. */
export const organizationEventsResolver: ResolveFn<Event[] | undefined> = (
  route,
  state
) => {
  return inject(EventService).getEventsByOrganization(
    route.paramMap.get('slug')!
  );
};
