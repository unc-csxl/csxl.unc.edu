import { HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, ReplaySubject } from 'rxjs';
import { PermissionService } from '../permission.service';

@Injectable({
  providedIn: 'root'
})
export class NavigationService {
  private title: BehaviorSubject<string> = new BehaviorSubject('');
  public title$ = this.title.asObservable();

  private loading: BehaviorSubject<boolean> = new BehaviorSubject(false);
  public loading$ = this.loading.asObservable();

  private sending: BehaviorSubject<boolean> = new BehaviorSubject(false);
  public sending$ = this.sending.asObservable();

  private _error: BehaviorSubject<string | null> = new BehaviorSubject<
    string | null
  >(null);
  public error$ = this._error.asObservable();

  private adminSettingsData: ReplaySubject<AdminSettingsNavigationData | null> =
    new ReplaySubject(1);
  public adminSettingsData$ = this.adminSettingsData.asObservable();

  constructor(private permissionService: PermissionService) {}

  setTitle(title: string) {
    this._deferToNextChangeDetectionCycle(() => this.title.next(title));
  }

  setLoading(state: boolean) {
    this._deferToNextChangeDetectionCycle(() => this.loading.next(state));
  }

  setSending(state: boolean) {
    this._deferToNextChangeDetectionCycle(() => this.sending.next(state));
  }

  error(e: HttpErrorResponse) {
    this._deferToNextChangeDetectionCycle(() =>
      this._error.next(
        `Response: ${e.status} ${e.statusText}\nEndpoint: ${e.url}`
      )
    );
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
    this.permissionService
      .check(permissionAction, permissionResource)
      .subscribe((hasPermission) => {
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
      });
  }
  /**
   * For reasons that seem related to HttpRequestInterceptor's lifecycle of asynchronous operations
   * being outside the general lifecycle of change detection in angular components, the following
   * workaround method is used to defer updating navigation state until the next tick and, therefore,
   * next change detection cycle.
   *
   * Additional investigation may help determine a better means for achieving this, but for now
   * it avoids the previously commonly seen error of front-end state being changed outside CD cycle.
   *
   * @param operation the logic moved to next tick.
   */
  private _deferToNextChangeDetectionCycle(operation: () => void) {
    setTimeout(operation, 0);
  }
}

export interface AdminSettingsNavigationData {
  tooltip: string;
  url: string;
}
