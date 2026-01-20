/**
 * Enables the root user to make hiring decisions.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import {
  animate,
  state,
  style,
  transition,
  trigger
} from '@angular/animations';
import {
  Component,
  computed,
  effect,
  signal,
  WritableSignal
} from '@angular/core';
import { PublicProfile } from 'src/app/profile/profile.service';
import {
  HiringAdminOverview,
  HiringAssignmentOverview,
  HiringCourseSiteOverview
} from '../hiring.models';
import { HiringService } from '../hiring.service';
import { AcademicsService } from 'src/app/academics/academics.service';
import {
  currentTermResolver,
  termsResolver
} from 'src/app/academics/academics.resolver';
import { ActivatedRoute } from '@angular/router';
import { Term } from 'src/app/academics/academics.models';
import { FormControl } from '@angular/forms';
import { toObservable } from '@angular/core/rxjs-interop';

enum HiringAdminTableSortMethod {
  COURSE = 'Course',
  COVERAGE_ASCENDING = 'Coverage (Asc)',
  COVERAGE_DESCENDING = 'Coverage (Desc)'
}

@Component({
    selector: 'app-hiring-admin',
    templateUrl: './hiring-admin.component.html',
    styleUrl: './hiring-admin.component.css',
    animations: [
        trigger('detailExpand', [
            state('collapsed,void', style({ height: '0px', minHeight: '0' })),
            state('expanded', style({ height: '*' })),
            transition('expanded <=> collapsed', animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)'))
        ])
    ],
    standalone: false
})
export class HiringAdminComponent {
  /** Route for the routing module */
  public static Route = {
    path: 'admin',
    title: 'Hiring Administration',
    component: HiringAdminComponent,
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

  /** Store the hiring data. */
  hiringAdminOverview: WritableSignal<HiringAdminOverview | undefined> =
    signal(undefined);
  sortMethods = HiringAdminTableSortMethod;
  sortMethod: WritableSignal<HiringAdminTableSortMethod> = signal(
    HiringAdminTableSortMethod.COURSE
  );
  /** Calculate a list of sites based on the sorting method. */
  sortedSites: WritableSignal<HiringCourseSiteOverview[]> = signal([]);

  /** Effect that updates the sorting of course sites.
   *
   * NOTE: This seems like a more convoluted approach, but this is the only version that
   * Angular Material Tables support - computed signals are not supported, so we need an
   * effect, triggered by the sort method signal changing, that updates a signal storing
   * a list of sorted sites.
   */
  sortedSitesEffect = effect(
    () => {
      const courseSortingMethod = (
        a: HiringCourseSiteOverview,
        b: HiringCourseSiteOverview
      ) => {
        return (a.sections[0].course_number ?? '').localeCompare(
          b.sections[0].course_number ?? ''
        );
      };
      const coverageAscendingSortingMethod = (
        a: HiringCourseSiteOverview,
        b: HiringCourseSiteOverview
      ) => {
        return a.coverage - b.coverage;
      };
      const coverageDescendingSortingMethod = (
        a: HiringCourseSiteOverview,
        b: HiringCourseSiteOverview
      ) => {
        return b.coverage - a.coverage;
      };

      if (this.sortMethod() === HiringAdminTableSortMethod.COURSE) {
        this.sortedSites.set([
          ...(this.hiringAdminOverview()?.sites.sort(courseSortingMethod) ?? [])
        ]);
      }
      if (this.sortMethod() === HiringAdminTableSortMethod.COVERAGE_ASCENDING) {
        this.sortedSites.set([
          ...(this.hiringAdminOverview()?.sites.sort(
            coverageAscendingSortingMethod
          ) ?? [])
        ]);
      }
      if (
        this.sortMethod() === HiringAdminTableSortMethod.COVERAGE_DESCENDING
      ) {
        this.sortedSites.set([
          ...(this.hiringAdminOverview()?.sites.sort(
            coverageDescendingSortingMethod
          ) ?? [])
        ]);
      }
    },
    { allowSignalWrites: true } // Needed to update the signal.
  );

  // NOTE: This is required for mat tables.
  sortedSites$ = toObservable(this.sortedSites);

  /** Store the columns to display in the table */
  public displayedColumns: string[] = ['sections', 'instructor'];
  /** Store the columns to display when extended */
  public columnsToDisplayWithExpand = [...this.displayedColumns, 'expand'];
  /** Store the element where the dropdown is currently active */
  public expandedElement: HiringCourseSiteOverview | undefined = undefined;

  /** Effect that updates the hiring data when the selected term changes. */
  selectedTermEffect = effect(() => {
    if (this.selectedTermId()) {
      const term = this.terms.find(
        (term) => term.id === this.selectedTermId()
      )!;
      this.hiringService
        .getHiringAdminOverview(term.id)
        .subscribe((overview) => {
          this.hiringAdminOverview.set(overview);
        });
    }
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
  }

  /**
   * Reload the data on the creation and deletion of assignments so that
   * the coverage calculations can be re-performed.
   */
  reloadData() {
    let expanded = this.expandedElement;
    if (this.selectedTermId()) {
      const term = this.terms.find(
        (term) => term.id === this.selectedTermId()
      )!;
      this.hiringService
        .getHiringAdminOverview(term.id)
        .subscribe((overview) => {
          this.hiringAdminOverview.set(overview);
          this.expandedElement = overview.sites.find(
            (s) => s.course_site_id === expanded?.course_site_id
          );
        });
    }
  }

  /** Upload enrollment totals and refresh data */
  updateEnrollmentTotals() {
    this.hiringService.updateEnrollmentTotals().subscribe((_) => {
      this.reloadData();
    });
  }

  /** Download applicants CSV for selected term */
  downloadApplicantsCsv() {
    if (this.selectedTermId()) {
      this.hiringService.downloadApplicantsCsv(this.selectedTermId()!);
    }
  }
}
