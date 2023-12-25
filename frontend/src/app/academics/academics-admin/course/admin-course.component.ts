/**
 * The Courses Admin page enables the administrator to add, edit,
 * and delete courses.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2023
 * @license MIT
 */

import { Component, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { permissionGuard } from 'src/app/permission.guard';
import { Course } from '../../academics.models';
import { Route, Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AcademicsService } from '../../academics.service';
import { RxCourseList } from '../rx-academics-admin';

@Component({
  selector: 'app-admin-course',
  templateUrl: './admin-course.component.html',
  styleUrls: ['./admin-course.component.css']
})
export class AdminCourseComponent {
  public static Route = {
    path: 'course',
    component: AdminCourseComponent,
    title: 'Course Administration',
    canActivate: [permissionGuard('academics.course', '*')]
  };

  /** Courses List */
  public courses: RxCourseList = new RxCourseList();
  public courses$: Observable<Course[]> = this.courses.value$;

  public displayedColumns: string[] = ['name'];

  constructor(
    private router: Router,
    private snackBar: MatSnackBar,
    private academicsService: AcademicsService
  ) {
    academicsService
      .getCourses()
      .subscribe((courses) => this.courses.set(courses));
  }

  /** Event handler to open the Course Editor to create a new course */
  createCourse(): void {
    // Navigate to the course editor
    this.router.navigate(['academics', 'course', 'edit', 'new']);
  }

  /** Event handler to open the Course Editor to update a course
   * @param course: course to update
   */
  updateCourse(course: Course): void {
    // Navigate to the course editor
    this.router.navigate(['academics', 'course', 'edit', course.id]);
  }

  /** Delete a course object from the backend database table using the backend HTTP delete request.
   * @param course: course to delete
   * @returns void
   */
  deleteCourse(course: Course): void {
    let confirmDelete = this.snackBar.open(
      'Are you sure you want to delete this course?',
      'Delete'
    );
    confirmDelete.onAction().subscribe(() => {
      this.academicsService.deleteCourse(course).subscribe(() => {
        this.courses.removeCourse(course);
        this.snackBar.open('This course has been deleted.', '', {
          duration: 2000
        });
      });
    });
  }
}
