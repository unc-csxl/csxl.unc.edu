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
  OnInit,
  Signal,
  signal,
  effect,
  WritableSignal,
  computed
} from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { Profile, ProfileService } from 'src/app/profile/profile.service';
import { Event } from '../event.model';
import { DatePipe } from '@angular/common';

import { Paginated, TimeRangePaginationParams } from 'src/app/pagination';
import { NewEventService } from '../new-event.service';
import { GroupEventsPipe } from '../pipes/group-events.pipe';

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
    canActivate: []
  };

  /** Stores a reactive event pagination page. */
  public page: WritableSignal<
    Paginated<Event, TimeRangePaginationParams> | undefined
  > = signal(undefined);

  /** Stores a reactive mapping of days to events on the active page. */
  protected eventsByDate: Signal<[string, Event[]][]> = computed(() => {
    return this.groupEventsPipe.transform(this.page()?.items ?? []);
  });

  /** Stores reactive date signals for the bounds of pagination. */
  public startDate: Date = new Date();
  public endDate: Date = new Date(
    new Date().setMonth(new Date().getMonth() + 1)
  );

  /** Store the content of the search bar */
  public searchBarQuery = '';

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;

  /** Constructor for the events page. */
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    public datePipe: DatePipe,
    public eventService: NewEventService,
    private profileService: ProfileService,
    protected groupEventsPipe: GroupEventsPipe
  ) {
    this.profile = this.profileService.profile()!;
    this.eventService
      .getEvents({
        order_by: 'time',
        ascending: 'true',
        filter: '',
        range_start: new Date().toLocaleString('en-GB'),
        range_end: new Date(
          new Date().setMonth(new Date().getMonth() + 1)
        ).toLocaleString('en-GB')
      } as TimeRangePaginationParams)
      .subscribe((events) => {
        this.page.set(events);
      });
  }

  /** Runs when the frontend UI loads */
  ngOnInit() {
    // Subscribe to the active route's query parameters, and update the
    // internal start date and end date signals when these parameters
    // change in the route.
    //
    // This will trigger the `paginationTimeRangeEffect` effect and reload
    // the event pagination data.
    this.route.queryParams.subscribe((params: Params): void => {
      let newStartDate = params['start_date']
        ? new Date(Date.parse(params['start_date']))
        : new Date();
      let newEndDate = params['end_date']
        ? new Date(Date.parse(params['end_date']))
        : new Date(new Date().setMonth(new Date().getMonth() + 1));

      if (this.startDate !== newStartDate || this.endDate !== newEndDate) {
        this.reloadQueryParams(newStartDate, newEndDate);
      }
    });
  }

  /** Effect that refreshes the event pagination when the time range changes. */
  // paginationTimeRangeEffect = effect(() => {
  //   let params = this.page()!.params;
  //   params.range_start = this.startDate.toLocaleString('en-GB');
  //   params.range_end = this.endDate.toLocaleString('en-GB');
  //   this.eventService.getEvents(params);
  // });

  /** Reloads the page and its query parameters to adjust to the next month. */
  nextPage() {
    let newStart = new Date(
      this.startDate.setMonth(this.startDate.getMonth() + 1)
    );
    let newEnd = new Date(this.endDate.setMonth(this.endDate.getMonth() + 1));
    this.reloadQueryParams(newStart, newEnd);
  }

  /** Reloads the page and its query parameters to adjust to the previous month. */
  previousPage() {
    let newStart = new Date(
      this.startDate.setMonth(this.startDate.getMonth() - 1)
    );
    let newEnd = new Date(this.endDate.setMonth(this.endDate.getMonth() - 1));
    this.reloadQueryParams(newStart, newEnd);
  }

  /**
   * Reloads the page to update the query parameters and reload the data.
   * This is required so that the correct query parameters are reflected in the
   * browser's URL field.
   * @param startDate: The new start date
   * @param endDate: The new end date
   */
  reloadQueryParams(startDate: Date, endDate: Date) {
    this.router.navigate([], {
      relativeTo: this.route,
      queryParams: {
        start_date: startDate.toISOString(),
        end_date: endDate.toISOString()
      },
      queryParamsHandling: 'merge'
    });

    let newParams = this.page()!.params;
    newParams.range_start = startDate.toISOString();
    newParams.range_end = startDate.toISOString();

    this.eventService.getEvents(newParams).subscribe((events) => {
      this.page.set(events);
    });
  }

  // TODO: Refactor this method to remove manual +/- 100 year range on query filtering.

  /** Handler that runs when the search bar query changes.
   * @param query: Search bar query to filter the items
   */
  onSearchBarQueryChange(query: string) {
    let newParams = this.page()!.params;
    if (query == '') {
      newParams.range_start = this.startDate.toLocaleString('en-GB');
      newParams.range_end = this.endDate.toLocaleString('en-GB');
    } else {
      newParams.range_start = new Date(
        new Date().setFullYear(new Date().getFullYear() - 100)
      ).toLocaleString('en-GB');
      newParams.range_end = new Date(
        new Date().setFullYear(new Date().getFullYear() + 100)
      ).toLocaleString('en-GB');
      newParams.filter = query;
    }

    this.eventService.getEvents(newParams);
  }
}
