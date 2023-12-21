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

@Component({
  selector: 'app-offerings',
  templateUrl: './offerings.component.html',
  styleUrls: ['./offerings.component.css'],
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
export class OfferingsComponent {
  /** Route information to be used in Course Routing Module */
  public static Route = {
    path: 'offerings',
    title: 'Course Offerings',
    component: OfferingsComponent,
    canActivate: [],
    resolve: { terms: termResolver, courses: courseResolver }
  };

  /** Store Observable list of Courses */
  public courses: Course[];
  public terms: Term[];

  public displayTerm: Term;

  public displayedColumns: string[] = [
    'code',
    'title',
    'instructor',
    'meetingpattern'
  ];
  public columnsToDisplayWithExpand = [...this.displayedColumns, 'expand'];
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
    this.displayTerm = this.terms[1];
  }

  courseFromId(id: string): Course | null {
    let coursesFilter = this.courses.filter((c) => c.id === id);
    return coursesFilter.length > 0 ? coursesFilter[0] : null;
  }

  instructorNameForSection(section: Section): string {
    let staffFilter = section.staff?.filter(
      (s) => s.member_role == RosterRole.INSTRUCTOR
    );
    let instructor = staffFilter?.length ?? 0 > 0 ? staffFilter![0] : null;

    return instructor
      ? instructor.first_name + ' ' + instructor.last_name
      : 'Unknown';
  }
}
