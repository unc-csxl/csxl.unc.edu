/**
 * This is the pipe used to filter events on the events page.
 * 
 * @author Ajay Gandecha
 * @copyright 2023
 * @license MIT
 */

import { Pipe, PipeTransform } from '@angular/core';
import { Event } from '../event.model';

@Pipe({
  name: 'eventFilter'
})
export class EventFilterPipe implements PipeTransform {

  /** Returns a mapped array of events that start with the input string (if search query provided). 
   * @param {Observable<Event[]>} events: observable list of valid Event models
   * @param {String} searchQuery: input string to filter by
   * @returns {Observable<Event[]>}
   */
  transform(events: Event[], searchQuery: String): Event[] {
    // Sort the events list alphabetically by name
    events = events.sort((a: Event, b: Event) => {
      return a.name.toLowerCase().localeCompare(b.name.toLowerCase());
    })

    // Remove past events

    // If a search query is provided, return the events that start with the search query.
    if (searchQuery) {
      return events.filter(events =>
        events.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        events.organization!.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        events.description.toLowerCase().includes(searchQuery.toLowerCase()));
    } else {
      // Otherwise, return the original list.
      return events;
    }
  }

}