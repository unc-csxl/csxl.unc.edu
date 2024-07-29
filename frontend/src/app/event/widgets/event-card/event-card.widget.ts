/**
 * The Event Card displays details for events in the paginated list.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { Component, EventEmitter, Input, Output } from '@angular/core';
import { EventOverview, RegistrationType } from '../../event.model';
import { EventService } from '../../event.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Profile } from 'src/app/profile/profile.service';

@Component({
  selector: 'new-event-card',
  templateUrl: './event-card.widget.html',
  styleUrl: './event-card.widget.css'
})
export class EventCardWidget {
  @Input() profile: Profile | undefined;
  registrationType = RegistrationType;
  @Input() event!: EventOverview;
  @Output() registrationChange = new EventEmitter<boolean>();

  now = new Date();

  constructor(
    protected eventService: EventService,
    protected snackBar: MatSnackBar
  ) {}

  /** Registers a user for an event. */
  registerForEvent() {
    this.eventService.registerForEvent(this.event.id!).subscribe({
      next: () => {
        this.registrationChange.emit(true);
        this.snackBar.open(
          `Successfully registered for ${this.event.name}!`,
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
    this.eventService.unregisterForEvent(this.event.id!).subscribe({
      next: () => {
        this.registrationChange.emit(true);
        this.snackBar.open(
          `Successfully unregistered for ${this.event.name}!`,
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
