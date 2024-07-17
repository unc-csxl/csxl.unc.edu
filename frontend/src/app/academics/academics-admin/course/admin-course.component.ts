/**
 * The Courses Admin page enables the administrator to add, edit,
 * and delete courses.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2023
 * @license MIT
 */

import { Component, WritableSignal, inject, signal } from '@angular/core';
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
  courses: WritableSignal<Course[]> = signal([]);

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
   * @param event: event to stop propagation
   * @returns void
   */
  deleteCourse(course: Course, event: Event): void {
    event.stopPropagation();
    let confirmDelete = this.snackBar.open(
      'Are you sure you want to delete this course?',
      'Delete'
    );
    confirmDelete.onAction().subscribe(() => {
      this.academicsService.deleteCourse(course).subscribe({
        next: () => {
          this.courses.update((courses) => {
            let newCourses = courses.filter((c) => c.id !== course.id);
            return [...newCourses];
          });
          this.snackBar.open('This course has been deleted.', '', {
            duration: 2000
          });
        },
        error: () => {
          this.snackBar.open(
            'Delete failed. Make sure to remove all sections for this course first.',
            '',
            {
              duration: 2000
            }
          );
        }
      });
    });
  }
}
