import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { map } from 'rxjs';
import { OrganizationAdminPermissionService } from '/workspace/frontend/src/app/organization/organization-admin/organization-admin-permission.service';

export const OrganizationAdminPermissionGuard = (): CanActivateFn => {
  return (_route, _state) => {
    const permission = inject(OrganizationAdminPermissionService);
    const router = inject(Router);
    return permission.checkForOrganizationPermissions().pipe(
      map((isAuthenticated) => {
        if (isAuthenticated) {
          return true;
        } else {
          return router.createUrlTree(['']);
        }
      })
    );
  };
};
