import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, mergeMap, of, shareReplay } from 'rxjs';
import { EventSummary2, OrgRoleSummary, Organization, OrganizationSummary, Profile } from '../models.module';
import { AuthenticationService } from '../authentication.service';

@Injectable({
  providedIn: 'root'
})

export class OrgDetailsService {

  /** Store profile observable*/
  public profile$: Observable<Profile | undefined>;

  /** Store unwrapped profile */
  public starred: boolean = false;

  constructor(protected http: HttpClient, protected auth: AuthenticationService) {
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

  getOrganization(id: string): Observable<Organization> {
    return this.http.get<Organization>("/api/organizations/" + id);
  }

  create(event: EventSummary2) {
    return this.http.post<EventSummary2>("/api/events", event);
  }

  /**
   * Toggles the star status of the organization.
   */
  starOrganization(orgId: number) {

    // First, ensure profile exists
    if (this.profile$) {
      this.profile$.subscribe(profile => {
        
        // Check if item is already starred
        let assocFilter = profile!.organization_associations!.filter((orgRole) => orgRole.org_id?.valueOf() == orgId);
        if (assocFilter && assocFilter!.length > 0 && assocFilter[0].membership_type.valueOf() >= 0) {
          // If so, delete the star
          const orgRoleId = assocFilter[0].id!.valueOf();
          console.log(orgRoleId);
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

  /**
   * Delete an event that the organization is hosting.
   */
  deleteEvent(eventId: number) {

    // Make the call to delete the event.
    this.http.delete<void>(`/api/events/${eventId}`).subscribe(() => console.log('Delete successful.'));
  }
}
