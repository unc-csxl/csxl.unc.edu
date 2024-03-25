import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { OrganizationAdminPermissionGuard } from 'src/app/organization/organization-admin/organization-admin-permission.guard';
import { MatSnackBar } from '@angular/material/snack-bar';
import { OrganizationAdminService } from 'src/app/organization/organization-admin/organization-admin.service';
import { Observable, map, of } from 'rxjs';
import {
  Permission,
  Profile
} from '/workspace/frontend/src/app/profile/profile.service';
import { Organization } from 'src/app/organization/organization.model';
import { Event } from 'src/app/event/event.model';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { organizationResolver } from 'src/app/organization/organization.resolver';
import { EventService } from 'src/app/event/event.service';
import { eventResolver } from '../event.resolver';

@Component({
  selector: 'app-event-list-admin',
  templateUrl: './event-list-admin.component.html',
  styleUrls: ['./event-list-admin.component.css']
})
export class EventListAdminComponent implements OnInit {
  /** Events List */
  protected displayedEvents$: Observable<Event[]>;
  public displayedColumns: string[] = ['name'];

  /** Profile of signed in user */
  protected profile: Profile;
  /** List of displayed organizations for the signed in user */

  /** Route information to be used in Organization Routing Module */
  public static Route = {
    path: 'admin',
    component: EventListAdminComponent,
    title: 'Event Administration',
    canActivate: [OrganizationAdminPermissionGuard()],
    resolve: {
      profile: profileResolver,
      organizations: organizationResolver,
      events: eventResolver
    }
  };

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private snackBar: MatSnackBar,
    private organizationAdminService: OrganizationAdminService,
    private eventService: EventService
  ) {
    this.displayedEvents$ = eventService.getEvents();

    /** Get the profile data of the signed in user */
    const data = this.route.snapshot.data as {
      profile: Profile;
    };
    this.profile = data.profile;
  }

  ngOnInit() {
    if (this.profile.permissions[0].resource !== '*') {
      let userOrganizationPermissions: string[] = this.profile.permissions
        .filter((permission) => permission.resource.includes('organization'))
        .map((permission) => permission.resource.substring(13));

      // this.displayedEvents$ = this.route.snapshot.data['events'] as Observable<
      //   Event[]
      // >;
      this.displayedEvents$ = this.displayedEvents$.pipe(
        map((events) =>
          events.filter(
            (event) =>
              event.organization &&
              userOrganizationPermissions.includes(event.organization.slug)
          )
        )
      );
    }
  }

  /** Resposible for generating delete and create buttons in HTML code when admin signed in */
  adminPermissions(): boolean {
    return this.profile.permissions[0].resource === '*';
  }

  /** Event handler to open Event Editor for the selected event.
   * @param event: event to be edited
   * @returns void
   */
  editEvent(event: Event): void {
    this.router.navigate([
      'events',
      'organizations',
      event.organization?.slug,
      'events',
      event.id,
      'edit'
    ]);
  }
}
