/**
 * The Event Detail Page Component shows more details about
 * any given event.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2024
 * @license MIT
 */

import { Component, OnInit } from '@angular/core';
import { eventResolver } from '../event.resolver';
import { Profile, ProfileService } from 'src/app/profile/profile.service';
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
export class EventDetailsComponent implements OnInit {
  /** Route information to be used in Event Routing Module */
  public static Route = {
    path: ':id',
    title: 'Event Details',
    component: EventDetailsComponent,
    resolve: {
      event: eventResolver
    },
    children: [
      { path: '', title: titleResolver, component: EventDetailsComponent }
    ]
  };

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;

  /** The event to show */
  public event: Event | undefined;

  /**
   * Determines whether or not a user can view the event.
   * @returns {Observable<boolean>}
   */
  canViewEvent(): Observable<boolean> {
    return this.permissionService.check(
      'organization.events.view',
      `organization/${this.event?.organization!?.id ?? '*'}`
    );
  }

  /** Constructs the Event Detail component. */
  constructor(
    private route: ActivatedRoute,
    private permissionService: PermissionService,
    private profileService: ProfileService,
    private gearService: NagivationAdminGearService
  ) {
    this.profile = this.profileService.profile()!;

    const data = this.route.snapshot.data as {
      event: Event;
    };

    this.event = data.event;
  }

  ngOnInit() {
    this.gearService.showAdminGearByPermissionCheck(
      'events.*',
      '*',
      '',
      `/events/${this.event?.organization_id}/${this.event?.id}/edit`
    );
  }
}
