import { Component, WritableSignal, signal } from '@angular/core';
import { PageEvent } from '@angular/material/paginator';
import { ActivatedRoute } from '@angular/router';
import {
  OfficeHourEventOverview,
  OfficeHourEventOverviewJson,
  parseOfficeHourEventOverviewJson
} from 'src/app/my-courses/my-courses.model';
import { MyCoursesService } from 'src/app/my-courses/my-courses.service';
import {
  DEFAULT_PAGINATION_PARAMS,
  Paginated,
  PaginationParams,
  Paginator
} from 'src/app/pagination';

@Component({
  selector: 'app-course-office-hours-page',
  templateUrl: './office-hours-page.component.html',
  styleUrl: './office-hours-page.component.css'
})
export class OfficeHoursPageComponent {
  /** Route information to be used in the routing module */
  public static Route = {
    path: 'office-hours',
    title: 'Course',
    component: OfficeHoursPageComponent
  };

  /** Stores the view state enum and view state. */
  ViewState = OfficeHoursPageComponent.ViewState;
  viewState = OfficeHoursPageComponent.ViewState.Scheduled;

  /** Signal to store the reactive office hour overview information */
  currentOfficeHourEvents: WritableSignal<OfficeHourEventOverview[]> = signal(
    []
  );

  /** Encapsulated future events paginator and params */
  private futureOfficeHourEventsPaginator: Paginator<OfficeHourEventOverview>;
  futureOfficeHourEventsPage: WritableSignal<
    Paginated<OfficeHourEventOverview, PaginationParams> | undefined
  > = signal(undefined);
  private previousFutureOfficeHourEventParams: PaginationParams =
    DEFAULT_PAGINATION_PARAMS;

  public futureOhDisplayedColumns: string[] = ['date', 'type'];

  /** Encapsulated past events paginator and params */
  private pastOfficeHourEventsPaginator: Paginator<OfficeHourEventOverview>;
  pastOfficeHourEventsPage: WritableSignal<
    Paginated<OfficeHourEventOverview, PaginationParams> | undefined
  > = signal(undefined);
  private previousPastOfficeHourEventParams: PaginationParams =
    DEFAULT_PAGINATION_PARAMS;

  public pastOhDisplayedColumns: string[] = ['date', 'type'];

  constructor(
    private route: ActivatedRoute,
    protected myCoursesService: MyCoursesService
  ) {
    // Load information from the parent route
    let termId = this.route.parent!.snapshot.params['term_id'];
    let courseId = this.route.parent!.snapshot.params['course_id'];

    // Load office hour data
    this.myCoursesService
      .getCurrentOfficeHourEvents(termId, courseId)
      .subscribe((overview) => {
        this.currentOfficeHourEvents.set(overview);
      });

    // Load paginated future office hours data
    this.futureOfficeHourEventsPaginator =
      new Paginator<OfficeHourEventOverview>(
        `/api/academics/my-courses/${termId}/${courseId}/oh-events/future`
      );

    this.futureOfficeHourEventsPaginator
      .loadPage<OfficeHourEventOverviewJson>(
        this.previousFutureOfficeHourEventParams,
        parseOfficeHourEventOverviewJson
      )
      .subscribe((page) => {
        this.futureOfficeHourEventsPage.set(page);
      });

    // Load paginated past office hours data
    this.pastOfficeHourEventsPaginator = new Paginator<OfficeHourEventOverview>(
      `/api/academics/my-courses/${termId}/${courseId}/oh-events/history`
    );

    this.pastOfficeHourEventsPaginator
      .loadPage<OfficeHourEventOverviewJson>(
        this.previousPastOfficeHourEventParams,
        parseOfficeHourEventOverviewJson
      )
      .subscribe((page) => {
        this.pastOfficeHourEventsPage.set(page);
      });
  }

  /** Handles a pagination event for the future office hours table */
  handleFutureOfficeHoursPageEvent(e: PageEvent) {
    let paginationParams = this.futureOfficeHourEventsPage()!.params;
    paginationParams.page = e.pageIndex;
    paginationParams.page_size = e.pageSize;
    this.futureOfficeHourEventsPaginator
      .loadPage<OfficeHourEventOverviewJson>(
        paginationParams,
        parseOfficeHourEventOverviewJson
      )
      .subscribe((page) => {
        this.futureOfficeHourEventsPage.set(page);
        this.previousFutureOfficeHourEventParams = paginationParams;
      });
  }

  /** Handles a pagination event for the past office hours table */
  handlePastOfficeHoursPageEvent(e: PageEvent) {
    let paginationParams = this.pastOfficeHourEventsPage()!.params;
    paginationParams.page = e.pageIndex;
    paginationParams.page_size = e.pageSize;
    this.pastOfficeHourEventsPaginator
      .loadPage<OfficeHourEventOverviewJson>(
        paginationParams,
        parseOfficeHourEventOverviewJson
      )
      .subscribe((page) => {
        this.pastOfficeHourEventsPage.set(page);
        this.previousPastOfficeHourEventParams = paginationParams;
      });
  }
}

export namespace OfficeHoursPageComponent {
  /** Enumeration for the view states */
  export enum ViewState {
    Scheduled,
    History,
    Data
  }
}
