/** Abstracts HTTP request functionality for organizations away from the backend database */

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { EventSummary, OrgRole, OrgRoleSummary, Organization, OrganizationSummary, Profile } from '../models.module';
import { AuthenticationService } from '../authentication.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { BehaviorSubject, Observable, mergeMap, of, shareReplay } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class OrganizationsService {

  /** Store profile observable*/
  public profile$: Observable<Profile | undefined>;

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

  /** Returns all organization entries from the backend database table using the backend HTTP get request. 
   * @returns {Observable<OrganizationSummary[]>}
   */
  getOrganizations = () => {
    return this.http.get<OrganizationSummary[]>("/api/organizations");
  }

  /** Returns the organization object from the backend database table using the backend HTTP get request. 
   * @param id: Number representing the organization id
   * @returns {Observable<OrganizationSummary>}
   */
  getOrganization = (id: Number) => {
    return this.http.get<OrganizationSummary>("/api/organizations/" + id);
  }

  /** Returns the updated organization object from the backend database table using the backend HTTP put request. 
 * @param org: OrganizationSummary representing the updated organization
 * @returns {Observable<OrganizationSummary>}
 */
  updateOrganization = (org: OrganizationSummary) => {
    if (org.id) {
      return this.http.put<OrganizationSummary>("/api/organizations", org);
    } else {
      return this.http.post<OrganizationSummary>("/api/organizations", org);
    }
  }

  /** Returns an Observable Organization based on the given id.
 * @param id: a valid string representing the id of the organization to be added.
 * @returns {Observable<Organization>}
 */
  getOrganizationDetail = (id: string) => {
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
   * Deletes an organization role in the database.
   * @param id: Id of the OrgRole to delete.
   * @returns {Observable<void>}
   */
  deleteOrganizationRole = (id: number) => {
    return this.http.delete<void>(`/api/orgroles/${id}`);
  }

  /**
 * Creates an organization role in the database.
 * @param userId: ID of the user to create the role for.
 * @param orgId: ID of the organization to create the role for.
 * @returns {Observable<OrgRoleSummary>}
 */
  createOrganizationRole = (userId: number, orgId: number) => {
    const newOrgRole: OrgRoleSummary = {
      id: null,
      user_id: userId,
      org_id: orgId,
      membership_type: 0,
      timestamp: new Date()
    }

    // Post new org role object
    return this.http.post<OrgRoleSummary>(`/api/orgroles`, newOrgRole);
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
          this.getOrganizationDetail(`${orgId}`).subscribe((organization) => {
            if (organization.public) {
              // Join organization
              // Create new org role object to post
              const newOrgRole: OrgRoleSummary = {
                id: null,
                user_id: profile!.id!,
                org_id: orgId,
                membership_type: 0,
                timestamp: new Date()
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

  /** Delete an event that the organization is hosting.
   * @param eventId: number representing the ID of the event to be deleted.
   * @returns {void}
   */
  deleteEvent = (eventId: number) => {
    // Make the call to delete the event.
    this.http.delete<void>(`/api/events/${eventId}`).subscribe(() => console.log('Delete successful.'));
  }

  /** Returns the organization roles for an organization using the backend HTTP get request.
 * @param orgId: Number representing the organization ID
 * @returns {Observable<OrgRoleSummary>}
 */
  getRolesForOrganization = (orgId: number) => {
    return this.http.get<OrgRole[]>("/api/orgroles/org/" + orgId);
  }

  /** Delete an organization role based on the role's ID using the backend HTTP delete request.
   * @param orgId: Number representing the organization ID
   */
  deleteRoleFromOrganization = (orgId: number) => {
    return this.http.delete<void>("/api/orgroles/" + orgId);
  }

  /** Promotes a role
   * @param orgRole: Role to promote
   * @returns {Observable<OrgRoleSummary>}
   */
  promoteRole = (orgRole: OrgRoleSummary) => {
    let newSummary: OrgRoleSummary = {
      id: orgRole.id,
      user_id: orgRole.user_id,
      org_id: orgRole.org_id,
      membership_type: 1,
      timestamp: orgRole.timestamp
    }
    return this.http.post<OrgRoleSummary>("/api/orgroles", newSummary);
  }

  demoteRole = (orgRole: OrgRoleSummary) => {
    let newSummary: OrgRoleSummary = {
      id: orgRole.id,
      user_id: orgRole.user_id,
      org_id: orgRole.org_id,
      membership_type: 0,
      timestamp: orgRole.timestamp
    }
    return this.http.post<OrgRoleSummary>("/api/orgroles", newSummary);
  }


}
