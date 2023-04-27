import { Pipe, PipeTransform } from '@angular/core';
import { Observable } from 'rxjs';
import { Event } from '../models.module';
import { map } from 'rxjs/operators';

@Pipe({
  name: 'eventsFilter'
})
export class EventsFilterPipe implements PipeTransform {

  /** Returns a mapped array of events that are filtered 
   * @param {Observable<Event[]>} events: observable list of valid Event models
   * @param {string} searchQuery: input string to filter by
   * @returns {Observable<EventS[]>}
   */
  transform = (events: Observable<Event[]>, searchQuery: string, start: Date | null | undefined, end: Date | null | undefined, organizations: String[] | null) => {
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
      if(organizations.length > 0) {
        events = events.pipe(
          map(events => events
            .filter(event => 
              organizations.indexOf(event.organization.name) != -1
            )
          )
        )
      }
    }
    // Return the filtered events list
    return events;
  }

}
