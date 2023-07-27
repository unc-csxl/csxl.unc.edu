import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, mergeMap, of, shareReplay } from 'rxjs';
import { EventSummary, OrgRoleSummary, Organization, Profile } from '../models.module';
import { AuthenticationService } from '../authentication.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Injectable({
  providedIn: 'root'
})

export class OrgDetailsService {

  /** Store profile observable*/
  public profile$: Observable<Profile | undefined>;

  /** Store unwrapped profile */
  public starred: boolean = false;

  constructor(protected http: HttpClient, protected auth: AuthenticationService, protected snackBar: MatSnackBar) {
    /** If profile is authenticated, display profile page. */
    this.profile$ = this.auth.isAuthenticated$.pipe(
      mergeMap(isAuthenticated => {
        if (isAuthenticated) {
          return this.http.get<Profile>('/api/profile');
        } else {
          return of(undefined);
        }
      }),
      shareReplay(1)
    );
  }

  /** Returns an Observable Organization based on the given id.
   * @param id: a valid string representing the id of the organization to be added.
   * @returns {Observable<Organization>}
   */
  getOrganization = (id: string) => {
    return this.http.get<Organization>("/api/organizations/" + id);
  }

  /** Creates an event in the backend table based on the given event model
   * @param event: a valid EventSummary model that represents the event to be created
   * @returns {Observable<EventSummary>}
   */
  create = (event: EventSummary) => {
    return this.http.post<EventSummary>("/api/events", event);
  }

  /**
   * Toggles the membership status of a user for an organization.
   * @param orgId: number representing the ID of the organization to join or leave
   * @returns {void}
   */
  toggleOrganizationMembership = (orgId: number) => {

    // First, ensure profile exists
    if (this.profile$) {
      // Then, subscribe to access profile contents
      this.profile$.subscribe(profile => {
        // Check if user is already a member of the organization
        let assocFilter = profile!.organization_associations!.filter((orgRole) => orgRole.org_id == orgId);
        if (assocFilter && assocFilter!.length > 0 && assocFilter[0].membership_type >= 0) {
          // If so, the membership is to be deleted
          // First, confirm with the user in a snackbar
          let deleteMembershipSnackBarRef = this.snackBar.open("Are you sure you want to leave this organization?", "Leave");

          deleteMembershipSnackBarRef.onAction().subscribe(() => {
            // If snackbar button pressed, delete membership
            const orgRoleId = assocFilter[0].id!;
            this.http.delete<void>(`/api/orgroles/${orgRoleId}`).subscribe(() => {
              console.log('Delete successful.');
              location.reload();
            });
          })
        }
        else {
          // If not, check if user can join on their own
          this.getOrganization(`${orgId}`).subscribe((organization) => {
            if (organization.public) {
              // Join organization
              // Create new org role object to post
              const newOrgRole: OrgRoleSummary = {
                id: null,
                user_id: profile!.id!,
                org_id: orgId,
                membership_type: 0
              }

              // Post new org role object
              this.http.post<OrgRoleSummary>(`/api/orgroles`, newOrgRole).subscribe(() => {
                console.log('Role added successfully.');
                location.reload();
              });

              // Set slight delay so page reloads after API calls finish running.
              new Promise(f => setTimeout(f, 200));

              // Reload the window to update the events.
              location.reload();
            }
            else {
              // User cannot join the organization without getting approved.
              this.snackBar.open(`To join ${organization.slug}, you must be added manually by the organization!`, "Close");
            }
          })
        }
      })
    }
  }


  /** Toggles the star status of the organization.
   * @deprecated
   * @param orgId: number representing the ID of the organization to be "starred"
   * @returns {void}
   */
  starOrganization = (orgId: number) => {

    // First, ensure profile exists
    if (this.profile$) {
      this.profile$.subscribe(profile => {

        // Check if item is already starred
        let assocFilter = profile!.organization_associations!.filter((orgRole) => orgRole.org_id == orgId);
        if (assocFilter && assocFilter!.length > 0 && assocFilter[0].membership_type >= 0) {
          // If so, delete the star
          const orgRoleId = assocFilter[0].id!;
          this.http.delete<void>(`/api/orgroles/${orgRoleId}`).subscribe(() => console.log('Delete successful.'));
        }
        else {
          // If not, add the star
          // Create new org role object to post
          const newOrgRole: OrgRoleSummary = {
            id: null,
            user_id: profile!.id!,
            org_id: orgId,
            membership_type: 0
          }

          // Post new org role object
          this.http.post<OrgRoleSummary>(`/api/orgroles`, newOrgRole).subscribe(() => console.log('Role added successfully.'));
        }
      }
      )

    }
  }

  /** Delete an event that the organization is hosting.
   * @param eventId: number representing the ID of the event to be deleted.
   * @returns {void}
   */
  deleteEvent = (eventId: number) => {
    // Make the call to delete the event.
    this.http.delete<void>(`/api/events/${eventId}`).subscribe(() => console.log('Delete successful.'));
  }
}