import {
  Component,
  computed,
  effect,
  signal,
  WritableSignal
} from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Term } from 'src/app/academics/academics.models';
import {
  currentTermResolver,
  termsResolver
} from 'src/app/academics/academics.resolver';
import { HiringService } from '../hiring.service';
import { AcademicsService } from 'src/app/academics/academics.service';
import { Paginated, PaginationParams, Paginator } from 'src/app/pagination';
import {
  HiringAssignmentDraft,
  HiringAssignmentSummaryOverview
} from '../hiring.models';
import { PageEvent } from '@angular/material/paginator';

const DEFAULT_PAGINATION_PARAMS = {
  page: 0,
  page_size: 50,
  order_by: '',
  filter: ''
} as PaginationParams;

@Component({
    selector: 'app-hiring-summary',
    templateUrl: './hiring-summary.component.html',
    styleUrl: './hiring-summary.component.css',
    standalone: false
})
export class HiringSummaryComponent {
  /** Route for the routing module */
  public static Route = {
    path: 'summary',
    title: 'Hiring Onboarding',
    component: HiringSummaryComponent,
    resolve: {
      terms: termsResolver,
      currentTerm: currentTermResolver
    }
  };

  /** Store list of Terms  */
  public terms: Term[];
  public selectedTermId: WritableSignal<string | undefined> = signal(undefined);

  public selectedTerm = computed(() => {
    return this.terms.find((term) => term.id === this.selectedTermId())!;
  });

  /** Effect that updates the hiring data when the selected term changes. */
  selectedTermEffect = effect(() => {
    if (this.selectedTermId()) {
      const term = this.terms.find(
        (term) => term.id === this.selectedTermId()
      )!;
      // Load paginated data
      this.assignmentsPaginator.changeApiRoute(
        `/api/hiring/summary/${term.id}`
      );

      this.assignmentsPaginator
        .loadPage(this.previousPaginationParams)
        .subscribe((page) => {
          this.assignmentsPage.set(page);
        });
    }
  });

  /** Encapsulated future events paginator and params */
  private assignmentsPaginator: Paginator<HiringAssignmentSummaryOverview>;
  assignmentsPage: WritableSignal<
    Paginated<HiringAssignmentSummaryOverview, PaginationParams> | undefined
  > = signal(undefined);
  private previousPaginationParams: PaginationParams =
    DEFAULT_PAGINATION_PARAMS;

  public displayedColumns: string[] = [
    'flagged',
    'name',
    'course',
    'level',
    'i9',
    'position_number',
    'epar',
    'notes'
  ];

  /** Current search bar query */
  public searchBarQuery: WritableSignal<string> = signal('');

  // TODO: ADD DEBOUNCE
  /**
   * Effect that refreshes the  pagination when the search bar text changes.
   */
  searchBarEffect = effect(() => {
    // Update the parameters with the new date range
    let paginationParams = this.previousPaginationParams;
    paginationParams.filter = this.searchBarQuery();

    // Refresh the data
    this.assignmentsPaginator.loadPage(paginationParams).subscribe((page) => {
      this.assignmentsPage.set(page);
      this.previousPaginationParams = paginationParams;
    });
  });

  /** Constructor */
  constructor(
    private route: ActivatedRoute,
    protected hiringService: HiringService,
    protected academicsService: AcademicsService
  ) {
    // Initialize data from resolvers
    const data = this.route.snapshot.data as {
      terms: Term[];
      currentTerm: Term | undefined;
    };

    this.terms = data.terms;
    this.selectedTermId.set(data.currentTerm?.id ?? undefined);

    // Load paginated data
    this.assignmentsPaginator = new Paginator<HiringAssignmentSummaryOverview>(
      `/api/hiring/summary/${data.currentTerm!.id}`
    );

    this.assignmentsPaginator
      .loadPage(this.previousPaginationParams)
      .subscribe((page) => {
        this.assignmentsPage.set(page);
      });
  }

  /** Handles a pagination event for the future office hours table */
  handlePageEvent(e: PageEvent) {
    let paginationParams = this.assignmentsPage()!.params;
    paginationParams.page = e.pageIndex;
    paginationParams.page_size = e.pageSize;
    this.assignmentsPaginator.loadPage(paginationParams).subscribe((page) => {
      this.assignmentsPage.set(page);
      this.previousPaginationParams = paginationParams;
    });
  }

  /** Save changes */
  updateAssignment(assignment: HiringAssignmentSummaryOverview) {
    let draft: HiringAssignmentDraft = {
      id: assignment.id,
      user_id: assignment.user.id,
      term_id: this.selectedTerm()!.id,
      application_review_id: assignment.application_review_id,
      course_site_id: assignment.course_site_id!,
      level: assignment.level,
      status: assignment.status,
      position_number: assignment.position_number,
      epar: assignment.epar,
      i9: assignment.i9,
      notes: assignment.notes,
      flagged: assignment.flagged,
      created: new Date(), // will be overrided
      modified: new Date()
    };
    this.hiringService.updateHiringAssignment(draft).subscribe((_) => {});
  }

  /** Gets ordered hiring assignments */
  getOrderedAssignments(): HiringAssignmentSummaryOverview[] {
    const assignments = this.assignmentsPage()?.items ?? [];
    if (assignments.length === 0) {
      return [];
    }
    let sorted_assn = [...assignments].sort((a, b) => Number(b.flagged) - Number(a.flagged));
    console.log(sorted_assn);
    return sorted_assn;
  }

  /** Export CSV button pressed */
  exportCsv() {
    this.hiringService.downloadHiringSummaryCsv(this.selectedTerm()!.id);
  }
}
