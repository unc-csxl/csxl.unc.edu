/**
 * The Event Detail Card widget abstracts the implementation of the
 * detail event card from the whole event page.
 *
 * @author Ajay Gandecha, Jade Keegan
 * @copyright 2023
 * @license MIT
 */

import { Component, Input, OnInit } from '@angular/core';
import { Event, EventRegistration } from '../../event.model';
import { MatSnackBar } from '@angular/material/snack-bar';
import { EventService } from '../../event.service';
import { Observable, of } from 'rxjs';
import { PermissionService } from 'src/app/permission.service';
import { Profile } from 'src/app/models.module';
import { Router } from '@angular/router';

@Component({
  selector: 'event-detail-card',
  templateUrl: './event-detail-card.widget.html',
  styleUrls: ['./event-detail-card.widget.css']
})
export class EventDetailCard implements OnInit {
  /** The event for the event card to display */
  @Input() event!: Event;
  @Input() profile!: Profile;
  adminPermission$!: Observable<boolean>;

  /** Constructs the widget */
  constructor(
    protected snackBar: MatSnackBar,
    protected eventService: EventService,
    private permission: PermissionService,
    private router: Router
  ) {}

  ngOnInit() {
    this.adminPermission$ = this.permission.check(
      'organization.events.*',
      `organization/${this.event.organization_id!}`
    );
  }

  /** Handler for when the share button is pressed
   *  This function copies the permalink to the event to the user's
   *  clipboard.
   */
  onShareButtonClick() {
    // Write the URL to the clipboard
    navigator.clipboard.writeText(
      'https://' + window.location.host + '/events/' + this.event.id
    );
    // Open a snackbar to alert the user
    this.snackBar.open('Event link copied to clipboard.', '', {
      duration: 3000
    });
  }

  /** Delete the given event object using the Event Service's deleteEvent method
   * @param event: Event representing the updated event
   * @returns void
   */
  deleteEvent(event: Event): void {
    let confirmDelete = this.snackBar.open(
      'Are you sure you want to delete this event?',
      'Delete',
      { duration: 15000 }
    );
    confirmDelete.onAction().subscribe(() => {
      this.eventService.deleteEvent(event).subscribe(() => {
        this.snackBar.open('Event Deleted', '', { duration: 2000 });
        this.router.navigateByUrl('/events');
      });
    });
  }

  /** Registers a user for the given event
   * @param event_id: number representing the id of the Event to register the User for
   */
  registerForEvent(event_id: number) {
    let confirmRegistration = this.snackBar.open(
      'Are you sure you want to register for this event?',
      'Register'
    );
    confirmRegistration.onAction().subscribe(() => {
      this.eventService.registerForEvent(event_id).subscribe({
        next: (event_registration) => this.onSuccess(event_registration),
        error: (err) => this.onError(err)
      });
    });
  }

  /** Registers a user for the given event
   * @param event_id: number representing the id of the Event to register the User for
   */
  unregisterForEvent(event_registration_id: number) {
    let confirmUnregistration = this.snackBar.open(
      'Are you sure you want to unregister for this event?',
      'Unregister',
      { duration: 15000 }
    );
    confirmUnregistration.onAction().subscribe(() => {
      this.eventService
        .unregisterForEvent(event_registration_id)
        .subscribe(() => {
          this.event.is_attendee = false;
          this.event.registration_count -= 1;
          this.snackBar.open('Successfully Unregistered!', '', {
            duration: 2000
          });
        });
    });
  }

  /** Opens a confirmation snackbar when an event is successfully created.
   * @returns {void}
   */
  private onSuccess(event_registration: EventRegistration): void {
    this.event.is_attendee = true;
    this.event.registration_count += 1;
    this.snackBar.open('Thanks for registering!', '', { duration: 2000 });
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
