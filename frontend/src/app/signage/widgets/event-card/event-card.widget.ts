/**
 * The Event Card displays details for events in the paginated list.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { Component, EventEmitter, Input, Output } from '@angular/core';
import { EventOverview, RegistrationType } from '../../../event/event.model';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Profile } from 'src/app/profile/profile.service';

@Component({
  selector: 'event-card',
  templateUrl: './event-card.widget.html',
  styleUrl: './event-card.widget.css'
})
export class EventCardWidget {
  @Input() profile: Profile | undefined;
  registrationType = RegistrationType;
  @Input() event!: EventOverview;

  now = new Date();

  constructor(protected snackBar: MatSnackBar) {}

  /** Registers a user for an event. */
}
