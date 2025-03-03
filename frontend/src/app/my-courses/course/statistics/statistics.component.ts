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
import { ActivatedRoute } from '@angular/router';
import { OfficeHourStatisticsFilterData } from '../../my-courses.model';
import { PublicProfile } from 'src/app/profile/profile.service';

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
  selectedStudentFilterOptions: MatFilterChipSearchableItem<PublicProfile>[] =
    [];

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
  selectedStaffFilterOptions: MatFilterChipSearchableItem<PublicProfile>[] = [];

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

  constructor(
    private route: ActivatedRoute,
    protected myCoursesService: MyCoursesService
  ) {
    // Get the course site ID from the route parameters
    this.courseSiteId = +this.route.parent!.snapshot.params['course_site_id'];
    // Get the filter options for the course site
    this.myCoursesService
      .getOfficeHoursStatisticsFilterOptions(this.courseSiteId)
      .subscribe((data) => {
        this.filterOptions.set(data);
      });
  }

  clearFilters() {
    this.selectedStudentFilterOptions = [];
    this.selectedStaffFilterOptions = [];
    this.selectedStartDate.set(undefined);
    this.selectedEndDate.set(undefined);
  }
}
