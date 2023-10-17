/**
 * The Event Page Component serves as a hub for students to browse all of the 
 * events hosted by CS Organizations at UNC.
 * 
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { Component, HostListener } from '@angular/core';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { eventResolver } from '../event.resolver';
import { ActivatedRoute } from '@angular/router';
import { Profile } from 'src/app/profile/profile.service';
import { Event } from '../event.service';
import { DatePipe } from '@angular/common';
import { EventFilterPipe } from '../event-filter/event-filter.pipe';

@Component({
  selector: 'app-event-page',
  templateUrl: './event-page.component.html',
  styleUrls: ['./event-page.component.css']
})
export class EventPageComponent {

  /** Route information to be used in App Routing Module */
  public static Route = {
    path: '',
    title: 'Events',
    component: EventPageComponent,
    canActivate: [],
    resolve: { profile: profileResolver, events: eventResolver }
  }

  /** Store the content of the search bar */
  public searchBarQuery = "";

  /** Store list of Events */
  public events: Event[];

  /** Store a map of days to a list of events for that day */
  public eventsPerDay: Map<string, Event[]> = new Map();

  /** Store the selected Event */
  public selectedEvent: Event | null = null;

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;

  /** Stores the width of the window. */
  public innerWidth: any;

  /** Constructor for the events page. */
  constructor(
    private route: ActivatedRoute,
    public datePipe: DatePipe,
    public eventFilterPipe: EventFilterPipe  
  ) {

    // Initialize data from resolvers
    const data = this.route.snapshot.data as { profile: Profile, events: Event[] };
    this.profile = data.profile;
    this.events = data.events;

    // Group events by their dates
    this.groupEventsByDate(this.events);

    // Initialize the initially selected event
    if(data.events.length > 0) {
      this.selectedEvent = data.events[0]
    }

  }

  /** Runs when the frontend UI loads */
  ngOnInit() {
      // Keep track of the initial width of the browser window
      this.innerWidth = window.innerWidth;
  }

  /** Handler that runs when the window resizes */
  @HostListener('window:resize', ['$event'])
  onResize(_: UIEvent) {
    // Update the browser window width
    this.innerWidth = window.innerWidth;
  }

  /** Helper function to group a list of events by date,
   * filtered based on the input query string.
   * @param events: List of the input events
   * @param query: Search bar query to filter the items
   */
  groupEventsByDate(events: Event[], query: string = "") {
    // Initialize an empty map
    let groups: Map<string, Event[]> = new Map();

    // Transform the list of events based on the event filter pipe and query
    this.eventFilterPipe.transform(events, query).forEach((event) => {
      // Find the date to group by
      let dateString = this.datePipe.transform(event.time, 'EEEE, MMMM d, y') ?? ""
      // Add the event
      let newEventsList = groups.get(dateString) ?? []
      newEventsList.push(event)
      groups.set(dateString, newEventsList)
    })
    
    // Update the data
    this.eventsPerDay = groups;
  }

  /** Handler that runs when the search bar query changes.
   * @param query: Search bar query to filter the items
   */
  onSearchBarQueryChange(query: string) {
      this.groupEventsByDate(this.events, query)
  }

  /** Handler that runs when an event card is clicked.
   * This function selects the event to display on the sidebar.
   * @param event: Event pressed
   */
  onEventCardClicked(event: Event) {
    this.selectedEvent = event
  }
}
