/**
 * Office hours page that shows events.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { DialogRef } from '@angular/cdk/dialog';
import { Component, WritableSignal, signal } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { PageEvent } from '@angular/material/paginator';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ActivatedRoute } from '@angular/router';
import { DeleteRecurringEventDialog } from 'src/app/my-courses/dialogs/delete-recurring-event/delete-recurring-event.dialog';
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

  courseSiteId: string;

  constructor(
    private route: ActivatedRoute,
    protected myCoursesService: MyCoursesService,
    private snackBar: MatSnackBar,
    protected dialog: MatDialog
  ) {
    // Load information from the parent route
    this.courseSiteId = this.route.parent!.snapshot.params['course_site_id'];

    // Load office hour data
    this.myCoursesService
      .getCurrentOfficeHourEvents(this.courseSiteId)
      .subscribe((overview) => {
        this.currentOfficeHourEvents.set(overview);
      });

    // Load paginated future office hours data
    this.futureOfficeHourEventsPaginator =
      new Paginator<OfficeHourEventOverview>(
        `/api/my-courses/${this.courseSiteId}/oh-events/future`
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
      `/api/my-courses/${this.courseSiteId}/oh-events/history`
    );

    this.pastOfficeHourEventsPaginator
      .loadPage<OfficeHourEventOverviewJson>(
        this.previousPastOfficeHourEventParams,
        parseOfficeHourEventOverviewJson
      )
      .subscribe((page) => {
        this.pastOfficeHourEventsPage.set(page);
      });

    // This subscription loads whether or not the user is a student in the course, and
    // hides the Actions columns if so. This is a hack to get around requirements for
    // Angular tables, and should be revisited in the future.
    this.myCoursesService.getTermOverviews().subscribe((terms) => {
      const courseSite = terms
        .flatMap((term) => term.sites)
        .find((site) => site.id == +this.courseSiteId);
      if (courseSite?.role !== 'Student') {
        this.futureOhDisplayedColumns = ['date', 'type', 'actions'];
      }
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

  deleteOfficeHours(officeHours: OfficeHourEventOverview) {
    if (officeHours.recurrence_id) {
      // Options for deleting recurring evnets
      let dialogRef = this.dialog.open(DeleteRecurringEventDialog, {
        height: '230px',
        width: '300px',
        data: { siteId: this.courseSiteId, officeHours }
      });
      dialogRef.afterClosed().subscribe(() => {
        this.futureOfficeHourEventsPaginator
          .loadPage<OfficeHourEventOverviewJson>(
            this.previousFutureOfficeHourEventParams,
            parseOfficeHourEventOverviewJson
          )
          .subscribe((page) => {
            this.futureOfficeHourEventsPage.set(page);
          });
      });
    } else {
      let confirmDelete = this.snackBar.open(
        'Are you sure you want to delete this office hours event?',
        'Delete',
        { duration: 15000 }
      );
      confirmDelete.onAction().subscribe(() => {
        this.myCoursesService
          .deleteOfficeHours(+this.courseSiteId, officeHours.id)
          .subscribe(() => {
            this.futureOfficeHourEventsPaginator
              .loadPage<OfficeHourEventOverviewJson>(
                this.previousFutureOfficeHourEventParams,
                parseOfficeHourEventOverviewJson
              )
              .subscribe((page) => {
                this.futureOfficeHourEventsPage.set(page);
              });
            this.snackBar.open('The office hours has been deleted.', '', {
              duration: 2000
            });
          });
      });
    }
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
