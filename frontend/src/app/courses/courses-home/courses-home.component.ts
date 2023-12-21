import { Component } from '@angular/core';
import { courseResolver } from '../courses.resolver';
import { Course } from '../courses.models';
import { ActivatedRoute } from '@angular/router';
import { CourseService } from '../courses.service';

@Component({
  selector: 'app-courses-home',
  templateUrl: './courses-home.component.html',
  styleUrls: ['./courses-home.component.css']
})
export class CoursesHomeComponent {
  /** Route information to be used in Course Routing Module */
  public static Route = {
    path: '',
    title: 'Course Catalog',
    component: CoursesHomeComponent,
    canActivate: [],
    resolve: { courses: courseResolver }
  };

  /** Store Observable list of Courses */
  public courses: Course[];

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
