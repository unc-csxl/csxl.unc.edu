/** Creates a filter pipe for events based on date. */

import { Pipe, PipeTransform } from '@angular/core';
import { EventSummary, Profile } from '../models.module';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Pipe({
  name: 'eventFilter'
})
export class EventFilterPipe implements PipeTransform {

  /** Returns a filtered array of events based on the past/current query input. 
   * @param {EventSummary[]} events: list of valid EventSummary models
   * @param {String} input: input string to filter by (past/current)
   * @returns {EventSummary[]}
   */
  transform = (events: EventSummary[], subject: Profile, input: String) => {
    // Sort the events list by date
    events = events.sort(
      (a: EventSummary, b: EventSummary) => a.time < b.time ? -1 : a.time > b.time ? 1 : 0
    );

    // Filter out events that should not be visible to the user
    if (subject) {
      // User authenticated, so show public events and private events
      // for organizations they are apart of
      events = events.filter((event) => {
        // Determine if the user is a member of the organization
        let rolesForEventOrg = subject.organization_associations.filter((org_role) => org_role.org_id == event.org_id)
        let isUserMember = (rolesForEventOrg.length > 0) && rolesForEventOrg[0].membership_type >= 0
        // Determine if event should be shown
        return event.public || isUserMember
      })
    }
    else {
      // User not authenticated, so only show public events
      events = events.filter((event) => event.public)
    }

    // If input is 'past', filter for events that have a Date less than the current Date.
    if (input === "past") {
      return events.filter(val => new Date(val.time) < new Date());
    } else if (input === "current") {
      // If input is 'current', filter for events that have a Date greater than or equal to 
      // the current Date.
      return events.filter(val => new Date(val.time) >= new Date());
    } else {
      // Otherwise, return the original list.
      return events;
    }
  }
}
