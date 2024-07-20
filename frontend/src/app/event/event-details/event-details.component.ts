/**
 * The Event Detail Page Component shows more details about
 * any given event.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2024
 * @license MIT
 */

import { Component, OnInit, WritableSignal, signal } from '@angular/core';
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
import { MatSnackBar } from '@angular/material/snack-bar';
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
  public event: WritableSignal<Event>;

  /**
   * Determines whether or not a user can view the event.
   * @returns {Observable<boolean>}
   */
  canViewEvent(): Observable<boolean> {
    return this.permissionService.check(
      'organization.events.view',
      `organization/${this.event()?.organization!?.id ?? '*'}`
    );
  }

  /** Constructs the Event Detail component. */
  constructor(
    private route: ActivatedRoute,
    private permissionService: PermissionService,
    private profileService: ProfileService,
    private gearService: NagivationAdminGearService,
    protected snackBar: MatSnackBar,
    private eventService: EventService
  ) {
    this.profile = this.profileService.profile()!;

    const data = this.route.snapshot.data as {
      event: Event;
    };

    this.event = signal(data.event);
  }

  ngOnInit() {
    this.gearService.showAdminGearByPermissionCheck(
      'events.*',
      '*',
      '',
      `/events/${this.event()?.organization_id}/${this.event()?.id}/edit`
    );
  }

  /** Registers a user for an event. */
  registerForEvent() {
    this.eventService.registerForEvent(this.event()!.id!).subscribe({
      next: () => {
        let newEvent = this.event();
        newEvent.is_attendee = true;
        newEvent.registration_count += 1;
        this.event.set(newEvent);

        this.snackBar.open(
          `Successfully registered for ${this.event()!.name}!`,
          'Close',
          { duration: 15000 }
        );
      },
      error: () => {
        this.snackBar.open(
          `Error: Could not register. Please try again.`,
          'Close',
          { duration: 15000 }
        );
      }
    });
  }

  /** Unregisters a user from an evenet. */
  unregisterForEvent() {
    let newEvent = this.event();
    newEvent.is_attendee = false;
    newEvent.registration_count -= 1;
    this.event.set(newEvent);

    this.eventService.unregisterForEvent(this.event()!.id!).subscribe({
      next: () => {
        this.snackBar.open(
          `Successfully unregistered for ${this.event()!.name}!`,
          'Close',
          { duration: 15000 }
        );
      },
      error: () => {
        this.snackBar.open(
          `Error: Could not unregister. Please try again.`,
          'Close',
          { duration: 15000 }
        );
      }
    });
  }
}
