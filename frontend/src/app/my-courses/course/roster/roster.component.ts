/**
 * The Roster Component enables instructors to view the roster of their courses.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import {
  Component,
  Signal,
  WritableSignal,
  effect,
  signal
} from '@angular/core';
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

@Component({
  selector: 'app-roster',
  templateUrl: './roster.component.html',
  styleUrl: './roster.component.css'
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

  public displayedColumns: string[] = ['section', 'name', 'pid', 'email'];

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

  courseSiteId: string;

  constructor(
    private route: ActivatedRoute,
    protected dialog: MatDialog,
    protected myCoursesService: MyCoursesService
  ) {
    this.courseSiteId = this.route.parent!.snapshot.params['course_site_id'];

    this.rosterPaginator = new Paginator<CourseMemberOverview>(
      `/api/my-courses/${this.courseSiteId}/roster`
    );

    this.rosterPaginator.loadPage(this.previousParams).subscribe((page) => {
      this.rosterPage.set(page);
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
      height: '400px',
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
}
