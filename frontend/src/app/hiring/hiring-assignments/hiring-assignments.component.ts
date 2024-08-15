import { Component, effect, signal, WritableSignal } from '@angular/core';
import {
  DEFAULT_PAGINATION_PARAMS,
  Paginated,
  PaginationParams,
  Paginator
} from 'src/app/pagination';
import { HiringAssignmentOverview } from '../hiring.models';
import { ActivatedRoute } from '@angular/router';
import { HiringService } from '../hiring.service';
import { PageEvent } from '@angular/material/paginator';
import { Term } from 'src/app/academics/academics.models';
import { AcademicsService } from 'src/app/academics/academics.service';
import {
  CourseSite,
  UpdatedCourseSite
} from 'src/app/my-courses/my-courses.model';
import { MyCoursesService } from 'src/app/my-courses/my-courses.service';
import { Observable, tap } from 'rxjs';

@Component({
  selector: 'app-hiring-assignments',
  templateUrl: './hiring-assignments.component.html',
  styleUrl: './hiring-assignments.component.css'
})
export class HiringAssignmentsComponent {
  /** Route for the routing module */
  public static Route = {
    path: 'assignments',
    title: 'Hiring Assignments',
    component: HiringAssignmentsComponent
  };

  /** Encapsulated assignment paginator and params */
  private assignmentPaginator: Paginator<HiringAssignmentOverview>;
  assignmentPage: WritableSignal<
    Paginated<HiringAssignmentOverview, PaginationParams> | undefined
  > = signal(undefined);
  private previousParams: PaginationParams = DEFAULT_PAGINATION_PARAMS;

  public displayedColumns: string[] = ['name', 'onyen', 'email', 'level'];

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
    this.assignmentPaginator.loadPage(paginationParams).subscribe((page) => {
      this.assignmentPage.set(page);
      this.previousParams = paginationParams;
    });
  });

  /** Store term and course site data */
  term$: Observable<Term> | undefined;
  courseSite$: Observable<UpdatedCourseSite>;

  constructor(
    private route: ActivatedRoute,
    protected hiringService: HiringService,
    protected academicsService: AcademicsService,
    protected myCoursesService: MyCoursesService
  ) {
    let courseSiteId = this.route.parent!.snapshot.params['courseSiteId'];

    this.courseSite$ = this.myCoursesService.getCourseSite(courseSiteId).pipe(
      tap((courseSite) => {
        this.term$ = this.academicsService.getTerm(courseSite.term_id);
      })
    );

    this.assignmentPaginator = new Paginator<HiringAssignmentOverview>(
      `/api/hiring/assignments/${courseSiteId}`
    );

    this.assignmentPaginator.loadPage(this.previousParams).subscribe((page) => {
      this.assignmentPage.set(page);
    });
  }

  handlePageEvent(e: PageEvent) {
    let paginationParams = this.assignmentPage()!.params;
    paginationParams.page = e.pageIndex;
    paginationParams.page_size = e.pageSize;
    this.assignmentPaginator.loadPage(paginationParams).subscribe((page) => {
      this.assignmentPage.set(page);
      this.previousParams = paginationParams;
    });
  }

  /** Export CSV button pressed */
  exportCsv() {
    this.courseSite$.subscribe((courseSite) => {
      this.hiringService.downloadHiringAssignmentsCsv(courseSite.id);
    });
  }
}
