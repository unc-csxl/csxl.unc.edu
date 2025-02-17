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
  shownEvent = 0;

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['events']) {
      this.shownEvent = 0;
    }
  }

  nextEvent() {
    this.shownEvent = (this.shownEvent + 1) % this.events.length;
  }
}
