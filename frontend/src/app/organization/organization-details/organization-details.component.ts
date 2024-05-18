/**
 * The Organization Detail Component displays more information and options regarding
 * UNC CS organizations.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2024
 * @license MIT
 */

import { Component } from '@angular/core';
import {
  ActivatedRoute,
  ActivatedRouteSnapshot,
  ResolveFn,
  Route
} from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Organization } from '../organization.model';
import { Profile, ProfileService } from '../../profile/profile.service';
import {
  organizationResolver,
  organizationEventsResolver
} from '../organization.resolver';
import { EventService } from '../../event/event.service';
import { Event } from '../../event/event.model';
import { Observable } from 'rxjs';
import { PermissionService } from '../../permission.service';

/** Injects the organization's name to adjust the title. */
let titleResolver: ResolveFn<string> = (route: ActivatedRouteSnapshot) => {
  return route.parent!.data['organization']?.name ?? 'Organization Not Found';
};

@Component({
  selector: 'app-organization-details',
  templateUrl: './organization-details.component.html',
  styleUrls: ['./organization-details.component.css']
})
export class OrganizationDetailsComponent {
  /** Route information to be used in Organization Routing Module */
  public static Route: Route = {
    path: ':slug',
    component: OrganizationDetailsComponent,
    resolve: {
      organization: organizationResolver,
      events: organizationEventsResolver
    },
    children: [
      {
        path: '',
        title: titleResolver,
        component: OrganizationDetailsComponent
      }
    ]
  };

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;

  /** The organization to show */
  public organization: Organization | undefined;

  // TODO: Refactor once the event feature is refactored.
  /** Store a map of days to a list of events for that day */
  public eventsPerDay: [string, Event[]][];

  // TODO: Refactor once the event feature is refactored.
  /** Whether or not the user has permission to update events. */
  public eventCreationPermission$: Observable<boolean>;

  /** Constructs the Organization Detail component */
  constructor(
    private route: ActivatedRoute,
    protected snackBar: MatSnackBar,
    private profileService: ProfileService,
    protected eventService: EventService,
    private permission: PermissionService
  ) {
    this.profile = this.profileService.profile()!;

    const data = this.route.snapshot.data as {
      organization: Organization;
      events: Event[];
    };

    this.organization = data.organization;
    this.eventsPerDay = eventService.groupEventsByDate(data.events ?? []);
    this.eventCreationPermission$ = this.permission.check(
      'organization.*',
      `organization/${this.organization?.slug ?? '*'}`
    );
  }
}
