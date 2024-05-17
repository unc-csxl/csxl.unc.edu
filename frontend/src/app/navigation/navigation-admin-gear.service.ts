import { Injectable, Signal, WritableSignal, signal } from '@angular/core';
import { PermissionService } from '../permission.service';
import { ReplaySubject } from 'rxjs';
import { AdminSettingsNavigationData } from './navigation.service';

@Injectable({
  providedIn: 'root'
})
export class NagivationAdminGearService {
  public adminSettingsData: WritableSignal<AdminSettingsNavigationData | null> =
    signal(null);

  // private adminSettingsData: ReplaySubject<AdminSettingsNavigationData | null> =
  //   new ReplaySubject(1);
  // public adminSettingsData$ = this.adminSettingsData.asObservable();

  constructor(private permissionService: PermissionService) {}

  /**
   * This function updates an internal reactive object setup to manage when to show the admin
   * page gear icon or not.
   *
   * @param permissionAction Permission action that must pass for the admin settings to appear.
   * @param permissionResource Permission resource that must pass for the admin settings to appear.
   * @param tooltip Tooltip to display when hovering over the settings gear icon.
   * @param targetUrl URL for the admin page for the button to redirect to.
   */
  public showAdminGear(
    permissionAction: string,
    permissionResource: string,
    tooltip: string,
    targetUrl: string
  ) {
    // First, check to see if the user has the permissions.
    this.permissionService
      .check(permissionAction, permissionResource)
      .subscribe((hasPermission) => {
        // If the user has the permission, then update the settings
        // navigation data so that it shows. If not, clear the data.
        if (hasPermission) {
          // Update the settings data
          this.adminSettingsData.set({
            tooltip: tooltip,
            url: targetUrl
          });
        } else {
          // Reset the settings data
          this.adminSettingsData.set(null);
        }
      });
  }

  public resetAdminSettingsNavigation() {
    this.adminSettingsData.set(null);
  }
}
