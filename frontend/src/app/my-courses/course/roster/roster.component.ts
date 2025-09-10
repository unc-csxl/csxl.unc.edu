/**
 * The Roster Component enables instructors to view the roster of their courses.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { Component, WritableSignal, effect, signal } from '@angular/core';
import {
  DEFAULT_PAGINATION_PARAMS,
  Paginated,
  PaginationParams,
  Paginator
} from 'src/app/pagination';
import { CourseMemberOverview } from '../../my-courses.model';
import { ActivatedRoute, Router } from '@angular/router';
import { PageEvent } from '@angular/material/paginator';
import { MatDialog } from '@angular/material/dialog';
import { ImportRosterDialog } from '../../dialogs/import-roster/import-roster.dialog';
import { MyCoursesService } from '../../my-courses.service';
import { saveAs } from 'file-saver';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
    selector: 'app-roster',
    templateUrl: './roster.component.html',
    styleUrl: './roster.component.css',
    standalone: false
})
export class RosterComponent {
  /** Route information to be used in the routing module */
  public static Route = {
    path: 'roster',
    title: 'Course',
    component: RosterComponent
  };

  /** Encapsulated roster paginator and params */
  private rosterPaginator: Paginator<CourseMemberOverview>;
  rosterPage: WritableSignal<
    Paginated<CourseMemberOverview, PaginationParams> | undefined
  > = signal(undefined);
  private previousParams: PaginationParams = DEFAULT_PAGINATION_PARAMS;

  public displayedColumns: string[] = ['section', 'name', 'role'];

  /** Current search bar query */
  public searchBarQuery: WritableSignal<string> = signal('');

  // TODO: ADD DEBOUNCE
  /**
   * Effect that refreshes the  pagination when the search bar text changes.
   */
  searchBarEffect = effect(() => {
    // Update the parameters with the new date range
    let paginationParams = this.previousParams;
    paginationParams.filter = this.searchBarQuery();

    // Refresh the data
    this.rosterPaginator.loadPage(paginationParams).subscribe((page) => {
      this.rosterPage.set(page);
      this.previousParams = paginationParams;
    });
  });

  courseSiteId: number;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    protected dialog: MatDialog,
    protected myCoursesService: MyCoursesService,
    protected snackBar: MatSnackBar
  ) {
    this.courseSiteId = this.route.parent!.snapshot.params['course_site_id'];

    this.rosterPaginator = new Paginator<CourseMemberOverview>(
      `/api/my-courses/${this.courseSiteId}/roster`
    );

    this.rosterPaginator.loadPage(this.previousParams).subscribe((page) => {
      this.rosterPage.set(page);
    });

    // This subscription loads whether or not the user is a student in the course, and
    // hides some detail columns if so. This is a hack to get around requirements for
    // Angular tables, and should be revisited in the future.
    this.myCoursesService.getTermOverviews().subscribe((terms) => {
      const courseSite = terms
        .flatMap((term) => term.sites)
        .find((site) => site.id == +this.courseSiteId);
      if (courseSite?.role !== 'Student') {
        this.displayedColumns = [
          'section',
          'name',
          'pid',
          'email',
          'role',
          'actions'
        ];
      }
    });
  }

  handlePageEvent(e: PageEvent) {
    let paginationParams = this.rosterPage()!.params;
    paginationParams.page = e.pageIndex;
    paginationParams.page_size = e.pageSize;
    this.rosterPaginator.loadPage(paginationParams).subscribe((page) => {
      this.rosterPage.set(page);
      this.previousParams = paginationParams;
    });
  }

  /** Opens the dialog for importing the roster */
  importFromCanvas(): void {
    let dialogRef = this.dialog.open(ImportRosterDialog, {
      height: '540px',
      width: '600px',
      data: this.myCoursesService.courseOverview(
        this.route.parent!.snapshot.params['course_site_id']
      )
    });
    dialogRef.afterClosed().subscribe((_) => {
      this.rosterPaginator.loadPage(this.previousParams).subscribe((page) => {
        this.rosterPage.set(page);
      });
    });
  }

  /** Copies student email to clipboard */
  copyToClipboard(email: string): void {
    navigator.clipboard.writeText(email).then(() => {
      this.snackBar.open('Copied to clipboard', '', {
        duration: 2000
      });
    });
  }

  /** Download course roster as csv */
  downloadCourseRoster(): void {
    this.myCoursesService.getCourseRosterCsv(this.courseSiteId).subscribe({
      next: (response) => {
        saveAs(response, 'course-roster.csv');
        this.snackBar.open('Course roster downloaded', '', {
          duration: 2000
        });
      },
      error: () => {
        this.snackBar.open(
          'There was an error downloading the course roster.',
          '',
          {
            duration: 2000
          }
        );
      }
    });
  }

  /** Navigate to statistics page and populate student or staff in the filter */
  openUserStatistics(member: CourseMemberOverview): void {
    const isStudent = member.role === 'Student'; // Check if the member is a student
    const queryParamKey = isStudent ? 'studentId' : 'staffId'; // Use appropriate query parameter

    this.router.navigate(['../statistics'], {
      relativeTo: this.route,
      queryParams: {
        [queryParamKey]: member.id // Pass `studentId` or `staffId` based on the role
      }
    });
  }
}
