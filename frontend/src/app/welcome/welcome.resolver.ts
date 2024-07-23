/**
 * The Welcome Resolver allows the welcome status to be injected into the routes
 * of components.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { inject } from '@angular/core';
import { ResolveFn } from '@angular/router';
import { WelcomeService } from './welcome.service';
import { WelcomeOverview } from './welcome.model';
import { ProfileService } from '../profile/profile.service';

/** This resolver injects an event into the events detail component. */
export const welcomeResolver: ResolveFn<WelcomeOverview> = (route, state) => {
  if (inject(ProfileService).profile() === undefined) {
    return inject(WelcomeService).getWelcomeStatusUnauthenticated();
  }
  return inject(WelcomeService).getWelcomeStatus();
};
