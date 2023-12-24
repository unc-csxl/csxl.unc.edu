import { Injectable } from '@angular/core';
import { map, Observable, ReplaySubject } from 'rxjs';
import { Profile, ProfileService, Permission } from './profile/profile.service';
import { AdminSettingsNavigationData } from './navigation/navigation.service';

@Injectable({
  providedIn: 'root'
})
export class PermissionService {
  private profile$: Observable<Profile | undefined>;

  private adminSettingsData: ReplaySubject<AdminSettingsNavigationData | null> =
    new ReplaySubject(1);
  public adminSettingsData$ = this.adminSettingsData.asObservable();

  constructor(profileService: ProfileService) {
    this.profile$ = profileService.profile$;
  }

  check(action: string, resource: string): Observable<boolean> {
    return this.profile$.pipe(
      map((profile) => {
        if (profile === undefined) {
          return false;
        } else {
          return this.hasPermission(profile.permissions, action, resource);
        }
      })
    );
  }

  private hasPermission(
    permissions: Permission[],
    action: string,
    resource: string
  ) {
    let permission = permissions.find((p) =>
      this.checkPermission(p, action, resource)
    );
    return permission !== undefined;
  }

  private checkPermission(
    permission: Permission,
    action: string,
    resource: string
  ) {
    let actionRegExp = this.expandPattern(permission.action);
    if (actionRegExp.test(action)) {
      let resourceRegExp = this.expandPattern(permission.resource);
      return resourceRegExp.test(resource);
    } else {
      return false;
    }
  }

  private expandPattern(pattern: string): RegExp {
    return new RegExp(`^${pattern.replaceAll('*', '.*')}$`);
  }

  /**
   * This function updates an internal reactive object setup to manage when to show the admin
   * page gear icon or not.
   *
   * @param permissionAction Permission action that must pass for the admin settings to appear.
   * @param permissionResource Permission resource that must pass for the admin settings to appear.
   * @param tooltip Tooltip to display when hovering over the settings gear icon.
   * @param targetUrl URL for the admin page for the button to redirect to.
   */
  public showAdminSettingsNavigation(
    permissionAction: string,
    permissionResource: string,
    tooltip: string,
    targetUrl: string
  ) {
    // First, check to see if the user has the permissions.
    this.check(permissionAction, permissionResource).subscribe(
      (hasPermission) => {
        // If the user has the permission, then update the settings
        // navigation data so that it shows. If not, clear the data.
        if (hasPermission) {
          // Update the settings data
          this.adminSettingsData.next({
            tooltip: tooltip,
            url: targetUrl
          });
        } else {
          // Reset the settings data
          this.adminSettingsData.next(null);
        }
      }
    );
  }
}
