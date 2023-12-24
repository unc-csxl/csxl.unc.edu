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
import {
  ActivatedRoute,
  ActivatedRouteSnapshot,
  ResolveFn
} from '@angular/router';
import { Event } from '../event.model';
import { EventRegistrationEvent } from '../widgets/event-detail-card/event-detail-card.widget';
import { EventService } from '../event.service';
import { MatSnackBar } from '@angular/material/snack-bar';

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
    children: [
      { path: '', title: titleResolver, component: EventDetailsComponent }
    ]
  };

  /** Store Event */
  public event!: Event;

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;

  constructor(
    private route: ActivatedRoute,
    private eventService: EventService,
    protected snackBar: MatSnackBar
  ) {
    /** Initialize data from resolvers. */
    const data = this.route.snapshot.data as { profile: Profile; event: Event };
    this.profile = data.profile;
    this.event = data.event;
  }

  register(event: EventRegistrationEvent) {
    this.eventService.registerForEvent(event.event.id!).subscribe({
      next: (event_registration) => {
        this.event.is_registered = true;
        this.snackBar.open('Successfully registered for event', '', {
          duration: 1000
        });
      },
      error: (err) => this.onError(err)
    });
  }

  unregister(event: EventRegistrationEvent) {
    this.eventService.unregisterForEvent(event.event.id!).subscribe(() => {
      this.event.is_registered = false;
      this.snackBar.open('Successfully Unregistered!', '', {
        duration: 2000
      });
    });
  }

  /** Opens a confirmation snackbar when there is an error creating an event.
   * @returns {void}
   */
  private onError(err: any): void {
    this.snackBar.open('Error: Event Not Registered For', '', {
      duration: 2000
    });
  }
}
