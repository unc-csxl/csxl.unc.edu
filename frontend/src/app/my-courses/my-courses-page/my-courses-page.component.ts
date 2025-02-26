import { Component, OnInit, WritableSignal, signal } from '@angular/core';
import { MyCoursesService } from '../my-courses.service';
import { Router } from '@angular/router';
import { MatDialog } from '@angular/material/dialog';
import { CreateCourseSiteDialog } from '../dialogs/create-course-site/create-course-site.dialog';
import { TermOverview } from '../my-courses.model';

@Component({
  selector: 'app-my-courses-page',
  templateUrl: './my-courses-page.component.html',
  styleUrl: './my-courses-page.component.css'
})
export class MyCoursesPageComponent {
  /** Route information to be used in the routing module */
  public static Route = {
    path: 'my-courses',
    title: 'My Courses',
    component: MyCoursesPageComponent
  };

  /** Whether or not to show the previous courses */
  showPreviousCourses: WritableSignal<boolean> = signal(false);
  instructorCourses: any[] = [];
  studentCourses: any[] = [];

  constructor(
    protected myCoursesService: MyCoursesService,
    private router: Router,
    protected dialog: MatDialog
  ) {}

  /** Opens the dialog for creating a course site */
  createCourseSite(): void {
    this.dialog.open(CreateCourseSiteDialog, {
      height: '560px',
      width: '620px',
      data: this.myCoursesService.allTerms()
    });
  }

  /** Returns names of active terms in comma separated format */
  getActiveTermNames(): string {
    return this.myCoursesService
      .currentTerms()
      .map(term => term.name)
      .join(', ');
  }

  /** Returns whether or not user has a non-student role in a course during the current terms */
  hasInstructorCourses(): boolean {
    return this.myCoursesService.currentTerms().some((term) => {
      return term.sites.some(course => course.role !== 'Student');
    });
  }
  
    /** Returns whether or not user has a student role in a course during the current terms */
  hasStudentCourses(): boolean {
    return this.myCoursesService.currentTerms().some((term) => {
      return term.sites.some(course => course.role === 'Student');
    });
  }

  /** Returns the courses where the user is an instructor during the current terms */
  getInstructorCourses(): any[] {
    return this.myCoursesService.currentTerms().flatMap((term) => {
      return term.sites.filter(course => course.role !== 'Student').map(course => ({
        ...course,
        termId: term.id
      }));
    });
  }

  /** Returns the courses where the user is a student during the current terms */
  getStudentCourses(): any[] {
    return this.myCoursesService.currentTerms().flatMap((term) => {
      return term.sites.filter(course => course.role === 'Student').map(course => ({
        ...course,
        termId: term.id
      }));
    });
  }

  
}


