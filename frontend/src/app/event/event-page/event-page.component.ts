import { Component, HostListener } from '@angular/core';
import { Organization } from 'src/app/organization/organization.service';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { eventResolver } from '../event.resolver';
import { ActivatedRoute } from '@angular/router';
import { Profile } from 'src/app/profile/profile.service';
import { Event } from '../event.service';
import { DatePipe } from '@angular/common';
import { EventFilterPipe } from '../event-filter/event-filter.pipe';
import { MatSnackBar } from '@angular/material/snack-bar';

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

  /** Store searchBarQuery */
  public searchBarQuery = "";

  /** Store Observable list of Events */
  public events: Event[];

  public eventsPerDay: Map<string, Event[]> = new Map();

  /** Store the selected Event */
  public selectedEvent: Event | null = null;

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;

  /** Stores the width of the window. */
  public innerWidth: any;

  constructor(
    private route: ActivatedRoute,
    public datePipe: DatePipe,
    public eventFilterPipe: EventFilterPipe  
  ) {

    // Initialize data from resolvers
    const data = this.route.snapshot.data as { profile: Profile, events: Event[] };
    this.profile = data.profile;
    this.events = data.events;

    this.groupEventsByDate(this.events);

    // Initialize the initially selected event
    if(data.events.length > 0) {
      this.selectedEvent = data.events[0]
    }

  }

  ngOnInit() {
      this.innerWidth = window.innerWidth;
  }

  @HostListener('window:resize', ['$event'])
  onResize(_: UIEvent) {
    this.innerWidth = window.innerWidth;
  }

  groupEventsByDate(events: Event[], query: string = "") {
    let groups: Map<string, Event[]> = new Map();
    this.eventFilterPipe.transform(events, query).forEach((event) => {
      let dateString = this.datePipe.transform(event.time, 'EEEE, MMMM d, y') ?? ""
      let newEventsList = groups.get(dateString) ?? []
      newEventsList.push(event)
      groups.set(dateString, newEventsList)
    })
    
    this.eventsPerDay = groups;
  }

  onSearchBarQueryChange(query: string) {
      this.groupEventsByDate(this.events, query)
  }

  onEventCardClicked(event: Event) {
    this.selectedEvent = event
  }
}

export interface EventDetailData {
  name: string;
  organization: Organization;
  startText: string;
  endText: string;
  location: string;
  description: string;
  requiresPreregistration: boolean;
}
