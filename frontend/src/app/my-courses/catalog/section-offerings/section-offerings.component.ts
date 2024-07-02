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
  coursesResolver,
  currentTermResolver,
  termsResolver
} from '../../../academics/academics.resolver';
import {
  CatalogSection,
  Course,
  RosterRole,
  Section,
  SectionMember,
  Term
} from '../../../academics/academics.models';
import { ActivatedRoute } from '@angular/router';
import { AcademicsService } from '../../../academics/academics.service';
import {
  animate,
  state,
  style,
  transition,
  trigger
} from '@angular/animations';
import { FormControl } from '@angular/forms';
import { NagivationAdminGearService } from 'src/app/navigation/navigation-admin-gear.service';

@Component({
  selector: 'app-offerings',
  templateUrl: './section-offerings.component.html',
  styleUrls: ['./section-offerings.component.css'],
  animations: [
    trigger('detailExpand', [
      state('collapsed,void', style({ height: '0px', minHeight: '0' })),
      state('expanded', style({ height: '*' })),
      transition(
        'expanded <=> collapsed',
        animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')
      )
    ])
  ]
})
export class SectionOfferingsComponent implements OnInit {
  /** Route information to be used in Course Routing Module */
  public static Route = {
    path: 'offerings',
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
    public academicsService: AcademicsService,
    private gearService: NagivationAdminGearService
  ) {
    // Initialize data from resolvers
    const data = this.route.snapshot.data as {
      terms: Term[];
      currentTerm: Term;
    };
    this.terms = data.terms;

    // Set initial display term
    this.displayTermId = data.currentTerm.id ?? null;
    this.displayTerm = signal(this.selectedTerm());
    // Initialize the sections list
    this.resetSections();
  }

  ngOnInit() {
    this.gearService.showAdminGearByPermissionCheck(
      'academics.*',
      '*',
      '',
      'academics/admin/section'
    );
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

  /** Resets the section data based on the selected term. */
  resetSections() {
    this.displayTerm.set(this.selectedTerm());
    if (this.displayTerm()) {
      this.academicsService
        .getSectionsByTerm(this.displayTerm()!)
        .subscribe((sections) => {
          this.sections.set(sections);
        });
    }
  }
}
