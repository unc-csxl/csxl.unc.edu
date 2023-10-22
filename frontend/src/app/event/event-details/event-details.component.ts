/**
 * The Event Detail Page Component shows more details about
 * any given event.
 * 
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { Component } from '@angular/core';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { eventDetailResolver } from '../event.resolver';
import { Profile } from 'src/app/profile/profile.service';
import { ActivatedRoute, ActivatedRouteSnapshot, ResolveFn } from '@angular/router';
import { Event } from '../event.model';
import { Observable } from 'rxjs';
import { PermissionService } from 'src/app/permission.service';
import { EventService } from '../event.service';

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
    resolve: { profile: profileResolver, event: eventDetailResolver },
    children: [{ path: '', title: titleResolver, component: EventDetailsComponent }]
  }

  /** Store Event */
  public event!: Event;
  public eventManagementPermission$: Observable<boolean>;

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;


  constructor(private route: ActivatedRoute, private permission: PermissionService) {
    /** Initialize data from resolvers. */
    const data = this.route.snapshot.data as { profile: Profile, event: Event };
    this.profile = data.profile;
    this.event = data.event;
    this.eventManagementPermission$ = this.permission.check('organization.events.manage', `organization/${this.event.organization_id}`);
  }
}
