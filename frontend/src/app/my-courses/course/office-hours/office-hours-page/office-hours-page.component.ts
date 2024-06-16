import { Component, WritableSignal, signal } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { OfficeHourEventsOverview } from 'src/app/my-courses/my-courses.model';
import { MyCoursesService } from 'src/app/my-courses/my-courses.service';

@Component({
  selector: 'app-course-office-hours-page',
  templateUrl: './office-hours-page.component.html',
  styleUrl: './office-hours-page.component.css'
})
export class OfficeHoursPageComponent {
  /** Route information to be used in the routing module */
  public static Route = {
    path: 'office-hours',
    title: 'Course',
    component: OfficeHoursPageComponent
  };

  /** Signal to store the reactive office hour overview information */
  officeHourEvents: WritableSignal<OfficeHourEventsOverview> = signal({
    current_events: [],
    future_events: []
  });

  constructor(
    private route: ActivatedRoute,
    protected myCoursesService: MyCoursesService
  ) {
    // Load information from the parent route
    let termId = this.route.parent!.snapshot.params['term_id'];
    let courseId = this.route.parent!.snapshot.params['course_id'];

    // Load office hour data
    this.myCoursesService
      .getOfficeHourEventsOverview(termId, courseId)
      .subscribe((overview) => {
        this.officeHourEvents.set(overview);
      });
  }
}
