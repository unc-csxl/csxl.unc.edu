/**
 * The Organization Detail Component displays more information and options regarding
 * UNC CS organizations.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { Component, Signal, signal } from '@angular/core';
import {
  ActivatedRoute,
  ActivatedRouteSnapshot,
  ResolveFn,
  Route
} from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Organization } from '../organization.model';
import {
  Profile,
  ProfileService
} from '/workspace/frontend/src/app/profile/profile.service';
import { organizationEventsResolver } from '../organization.resolver';
import { EventService } from 'src/app/event/event.service';
import { Event } from 'src/app/event/event.model';
import { Observable } from 'rxjs';
import { PermissionService } from 'src/app/permission.service';
import { NewOrganizationService } from '../new-organization.service';

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
  public organization: Signal<Organization | undefined> = signal(undefined);

  /** Store a map of days to a list of events for that day */
  public eventsPerDay: [string, Event[]][];

  /** Whether or not the user has permission to update events. */
  public eventCreationPermission$: Observable<boolean>;

  /** Constructs the Organization Detail component */
  constructor(
    private route: ActivatedRoute,
    protected snackBar: MatSnackBar,
    private profileService: ProfileService,
    private organizationService: NewOrganizationService,
    protected eventService: EventService,
    private permission: PermissionService
  ) {
    this.profile = this.profileService.profile()!;
    let slug = route.snapshot.paramMap.get('slug');
    if (slug && slug !== 'new') {
      this.organization = this.organizationService.getOrganization(slug);
    }

    // TODO: Refactor to remove dependence on resolver.
    const data = this.route.snapshot.data as {
      events: Event[];
    };
    this.eventsPerDay = eventService.groupEventsByDate(data.events ?? []);
    this.eventCreationPermission$ = this.permission.check(
      'organization.*',
      `organization/${this.organization()?.slug ?? '*'}`
    );
  }
}
