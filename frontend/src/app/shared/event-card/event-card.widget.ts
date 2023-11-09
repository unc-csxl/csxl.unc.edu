/**
 * The Event Card widget abstracts the implementation of each
 * individual event card from the whole event page.
 *
 * @author Ajay Gandecha
 * @copyright 2023
 * @license MIT
 */

import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Event } from 'src/app/event/event.model';

@Component({
  selector: 'event-card',
  templateUrl: './event-card.widget.html',
  styleUrls: ['./event-card.widget.css']
})
export class EventCard {
  /** The event for the event card to display */
  @Input() event!: Event;

  /** Whether to disable the tile link or not */
  @Input() disableLink!: Boolean;

  /** Whether or not the current card is selected */
  @Input() selected: Boolean = false;

  /** Provides the event to a handler for the on click action */
  @Output() clicked = new EventEmitter<Event>();

  constructor() {}

  /** Handler for when the event card is pressed */
  cardClicked() {
    if (this.disableLink) {
      this.clicked.emit(this.event);
    }
  }
}
