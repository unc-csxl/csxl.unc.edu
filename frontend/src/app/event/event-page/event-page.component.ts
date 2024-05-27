/**
 * The Event Page Component serves as a hub for students to browse all of the
 * events hosted by CS Organizations at UNC.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2024
 * @license MIT
 */

import {
  Component,
  Signal,
  signal,
  effect,
  WritableSignal,
  computed
} from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Profile, ProfileService } from 'src/app/profile/profile.service';
import { Event } from '../event.model';
import { DatePipe } from '@angular/common';

import {
  DEFAULT_TIME_RANGE_PARAMS,
  Paginated,
  TimeRangePaginationParams
} from 'src/app/pagination';
import { EventService } from '../event.service';
import { GroupEventsPipe } from '../pipes/group-events.pipe';

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
    canActivate: []
  };

  /** Stores a reactive event pagination page. */
  public page: WritableSignal<
    Paginated<Event, TimeRangePaginationParams> | undefined
  > = signal(undefined);
  private previousParams: TimeRangePaginationParams = DEFAULT_TIME_RANGE_PARAMS;

  /** Stores a reactive mapping of days to events on the active page. */
  protected eventsByDate: Signal<[string, Event[]][]> = computed(() => {
    return this.groupEventsPipe.transform(this.page()?.items ?? []);
  });

  /** Stores reactive date signals for the bounds of pagination. */
  public startDate: WritableSignal<Date> = signal(new Date());
  public endDate: WritableSignal<Date> = signal(
    new Date(new Date().setMonth(new Date().getMonth() + 1))
  );
  public filterQuery: WritableSignal<string> = signal('');

  /** Store the content of the search bar */
  public searchBarQuery = '';

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;

  /** Constructor for the events page. */
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    public datePipe: DatePipe,
    public eventService: EventService,
    private profileService: ProfileService,
    protected groupEventsPipe: GroupEventsPipe
  ) {
    this.profile = this.profileService.profile()!;
  }

  /**
   * Effect that refreshes the event pagination when the time range changes. This effect
   * is also called when the page initially loads.
   *
   * This effect also reloads the query parameters in the URL so that the URL in the
   * browser reflects the newly changed start and end date ranges.
   */
  paginationTimeRangeEffect = effect(() => {
    // Update the parameters with the new date range
    let params = this.previousParams;
    params.range_start = this.startDate().toLocaleString('en-GB');
    params.range_end = this.endDate().toLocaleString('en-GB');
    params.filter = this.filterQuery();
    // Refresh the data
    this.eventService.getEvents(params).subscribe((events) => {
      this.page.set(events);
      this.previousParams = events.params;
      this.reloadQueryParams();
    });
  });

  /** Reloads the page and its query parameters to adjust to the next month. */
  nextPage() {
    this.startDate.set(
      new Date(this.startDate().setMonth(this.startDate().getMonth() + 1))
    );
    this.endDate.set(
      new Date(this.endDate().setMonth(this.endDate().getMonth() + 1))
    );
  }

  /** Reloads the page and its query parameters to adjust to the previous month. */
  previousPage() {
    this.startDate.set(
      new Date(this.startDate().setMonth(this.startDate().getMonth() - 1))
    );
    this.endDate.set(
      new Date(this.endDate().setMonth(this.endDate().getMonth() - 1))
    );
  }

  /**
   * Reloads the page to update the query parameters and reload the data.
   * This is required so that the correct query parameters are reflected in the
   * browser's URL field.
   * @param startDate: The new start date
   * @param endDate: The new end date
   */
  reloadQueryParams() {
    this.router.navigate([], {
      relativeTo: this.route,
      queryParams: {
        start_date: this.startDate().toISOString(),
        end_date: this.endDate().toISOString()
      },
      queryParamsHandling: 'merge'
    });
  }

  // TODO: Refactor this method to remove manual +/- 100 year range on query filtering.

  /** Handler that runs when the search bar query changes.
   * @param query: Search bar query to filter the items
   */
  onSearchBarQueryChange(query: string) {
    if (query === '') {
      this.startDate.set(new Date());
      this.endDate.set(
        new Date(new Date().setMonth(new Date().getMonth() + 1))
      );
    } else {
      this.startDate.set(
        new Date(new Date().setMonth(new Date().getFullYear() - 100))
      );
      this.endDate.set(
        new Date(new Date().setMonth(new Date().getFullYear() + 100))
      );
    }
    this.filterQuery.set(query);
  }
}
