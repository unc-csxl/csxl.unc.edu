/**
 * The Section Offerings page enables users to view all current offerings of
 * the COMP courses.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2023
 * @license MIT
 */

import { Component, OnInit, WritableSignal, signal } from '@angular/core';
import {
  currentTermResolver,
  termsResolver
} from '../../../academics/academics.resolver';
import { CatalogSection, Section, Term } from '../../../academics/academics.models';
import { ActivatedRoute, ParamMap, Router } from '@angular/router';
import { AcademicsService } from '../../../academics/academics.service';
import {
  animate,
  state,
  style,
  transition,
  trigger
} from '@angular/animations';
import { NagivationAdminGearService } from 'src/app/navigation/navigation-admin-gear.service';

@Component({
  selector: 'app-offerings',
  templateUrl: './section-offerings.component.html',
  animations: [
    trigger('detailExpand', [
      state('collapsed,void', style({ height: '0px', minHeight: '0' })),
      state('expanded', style({ height: '*' })),
      transition(
        'expanded <=> collapsed',
        animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')
      )
    ])
  ],
  standalone: false
})
export class SectionOfferingsComponent implements OnInit {
  /** Route information to be used in Course Routing Module */
  public static Route = {
    path: 'offerings/:term_id',
    title: 'Catalog',
    component: SectionOfferingsComponent,
    canActivate: [],
    resolve: {
      terms: termsResolver,
      currentTerm: currentTermResolver
    }
  };

  /** Signal to store the list of sections for a term. */
  public sections: WritableSignal<CatalogSection[]> = signal([]);

  /** Store list of Terms  */
  public terms: Term[];
  public currentTermId: string | null;

  /** Store the currently selected term from the form */
  // NOTE: Separating these fields into an ID and a selected term was required
  // for Angular to correctly show the correct term in the initial drop down.
  public displayTermId: string | null;
  public displayTerm: WritableSignal<Term | undefined>;

  /** Store the columns to display in the table */
  public displayedColumns: string[] = [
    'code',
    'title',
    'instructor',
    'meetingpattern',
    'room',
    'enrollment'
  ];
  /** Store the columns to display when extended */
  public columnsToDisplayWithExpand = [...this.displayedColumns, 'expand'];
  /** Store the element where the dropdown is currently active */
  public expandedElement: Section | null = null;

  /** Constructor for the course catalog page. */
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    public academicsService: AcademicsService,
    private gearService: NagivationAdminGearService
  ) {
    // Initialize data from resolvers
    const data = this.route.snapshot.data as {
      terms: Term[];
      currentTerm: Term;
    };
    this.terms = data.terms;
    this.currentTermId = data.currentTerm.id ?? null;

    // Set initial display term from URL term when valid, else fallback to current term.
    const initialTermId = this.route.snapshot.paramMap.get('term_id');
    this.displayTermId = this.resolveDisplayTermId(initialTermId);
    this.displayTerm = signal(this.selectedTerm());
  }

  ngOnInit() {
    this.gearService.showAdminGearByPermissionCheck(
      'academics.*',
      '*',
      '',
      'academics/admin/section'
    );

    this.route.paramMap.subscribe((params: ParamMap) => {
      const termIdFromRoute = params.get('term_id');
      const resolvedTermId = this.resolveDisplayTermId(termIdFromRoute);

      if (resolvedTermId !== this.displayTermId) {
        this.displayTermId = resolvedTermId;
      }

      this.resetSections();
    });
  }

  /** Helper function that generates an instructor's name for a given section.
   * @param section Section to create the instructor name for.
   * @returns Name of the section's instructor, or 'Unknown' if no instructor is set.
   */
  instructorNameForSection(section: CatalogSection): string {
    if (!section.instructors || section.instructors.length == 0)
      return 'Unknown';
    let instructorText = '';

    for (let instructor of section.instructors) {
      instructorText +=
        instructor.first_name + ' ' + instructor.last_name + ', ';
    }
    return instructorText.substring(0, instructorText.length - 2);
  }

  selectedTerm() {
    return this.terms.find((term) => term.id == this.displayTermId);
  }

  private resolveDisplayTermId(termIdFromRoute: string | null): string | null {
    if (
      termIdFromRoute &&
      this.terms.some((term) => term.id === termIdFromRoute)
    ) {
      return termIdFromRoute;
    }
    return this.currentTermId;
  }

  onTermChange() {
    if (!this.displayTermId) return;
    this.router.navigate(['/catalog/offerings', this.displayTermId]);
  }

  /** Resets the section data based on the selected term. */
  resetSections() {
    this.displayTerm.set(this.selectedTerm());
    if (this.displayTerm()) {
      this.academicsService
        .getSectionsByTerm(this.displayTerm()!)
        .subscribe((sections: CatalogSection[]) => {
          this.sections.set(sections);
        });
    }
  }
}
