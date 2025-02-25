/**
 * The Event Card displays details for the most recent events on the CSXL TV.
 *
 * @author Will Zahrt <wzahrt@unc.edu>
 * @author Andrew Lockard <andrew.lockard15@gmail.com>
 * @copyright 2024
 * @license MIT
 */

import { Component, effect, input } from '@angular/core';
import { EventOverview } from '../../../event/event.model';

@Component({
  selector: 'event-card',
  templateUrl: './event-card.widget.html',
  styleUrl: './event-card.widget.css'
})
export class EventCardWidget {
  events = input<EventOverview[]>([]);
  shownEvent = 0;

  constructor() {
    effect(() => {
      /**
       * Reset shown event when events change
       * This prevents edge case where events changes to be shorter and the
       * shown event index is now longer than the new length of events
       */
      this.events();
      this.shownEvent = 0;
    });
  }

  nextEvent() {
    this.shownEvent = (this.shownEvent + 1) % this.events().length;
  }
}
