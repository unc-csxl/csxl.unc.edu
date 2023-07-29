/**
 * This pipe serves as the filter for the events page.
 * 
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { Pipe, PipeTransform } from '@angular/core';
import { Observable } from 'rxjs';
import { Event } from '../../models.module';
import { map } from 'rxjs/operators';
import { Profile } from '../../models.module';

@Pipe({
  name: 'eventsFilter'
})
export class EventsFilterPipe implements PipeTransform {

  /** Returns a mapped array of events that are filtered 
   * @param {Observable<Event[]>} events: observable list of valid Event models
   * @param {Profile} subject: user loading this page
   * @param {string} searchQuery: input string to filter by
   * @returns {Observable<EventS[]>}
   */
  transform = (events: Observable<Event[]>, subject: Profile, searchQuery: string, start: Date | null | undefined, end: Date | null | undefined, organizations: String[] | null) => {
    // Sort the events list by date
    events = events.pipe(
      map(events => events.sort((a: Event, b: Event) => a.time < b.time ? -1 : a.time > b.time ? 1 : 0))
    )

    // If a search query is provided, filter out the events that don't include that search query
    if (searchQuery) {
      events = events.pipe(
        map(events => events
          .filter(event =>
            event.name.toLowerCase().startsWith(searchQuery.toLowerCase()) ||
            event.description.toLowerCase().includes(searchQuery.toLowerCase())
          )
        )
      )
    }
    // If a start date is provided, filter out the events that are before start
    if (start) {
      events = events.pipe(
        map(events => events
          .filter(event =>
            new Date(event.time) >= new Date(start)
          )
        )
      )
    }
    // If an end date is provided, filter out the events that are after end
    if (end) {
      events = events.pipe(
        map(events => events
          .filter(event =>
            new Date(event.time) <= new Date(new Date(end).getTime() + 60 * 60 * 24 * 1000)
          )
        )
      )
    }
    // If the selected organizations list is provided and has a length greater than 0,
    // filter out the events whose host organizations are not on the list
    if (organizations) {
      if (organizations.length > 0) {
        events = events.pipe(
          map(events => events
            .filter(event =>
              organizations.indexOf(event.organization.name) != -1
            )
          )
        )
      }
    }

    // Filter out events that should not be visible to the user
    if (subject) {
      // User authenticated, so show public events and private events
      // for organizations they are apart of
      events = events.pipe(map(events => events.filter((event) => {
        // Determine if the user is a member of the organization
        let rolesForEventOrg = subject.organization_associations.filter((org_role) => org_role.org_id == event.org_id)
        let isUserMember = (rolesForEventOrg.length > 0) && rolesForEventOrg[0].membership_type >= 0
        // Determine if event should be shown
        return event.public || isUserMember
      })))
    }
    else {
      // User not authenticated, so only show public events
      events = events.pipe(map(events => events.filter((event) => event.public)))
    }


    // Return the filtered events list
    return events;
  }

}
