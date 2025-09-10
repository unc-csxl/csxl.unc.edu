import { Component, OnInit, WritableSignal, signal } from '@angular/core';
import { MyCoursesService } from '../my-courses.service';
import { Router } from '@angular/router';
import { MatDialog } from '@angular/material/dialog';
import { CreateCourseSiteDialog } from '../dialogs/create-course-site/create-course-site.dialog';
import { TermOverview, CourseSiteOverview } from '../my-courses.model';

interface CourseInformation extends CourseSiteOverview {
  termId: string
}

@Component({
    selector: 'app-my-courses-page',
    templateUrl: './my-courses-page.component.html',
    styleUrl: './my-courses-page.component.css',
    standalone: false
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
  getInstructorCourses(): CourseInformation[] {
    return this.myCoursesService.currentTerms().flatMap((term) => {
      return term.sites.filter(course => course.role !== 'Student').map(course => ({
        ...course,
        termId: term.id
      }));
    });
  }

  /** Returns the courses where the user is a student during the current terms */
  getStudentCourses(): CourseInformation[] {
    return this.myCoursesService.currentTerms().flatMap((term) => {
      return term.sites.filter(course => course.role === 'Student').map(course => ({
        ...course,
        termId: term.id
      }));
    });
  }

  /** Returns a user's courses in a term sorted by instructor/student status */
  getPastCourses(term: TermOverview) {
    return term.sites
      .sort((a, b) => {
        if (a.role !== 'Student' && b.role === 'Student') {
          return -1;
        }
        if (a.role === 'Student' && b.role !== 'Student') {
          return 1;
        }
        return 0;
      })
      .map(course => ({
        ...course,
        termId: term.id
      }));
  }
}


