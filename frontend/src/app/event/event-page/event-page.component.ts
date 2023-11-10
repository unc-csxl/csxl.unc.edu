/**
 * The Event Page Component serves as a hub for students to browse all of the
 * events hosted by CS Organizations at UNC.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { Component, HostListener, OnInit } from '@angular/core';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { eventResolver } from '../event.resolver';
import { ActivatedRoute } from '@angular/router';
import { Profile } from 'src/app/profile/profile.service';
import { Event } from '../event.model';
import { DatePipe } from '@angular/common';
import { EventFilterPipe } from '../event-filter/event-filter.pipe';
import { EventService } from '../event.service';

@Component({
  selector: 'app-event-page',
  templateUrl: './event-page.component.html',
  styleUrls: ['./event-page.component.css']
})
export class EventPageComponent implements OnInit {
  /** Route information to be used in App Routing Module */
  public static Route = {
    path: '',
    title: 'Events',
    component: EventPageComponent,
    canActivate: [],
    resolve: { profile: profileResolver, events: eventResolver }
  };

  /** Store the content of the search bar */
  public searchBarQuery = '';

  /** Store list of Events */
  public events: Event[];

  /** Store a map of days to a list of events for that day */
  public eventsPerDay: [string, Event[]][];

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
    public eventFilterPipe: EventFilterPipe,
    public eventService: EventService
  ) {
    // Initialize data from resolvers
    const data = this.route.snapshot.data as {
      profile: Profile;
      events: Event[];
    };
    this.profile = data.profile;
    this.events = data.events;

    // Group events by their dates
    this.eventsPerDay = eventService.groupEventsByDate(this.events);

    // Initialize the initially selected event
    if (data.events.length > 0) {
      this.selectedEvent = eventFilterPipe.transform(data.events, "")[0];
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

  /** Handler that runs when the search bar query changes.
   * @param query: Search bar query to filter the items
   */
  onSearchBarQueryChange(query: string) {
    this.eventsPerDay = this.eventService.groupEventsByDate(this.events, query);
  }

  /** Handler that runs when an event card is clicked.
   * This function selects the event to display on the sidebar.
   * @param event: Event pressed
   */
  onEventCardClicked(event: Event) {
    this.selectedEvent = event;
  }
}
