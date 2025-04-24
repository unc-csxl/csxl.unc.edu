/**
 * The Roster Component enables instructors to view the roster of their courses.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @author Jade Keegan
 * @copyright 2024
 * @license MIT
 */

import {
  Component,
  computed,
  effect,
  model,
  signal,
  Signal,
  WritableSignal
} from '@angular/core';
import {
  MatFilterChipFilterLogic,
  MatFilterChipSearchableItem
} from 'src/app/shared/mat/filter-chip/filter-chip.component';
import { MyCoursesService } from '../../my-courses.service';
import { ActivatedRoute, Router } from '@angular/router';
import {
  DefaultOfficeHourStatisticsPaginationParams,
  OfficeHourStatisticsFilterData,
  OfficeHourStatisticsPaginationParams,
  OfficeHoursTicketStatistics,
  OfficeHourTicketOverview
} from '../../my-courses.model';
import { PublicProfile } from 'src/app/profile/profile.service';
import { Paginated } from 'src/app/pagination';
import { PageEvent } from '@angular/material/paginator';
import { MatDialog } from '@angular/material/dialog';
import { TicketDetailsDialog } from '../../dialogs/ticket-details/ticket-details.dialog';
import saveAs from 'file-saver';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-statistics',
  templateUrl: './statistics.component.html',
  styleUrl: './statistics.component.css'
})
export class StatisticsComponent {
  /** Route information to be used in the routing module */
  public static Route = {
    path: 'statistics',
    title: 'Course',
    component: StatisticsComponent
  };

  /** Stores the ID for the course site. */
  courseSiteId: number;

  /** Stores the filter options for the filter chips on the UI. */
  filterOptions: WritableSignal<OfficeHourStatisticsFilterData | undefined> =
    signal(undefined);

  /** Student filter options for the filter dropdown based on the filter options. */
  studentFilterOptions: Signal<MatFilterChipSearchableItem<PublicProfile>[]> =
    computed(() => {
      return (
        this.filterOptions()?.students.map((student) => ({
          displayText: student.first_name + ' ' + student.last_name,
          item: student
        })) ?? []
      );
    });
  selectedStudentFilterOptions: WritableSignal<
    MatFilterChipSearchableItem<PublicProfile>[]
  > = signal([]);

  /** Staff filter options for the filter dropdown based on the filter options. */
  staffFilterOptions: Signal<MatFilterChipSearchableItem<PublicProfile>[]> =
    computed(() => {
      return (
        this.filterOptions()?.staff.map((staff) => ({
          displayText: staff.first_name + ' ' + staff.last_name,
          item: staff
        })) ?? []
      );
    });
  selectedStaffFilterOptions: WritableSignal<
    MatFilterChipSearchableItem<PublicProfile>[]
  > = signal([]);

  /** Logic for filtering profiles. */
  profileFilterLogic: MatFilterChipFilterLogic<PublicProfile> = (
    item,
    query
  ) => {
    return item.displayText.toLowerCase().includes(query.toLowerCase());
  };

  /** Filtering options for the date. */
  selectedStartDate = model<Date | undefined>(undefined);
  selectedEndDate = model<Date | undefined>(undefined);

  /** Store the filtered ticket data. */
  paginatedTickets: WritableSignal<
    | Paginated<OfficeHourTicketOverview, OfficeHourStatisticsPaginationParams>
    | undefined
  > = signal(undefined);
  previousPaginationParams: OfficeHourStatisticsPaginationParams =
    DefaultOfficeHourStatisticsPaginationParams;

  /** Store the statistics data */
  ticketStatistics: WritableSignal<OfficeHoursTicketStatistics | undefined> =
    signal(undefined);

  /** Helper function that helps to load the paginated data. */
  loadPaginatedData(params: OfficeHourStatisticsPaginationParams) {
    this.myCoursesService
      .getPaginatedOfficeHoursStatisticsTicketHistory(this.courseSiteId, params)
      .subscribe((data) => {
        this.paginatedTickets.set(data);
        this.previousPaginationParams = data.params;
      });
    this.myCoursesService
      .getOfficeHoursTicketStatistics(this.courseSiteId, params)
      .subscribe((data) => {
        this.ticketStatistics.set(data);
      });
  }

  /** Effect that handles filter changes and updates the data accordingly. */
  filterEffect = effect(() => {
    this.loadPaginatedData({
      page: 0,
      page_size: 25,
      student_ids: JSON.stringify(
        this.selectedStudentFilterOptions().map((student) => student.item.id)
      ),
      staff_ids: JSON.stringify(
        this.selectedStaffFilterOptions().map((staff) => staff.item.id)
      ),
      range_start: this.selectedStartDate()?.toISOString() ?? '',
      range_end: this.selectedEndDate()?.toISOString() ?? ''
    } as OfficeHourStatisticsPaginationParams);
  });

