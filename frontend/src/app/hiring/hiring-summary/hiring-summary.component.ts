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
import {
  DEFAULT_PAGINATION_PARAMS,
  Paginated,
  PaginationParams,
  Paginator
} from 'src/app/pagination';
import { HiringAssignmentSummaryOverview } from '../hiring.models';
import { PageEvent } from '@angular/material/paginator';

@Component({
  selector: 'app-hiring-summary',
  templateUrl: './hiring-summary.component.html',
  styleUrl: './hiring-summary.component.css'
})
export class HiringSummaryComponent {
  /** Route for the routing module */
  public static Route = {
    path: 'summary',
    title: 'Hiring Summary',
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
    'name',
    'onyen',
    'instructors',
    'epar',
    'position_number',
    'i9',
    'status'
  ];

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
}
