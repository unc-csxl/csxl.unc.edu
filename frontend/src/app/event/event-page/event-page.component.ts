/**
 * The Event Page Component serves as a hub for students to browse all of the
 * events hosted by CS Organizations at UNC.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import {
  Component,
  HostListener,
  OnInit,
  inject,
  OnDestroy
} from '@angular/core';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { ActivatedRoute, ActivationEnd, Params, Router } from '@angular/router';
import { Profile } from 'src/app/profile/profile.service';
import { Event } from '../event.model';
import { DatePipe } from '@angular/common';
import { EventService } from '../event.service';

import { PaginatedEvent } from 'src/app/pagination';
import {
  Subject,
  Subscription,
  debounceTime,
  distinctUntilChanged,
  filter,
  tap
} from 'rxjs';

@Component({
  selector: 'app-event-page',
  templateUrl: './event-page.component.html',
  styleUrls: ['./event-page.component.css']
})
export class EventPageComponent implements OnInit, OnDestroy {
  public page: PaginatedEvent<Event>;
  public startDate = new Date();
  public endDate = new Date(new Date().setMonth(new Date().getMonth() + 1));
  public today: boolean = true;

  private static EventPaginationParams = {
    order_by: 'time',
    ascending: 'true',
    filter: '',
    range_start: new Date().toLocaleString('en-GB'),
    range_end: new Date(
      new Date().setMonth(new Date().getMonth() + 1)
    ).toLocaleString('en-GB')
  };

  /** Route information to be used in App Routing Module */
  public static Route = {
    path: '',
    title: 'Events',
    component: EventPageComponent,
    canActivate: [],
    resolve: {
      profile: profileResolver,
      page: () =>
        inject(EventService).list(EventPageComponent.EventPaginationParams)
    }
  };

  /** Store the content of the search bar */
  public searchBarQuery = '';

  /** Store a map of days to a list of events for that day */
  public eventsPerDay: [string, Event[]][];

  /** Store the selected Event */
  public selectedEvent: Event | null = null;

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;

  /** Stores the width of the window. */
  public innerWidth: any;

  public query: string = '';

  public searchUpdate = new Subject<string>();

  private routeSubscription!: Subscription;

  /** Constructor for the events page. */
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    public datePipe: DatePipe,
    public eventService: EventService
  ) {
    // Initialize data from resolvers
    const data = this.route.snapshot.data as {
      profile: Profile;
      page: PaginatedEvent<Event>;
    };
    this.profile = data.profile;
    this.page = data.page;
    this.today =
      this.startDate.setHours(0, 0, 0, 0) == new Date().setHours(0, 0, 0, 0);

    // Group events by their dates
    this.eventsPerDay = eventService.groupEventsByDate(this.page.items);

    // Initialize the initially selected event
    if (data.page.items.length > 0) {
      this.selectedEvent = this.page.items[0];
    }

    this.searchUpdate
      .pipe(
        filter((search: string) => search.length > 2 || search.length == 0),
        debounceTime(500),
        distinctUntilChanged()
      )
      .subscribe((query) => {
        this.onSearchBarQueryChange(query);
      });
  }

  /** Runs when the frontend UI loads */
  ngOnInit() {
    // Keep track of the initial width of the browser window
    this.innerWidth = window.innerWidth;

    // Watch current route's query params
    this.route.queryParams.subscribe((params: Params): void => {
      this.startDate = params['start_date']
        ? new Date(Date.parse(params['start_date']))
        : new Date();
      this.endDate = params['end_date']
        ? new Date(Date.parse(params['end_date']))
        : new Date(new Date().setMonth(new Date().getMonth() + 1));
    });

    const today = new Date();
    if (this.startDate.getTime() < today.setHours(0, 0, 0, 0)) {
      this.page.params.ascending = 'false';
    }

    let paginationParams = this.page.params;
    paginationParams.range_start = this.startDate.toLocaleString('en-GB');
    paginationParams.range_end = this.endDate.toLocaleString('en-GB');
    this.eventService.list(paginationParams).subscribe((page) => {
      this.eventsPerDay = this.eventService.groupEventsByDate(page.items);
    });

    let prevUrl = '';
    this.routeSubscription = this.router.events
      .pipe(
        filter((e) => e instanceof ActivationEnd),
        distinctUntilChanged(() => this.router.url === prevUrl),
        tap(() => (prevUrl = this.router.url))
      )
      .subscribe((_) => {
        this.page.params.ascending = (
          this.startDate.getTime() > today.setHours(0, 0, 0, 0)
        ).toString();
        let paginationParams = this.page.params;
        paginationParams.range_start = this.startDate.toLocaleString('en-GB');
        paginationParams.range_end = this.endDate.toLocaleString('en-GB');
        this.eventService.list(paginationParams).subscribe((page) => {
          this.eventsPerDay = this.eventService.groupEventsByDate(page.items);
        });
      });
  }

  ngOnDestroy() {
    this.routeSubscription.unsubscribe();
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
    this.query = query;
    let paginationParams = this.page.params;
    paginationParams.ascending = 'true';
    if (query == '') {
      paginationParams.range_start = this.startDate.toLocaleString('en-US');
      paginationParams.range_end = this.endDate.toLocaleString('en-US');
    } else {
      paginationParams.range_start = new Date(
        new Date().setFullYear(new Date().getFullYear() - 100)
      ).toLocaleString('en-US');
      paginationParams.range_end = new Date(
        new Date().setFullYear(new Date().getFullYear() + 100)
      ).toLocaleString('en-US');
      paginationParams.filter = this.query;
    }
    this.eventService.list(paginationParams).subscribe((page) => {
      this.eventsPerDay = this.eventService.groupEventsByDate(page.items);
      paginationParams.filter = '';
    });
  }

  /** Handler that runs when an event card is clicked.
   * This function selects the event to display on the sidebar.
   * @param event: Event pressed
   */
  onEventCardClicked(event: Event) {
    this.selectedEvent = event;
  }

  showEvents(isPrevious: boolean) {
    //let paginationParams = this.page.params;
    this.startDate = isPrevious
      ? new Date(this.startDate.setMonth(this.startDate.getMonth() - 1))
      : new Date(this.startDate.setMonth(this.startDate.getMonth() + 1));
    this.endDate = isPrevious
      ? new Date(this.endDate.setMonth(this.endDate.getMonth() - 1))
      : new Date(this.endDate.setMonth(this.endDate.getMonth() + 1));
    if (isPrevious === true) {
      this.page.params.ascending = 'false';
    }
    this.today =
      this.startDate.setHours(0, 0, 0, 0) == new Date().setHours(0, 0, 0, 0);
    this.router.navigate([], {
      relativeTo: this.route,
      queryParams: {
        start_date: this.startDate.toISOString(),
        end_date: this.endDate.toISOString()
      },
      queryParamsHandling: 'merge'
    });
  }
}
