/**
 * The Organization Editor Guard ensures that the page can open if the user has either
 * create or edit permissions.
 *
 * @author Ajay Gandecha
 * @copyright 2024
 * @license MIT
 */

import { inject } from '@angular/core';
import { CanActivateFn } from '@angular/router';
import { PermissionService } from 'src/app/permission.service';

/** Determines whether the user can access the organization editor.
 * @param route Active route when the user enters the component.
 * @returns {CanActivateFn}
 */
export const organizationEditorGuard: CanActivateFn = (route, _) => {
  /** Determine if page is viewable by user based on permissions */

  let slug: string = route.params['slug'];

  if (slug === 'new') {
    return inject(PermissionService).check(
      'organization.create',
      'organization'
    );
  } else {
    return inject(PermissionService).check(
      'organization.update',
      `organization/${slug}`
    );
  }
};
