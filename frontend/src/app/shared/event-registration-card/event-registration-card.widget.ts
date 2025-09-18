/**
 * The Event Registration Card displays details for registrations to
 * events that the user has.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { Component, Input } from '@angular/core';
import { EventOverview } from 'src/app/event/event.model';
import { EventService } from 'src/app/event/event.service';

@Component({
    selector: 'event-registration-card',
    templateUrl: './event-registration-card.widget.html',
    styleUrl: './event-registration-card.widget.css',
    standalone: false
})
export class EventRegistrationCardWidget {
  @Input() event!: EventOverview;

  constructor(protected eventService: EventService) {}
}
