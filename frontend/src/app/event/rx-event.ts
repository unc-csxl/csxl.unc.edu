/**
 * The RxEvent object is used to ensure proper updating and
 * retrieval of the list of all events in the database.
 *
 * @author Ben Goulet
 * @copyright 2024
 * @license MIT
 */

import { RxObject } from '../rx-object';
import { Event } from './event.model';

export class RxEvent extends RxObject<Event[]> {
  pushEvent(event: Event): void {
    this.value.push(event);
    this.notify();
  }

  updateEvent(event: Event): void {
    this.value = this.value.map((o) => {
      return o.id !== event.id ? o : event;
    });
    this.notify();
  }
}
