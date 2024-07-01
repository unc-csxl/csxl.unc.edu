import { Component, OnInit, WritableSignal, signal } from '@angular/core';
import { MyCoursesService } from '../my-courses.service';
import { Application } from 'src/app/ta-application/application.model';
import { Router } from '@angular/router';
import { MatDialog } from '@angular/material/dialog';
import { UTANoticeComponent } from 'src/app/ta-application/uta-notice/uta-notice.component';
import { ApplicationsService } from 'src/app/ta-application/ta-application.service';
import { CreateCourseSiteDialog } from '../dialogs/create-course-site/create-course-site.dialog';

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
    protected dialog: MatDialog,
    public applicationService: ApplicationsService // to remove.
  ) {
    // to remove.
    this.applicationService.applications$.subscribe((application) => {
      this.applications.set(application);
    });
  }

  /** Temporary (delete with UTA Application rewrite.) */
  applications: WritableSignal<Application[]> = signal([]);
  onUTAClick(): void {
    if (this.applications().length > 0) {
      this.router.navigate(['/ta-application/uta-application/']);
    } else {
      const dialogRef = this.dialog.open(UTANoticeComponent, {
        width: '1000px',
        autoFocus: false
      });
      dialogRef.afterClosed().subscribe();
    }
  }

  /** Opens the dialog for creating a course site */
  createCourseSite(): void {
    this.dialog.open(CreateCourseSiteDialog, {
      height: '560px',
      width: '620px',
      data: this.myCoursesService.allTerms()
    });
  }
}