  /** Handler for the Material pagination stepper. */
  handlePageEvent(e: PageEvent) {
    let paginationParams = this.previousPaginationParams;
    paginationParams.page = e.pageIndex;
    paginationParams.page_size = e.pageSize;
    this.loadPaginatedData(paginationParams);
  }

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    protected myCoursesService: MyCoursesService,
    protected dialog: MatDialog,
    protected snackBar: MatSnackBar
  ) {
    // Get the course site ID from the route parameters
    this.courseSiteId = +this.route.parent!.snapshot.params['course_site_id'];
    // Get the filter options for the course site
    this.myCoursesService
      .getOfficeHoursStatisticsFilterOptions(this.courseSiteId)
      .subscribe((data) => {
        this.filterOptions.set(data);

        // Read the query parameters
        const studentIds = this.route.snapshot.queryParamMap
          .get('studentId')
          ?.split(',');
        const staffIds = this.route.snapshot.queryParamMap
          .get('staffId')
          ?.split(',');

        // Add students to the filter
        const studentsToAdd: MatFilterChipSearchableItem<PublicProfile>[] = (
          studentIds ?? []
        ).reduce<MatFilterChipSearchableItem<PublicProfile>[]>(
          (studentsToAdd, studentId) => {
            const student = data.students.find((s) => s.id === +studentId);
            if (student) {
              studentsToAdd.push({
                displayText: `${student.first_name} ${student.last_name}`,
                item: student
              });
            }
            return studentsToAdd;
          },
          []
        );

        // Add staff to the filter
        const staffToAdd: MatFilterChipSearchableItem<PublicProfile>[] = (
          staffIds ?? []
        ).reduce<MatFilterChipSearchableItem<PublicProfile>[]>(
          (staffToAdd, staffId) => {
            const staff = data.staff.find((s) => s.id === +staffId);
            if (staff) {
              staffToAdd.push({
                displayText: `${staff.first_name} ${staff.last_name}`,
                item: staff
              });
            }
            return staffToAdd;
          },
          []
        );

        this.selectedStudentFilterOptions.set(studentsToAdd);
        this.selectedStaffFilterOptions.set(staffToAdd);
      });
  }

  clearStudentFilter() {
    this.selectedStudentFilterOptions.set([]);
  }

  clearStaffFilter() {
    this.selectedStaffFilterOptions.set([]);
  }

  clearDateRangeFilter() {
    this.selectedStartDate.set(undefined);
    this.selectedEndDate.set(undefined);
  }

  /** Clear all currently-set filters when needed */
  clearFilters() {
    this.selectedStudentFilterOptions.set([]);
    this.selectedStaffFilterOptions.set([]);
    this.selectedStartDate.set(undefined);
    this.selectedEndDate.set(undefined);
  }

  /** Open the ticket details dialog */
  openTicketDetails(ticket: OfficeHourTicketOverview) {
    this.dialog.open(TicketDetailsDialog, {
      height: '500px',
      width: '450px',
      data: { ticket }
    });
  }

  /**
   * Downloads the ticket data as a CSV file.
   */
  downloadTicketData() {
    this.myCoursesService
      .getOfficeHoursTicketCsv(this.courseSiteId, {
        student_ids: JSON.stringify(
          this.selectedStudentFilterOptions().map((student) => student.item.id)
        ),
        staff_ids: JSON.stringify(
          this.selectedStaffFilterOptions().map((staff) => staff.item.id)
        ),
        range_start: this.selectedStartDate()?.toISOString() ?? '',
        range_end: this.selectedEndDate()?.toISOString() ?? ''
      } as OfficeHourStatisticsPaginationParams)
      .subscribe({
        next: (response) => {
          saveAs(response, 'ticket-data.csv');
          this.snackBar.open('Office hours data downloaded.', '', {
            duration: 2000
          });
        },
        error: () => {
          this.snackBar.open(
            'There was an error downloading office hours data.',
            '',
            {
              duration: 2000
            }
          );
        }
      });
  }

  urlUpdateEffect = effect(
    () => {
      const studentIds = this.selectedStudentFilterOptions()
        .map((student) => student.item.id)
        .join(',');
      const staffIds = this.selectedStaffFilterOptions()
        .map((staff) => staff.item.id)
        .join(',');
      const rangeStart = this.selectedStartDate()?.toISOString() ?? '';
      const rangeEnd = this.selectedEndDate()?.toISOString() ?? '';
      if (studentIds || staffIds || rangeStart || rangeEnd) {
        this.router.navigate([], {
          relativeTo: this.route,
          queryParams: {
            studentId: studentIds || null,
            staffId: staffIds || null,
            range_start: rangeStart || null,
            range_end: rangeEnd || null
          },
          queryParamsHandling: 'merge'
        });
      }
    },
    { allowSignalWrites: true }
  ); // Allow signal writes to update the URL with the selected filters
}
