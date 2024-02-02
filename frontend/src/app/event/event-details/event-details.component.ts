/**
 * The Event Detail Page Component shows more details about
 * any given event.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { Component, inject } from '@angular/core';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { eventDetailResolver } from '../event.resolver';
import { Profile } from 'src/app/profile/profile.service';
import {
  ActivatedRoute,
  ActivatedRouteSnapshot,
  ResolveFn
} from '@angular/router';
import { Event } from '../event.model';
import { Observable, of } from 'rxjs';
import { PermissionService } from 'src/app/permission.service';
import { NagivationAdminGearService } from 'src/app/navigation/navigation-admin-gear.service';

/** Injects the event's name to adjust the title. */
let titleResolver: ResolveFn<string> = (route: ActivatedRouteSnapshot) => {
  return route.parent!.data['event'].name;
};

@Component({
  selector: 'app-event-details',
  templateUrl: './event-details.component.html',
  styleUrls: ['./event-details.component.css']
})
export class EventDetailsComponent {
  /** Route information to be used in Event Routing Module */
  public static Route = {
    path: ':id',
    title: 'Event Details',
    component: EventDetailsComponent,
    resolve: {
      profile: profileResolver,
      event: eventDetailResolver
    },
    children: [
      { path: '', title: titleResolver, component: EventDetailsComponent }
    ]
  };

  /** Store Event */
  public event!: Event;

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;
  public adminPermission$: Observable<boolean>;

  constructor(
    private route: ActivatedRoute,
    private permission: PermissionService,
    private gearService: NagivationAdminGearService
  ) {
    /** Initialize data from resolvers. */
    const data = this.route.snapshot.data as {
      profile: Profile;
      event: Event;
    };
    this.profile = data.profile;
    this.event = data.event;

    // Admin Permission if has the actual permission or is event organizer
    this.adminPermission$ = this.permission.check(
      'organization.events.view',
      `organization/${this.event.organization!.id}`
    );
  }

  // eslint-disable-next-line @angular-eslint/use-lifecycle-interface
  ngOnInit() {
    this.gearService.showAdminGear(
      'events.*',
      '*',
      '',
      `events/organizations/${this.event.organization?.slug}/events/${this.event.id}/edit`
    );
  }
}
