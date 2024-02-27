import { Injectable } from '@angular/core';
import { map, Observable } from 'rxjs';
import {
  Profile,
  ProfileService,
  Permission
} from '/workspace/frontend/src/app/profile/profile.service';

@Injectable({
  providedIn: 'root'
})
export class OrganizationAdminPermissionService {
  private profile$: Observable<Profile | undefined>;

  constructor(profileService: ProfileService) {
    this.profile$ = profileService.profile$;
  }
  /** Check to see if the currently signed in user has any organization permissions */
  checkForOrganizationPermissions(): Observable<boolean> {
    return this.profile$.pipe(
      map((profile) => {
        if (profile === undefined) {
          return false;
        } else if (profile.permissions.length !== 0) {
          return this.hasOrganizationPermissions(profile.permissions);
        } else {
          return false;
        }
      })
    );
  }

  private hasOrganizationPermissions(permissions: Permission[]): boolean {
    if (permissions[0].resource === '*') {
      return true;
    } else {
      let organization_index = permissions.findIndex((element) =>
        element.resource.includes('organization')
      );
      return organization_index !== -1;
    }
  }
}
