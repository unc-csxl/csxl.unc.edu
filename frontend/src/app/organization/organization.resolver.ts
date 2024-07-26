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
import { catchError, map, of } from 'rxjs';
import { OrganizationService } from './organization.service';

// TODO: Explore if this can be replaced by a signal.
/** This resolver injects an organization into the organization detail component. */
export const organizationResolver: ResolveFn<Organization | undefined> = (
  route,
  _state
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
