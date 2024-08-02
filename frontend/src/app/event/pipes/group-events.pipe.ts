/**
 * This is the pipe used to group events in a page by day.
 * @author Ajay Gandecha
 * @copyright 2024
 * @license MIT
 */

import { DatePipe } from '@angular/common';
import { Pipe, PipeTransform, inject } from '@angular/core';
import { EventOverview } from '../event.model';

@Pipe({
  name: 'groupEvents'
})
export class GroupEventsPipe implements PipeTransform {
  datePipe = inject(DatePipe);

  transform(events: EventOverview[]): [string, EventOverview[]][] {
    // Initialize an empty map
    let groups: Map<string, EventOverview[]> = new Map();

    // Transform the list of events based on the event filter pipe and query
    events.forEach((event) => {
      // Find the date to group by
      let dateString =
        this.datePipe.transform(event.start, 'EEEE, MMMM d, y') ?? '';
      // Add the event
      let newEventsList = groups.get(dateString) ?? [];
      newEventsList.push(event);
      groups.set(dateString, newEventsList);
    });

    // Return the groups
    return [...groups.entries()];
  }
}
