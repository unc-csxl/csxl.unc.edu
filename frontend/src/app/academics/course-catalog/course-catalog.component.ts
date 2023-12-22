import { Component } from '@angular/core';
import { courseResolver } from '../courses.resolver';
import { Course } from '../courses.models';
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
  selector: 'app-courses-home',
  templateUrl: './course-catalog.component.html',
  styleUrls: ['./course-catalog.component.css'],
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
export class CoursesHomeComponent {
  /** Route information to be used in Course Routing Module */
  public static Route = {
    path: 'catalog',
    title: 'Course Catalog',
    component: CoursesHomeComponent,
    canActivate: [],
    resolve: { courses: courseResolver }
  };

  /** Store Observable list of Courses */
  public courses: Course[];

  public displayedColumns: string[] = ['code', 'title'];
  public columnsToDisplayWithExpand = [...this.displayedColumns, 'expand'];
  public expandedElement: Course | null = null;

  /** Constructor for the course catalog page. */
  constructor(
    private route: ActivatedRoute,
    public coursesService: CourseService
  ) {
    // Initialize data from resolvers
    const data = this.route.snapshot.data as {
      courses: Course[];
    };

    this.courses = data.courses;

    console.log(this.courses);
  }
}
