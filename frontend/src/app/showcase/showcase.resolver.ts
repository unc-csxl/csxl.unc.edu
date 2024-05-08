/**
 * The Showcase Resolver allows projects to be injected into the routes
 * of components.
 *
 * @author Ajay Gandecha
 * @copyright 2024
 * @license MIT
 */

import { inject } from '@angular/core';
import { ResolveFn } from '@angular/router';
import { ShowcaseProject } from './showcaseproject.model';
import { ShowcaseService } from './showcase.service';

/** This resolver injects the list of projects into the project component. */
export const showcaseResolver: ResolveFn<ShowcaseProject[] | undefined> = (
  route,
  state
) => {
  return inject(ShowcaseService).getProjects();
};
