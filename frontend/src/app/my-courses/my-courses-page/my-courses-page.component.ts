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

  getActiveTermNames(): string {
    return this.myCoursesService
      .currentTerms()
      .map(term => term.name)
      .join(', ');
  }

  /** Returns whether or not user has a non-student role in a course during a term */
  hasInstructorCourses(term: TermOverview): boolean {
    return term.sites.some(course => course.role !== 'Student');
  }
  
    /** Returns whether or not user has a student role in a course during a term */
  hasStudentCourses(term: TermOverview): boolean {
    return term.sites.some(course => course.role === 'Student');
  }
}


