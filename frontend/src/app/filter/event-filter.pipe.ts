/** Creates a filter pipe for events based on date. */

import { Pipe, PipeTransform } from '@angular/core';
import { EventSummary } from '../models.module';

@Pipe({
  name: 'eventFilter'
})
export class EventFilterPipe implements PipeTransform {

    /** Returns a filtered array of events based on the past/current query input. 
   * @param {EventSummary[]} events: list of valid EventSummary models
   * @param {String} input: input string to filter by (past/current)
   * @returns {EventSummary[]}
  */
  transform(value: EventSummary[], input: String): any {
    // If input is 'past', filter for events that have a Date less than the current Date.
    if (input === "past") {
      return value.filter(val => new Date(val.time) < new Date());
    } else if (input === "current") {
      // If input is 'current', filter for events that have a Date greater than or equal to 
      // the current Date.
      return value.filter(val => new Date(val.time) >= new Date());
    } else {
      // Otherwise, return the original list.
      return value;
    }
  }
}
