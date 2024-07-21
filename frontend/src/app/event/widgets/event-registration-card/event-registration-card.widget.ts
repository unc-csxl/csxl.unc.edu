/**
 * The Event Registration Card displays details for registrations to
 * events that the user has.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { Component, Input } from '@angular/core';
import { EventOverview } from '../../event.model';
import { EventService } from '../../event.service';

@Component({
  selector: 'event-registration-card',
  templateUrl: './event-registration-card.widget.html',
  styleUrl: './event-registration-card.widget.css'
})
export class EventRegistrationCardWidget {
  @Input() event!: EventOverview;

  constructor(protected eventService: EventService) {}
}
