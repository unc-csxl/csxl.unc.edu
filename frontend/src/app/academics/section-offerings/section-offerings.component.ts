import { Component } from '@angular/core';
import { courseResolver, termResolver } from '../courses.resolver';
import {
  Course,
  RosterRole,
  Section,
  SectionMember,
  Term
} from '../courses.models';
import { ActivatedRoute } from '@angular/router';
import { CourseService } from '../courses.service';
import {
  animate,
  state,
  style,
  transition,
  trigger
} from '@angular/animations';
import { FormControl } from '@angular/forms';

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
export class SectionOfferingsComponent {
  /** Route information to be used in Course Routing Module */
  public static Route = {
    path: 'offerings',
    title: 'Course Offerings',
    component: SectionOfferingsComponent,
    canActivate: [],
    resolve: { terms: termResolver, courses: courseResolver }
  };

  /** Store list of Courses */
  public courses: Course[];
  /** Store list of Terms  */
  public terms: Term[];

  /** Store the currently selected term from the form */
  public displayTerm: FormControl<Term> = new FormControl();

  /** Store the columns to display in the table */
  public displayedColumns: string[] = [
    'code',
    'title',
    'instructor',
    'meetingpattern',
    'room'
  ];
  /** Store the columns to display when extended */
  public columnsToDisplayWithExpand = [...this.displayedColumns, 'expand'];
  /** Store the element where the dropdown is currently active */
  public expandedElement: Section | null = null;

  /** Constructor for the course catalog page. */
  constructor(
    private route: ActivatedRoute,
    public coursesService: CourseService
  ) {
    // Initialize data from resolvers
    const data = this.route.snapshot.data as {
      courses: Course[];
      terms: Term[];
    };
    this.courses = data.courses;
    this.terms = data.terms;

    // Set initial display term
    this.displayTerm.setValue(this.terms[1]);
  }

  /** Helper function that returns the course object from the list with the given ID.
   * @param id ID of the course to look up.
   * @returns Course for the ID, if it exists.
   */
  courseFromId(id: string): Course | null {
    // Find the course for the given ID
    let coursesFilter = this.courses.filter((c) => c.id === id);
    // Return either the course if it exists, or null.
    return coursesFilter.length > 0 ? coursesFilter[0] : null;
  }

  /** Helper function that generates an instructor's name for a given section.
   * @param section Section to create the instructor name for.
   * @returns Name of the section's instructor, or 'Unknown' if no instructor is set.
   */
  instructorNameForSection(section: Section): string {
    // Find all staff with the instructor role
    let staffFilter = section.staff?.filter(
      (s) => s.member_role == RosterRole.INSTRUCTOR
    );
    // Find the instructor
    let instructor = staffFilter?.length ?? 0 > 0 ? staffFilter![0] : null;
    // Return the name for the instructor
    // If instructor exists: <First Name> <Last Name>
    // Otherwise: 'Unknown'
    return instructor
      ? instructor.first_name + ' ' + instructor.last_name
      : 'Unknown';
  }
}
