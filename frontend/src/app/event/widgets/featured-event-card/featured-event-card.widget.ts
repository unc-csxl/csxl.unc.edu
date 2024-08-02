/**
 * The Feature Event Card displays the featured event prominently on the page.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { Component, EventEmitter, Input, Output } from '@angular/core';
import { EventOverview, RegistrationType } from '../../event.model';
import { EventService } from '../../event.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Profile } from 'src/app/models.module';

@Component({
  selector: 'featured-event-card',
  templateUrl: './featured-event-card.widget.html',
  styleUrl: './featured-event-card.widget.css'
})
export class FeaturedEventCardWidget {
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
    if (this.event.override_registration_url) {
      window.location.href = this.event.override_registration_url!;
      return;
    }

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
