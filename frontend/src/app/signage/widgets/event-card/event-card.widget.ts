/**
 * The Event Card displays details for the most recent events on the CSXL TV.
 *
 * @author Will Zahrt <wzahrt@unc.edu>
 * @author Andrew Lockard <andrew.lockard15@gmail.com>
 * @copyright 2024
 * @license MIT
 */

import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { EventOverview } from '../../../event/event.model';

@Component({
  selector: 'event-card',
  templateUrl: './event-card.widget.html',
  styleUrl: './event-card.widget.css'
})
export class EventCardWidget implements OnChanges {
  @Input() events!: EventOverview[];
  shown_event = 0;

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['events']) {
      this.shown_event = 0;
    }
  }

  next_event() {
    this.shown_event = (this.shown_event + 1) % this.events.length;
  }
}
