/**
 * The Office Hour Event widget defines the UI card for
 * an office hour event.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { Component, Input } from '@angular/core';
import { OfficeHourEventOverview } from '../../../../my-courses.model';

@Component({
  selector: 'office-hour-event-card',
  templateUrl: './office-hour-event-card.widget.html',
  styleUrls: ['./office-hour-event-card.widget.scss']
})
export class OfficeHourEventCardWidget {
  /** The event to show */
  @Input() event!: OfficeHourEventOverview;

  constructor() {}
}
