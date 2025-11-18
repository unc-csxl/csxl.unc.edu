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
import { EventOverview, RegistrationType } from '../event.model';
import { PermissionService } from 'src/app/permission.service';
import { NagivationAdminGearService } from 'src/app/navigation/navigation-admin-gear.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { EventService } from '../event.service';
import { Paginated, PaginationParams } from 'src/app/pagination';
import { PageEvent } from '@angular/material/paginator';

/** Injects the event's name to adjust the title. */
let titleResolver: ResolveFn<string> = (route: ActivatedRouteSnapshot) => {
  return route.parent!.data['event'].name;
};

@Component({
  selector: 'app-event-details',
  templateUrl: './event-details.component.html',
  standalone: false
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
  public event: WritableSignal<EventOverview>;

  /** Event registrations */
  public eventRegistrationsPage: WritableSignal<
    Paginated<Profile, PaginationParams> | undefined
  > = signal(undefined);

  public eventRegistrationDisplayedColumns: string[] = [
    'first_name',
    'last_name',
    'pronouns',
    'email'
  ];

  registrationType = RegistrationType;

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
      event: EventOverview;
    };

    this.event = signal(data.event);

    this.permissionService
      .check(
        'organization.events.edit',
        `organization/${this.event()?.organization_id ?? '*'}`
      )
      .subscribe((permission) => {
        if (permission) {
          // Load user registrations:
          this.eventService
            .getRegisteredUsersForEvent(this.event(), {
              page: 0,
              page_size: 25,
              order_by: 'first_name',
              filter: ''
            } as PaginationParams)
            .subscribe((page) => this.eventRegistrationsPage.set(page));
        }
      });
  }

  ngOnInit() {
    this.gearService.showAdminGearByPermissionCheck(
      'events.*',
      '*',
      '',
      `/events/${this.event()?.organization_slug}/${this.event()?.id}/edit`
    );
  }

  /** Registers a user for an event. */
  registerForEvent() {
    if (this.event().override_registration_url) {
      window.location.href = this.event().override_registration_url!;
      return;
    }

    this.eventService.registerForEvent(this.event()!.id!).subscribe({
      next: () => {
        let newEvent = this.event();
        newEvent.user_registration_type = RegistrationType.ATTENDEE;
        newEvent.number_registered += 1;
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
    newEvent.user_registration_type = null;
    newEvent.number_registered -= 1;
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

  handlePageEvent(e: PageEvent) {
    let paginationParams = this.eventRegistrationsPage()!.params;
    paginationParams.page = e.pageIndex;
    paginationParams.page_size = e.pageSize;
    this.eventService
      .getRegisteredUsersForEvent(this.event(), paginationParams)
      .subscribe((page) => this.eventRegistrationsPage.set(page));
  }
}
