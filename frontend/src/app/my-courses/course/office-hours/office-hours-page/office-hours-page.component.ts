import { Component, WritableSignal, signal } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { OfficeHourEventOverview } from 'src/app/my-courses/my-courses.model';
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

  /** Stores the view state enum and view state. */
  ViewState = OfficeHoursPageComponent.ViewState;
  viewState = OfficeHoursPageComponent.ViewState.Scheduled;

  /** Signal to store the reactive office hour overview information */
  currentOfficeHourEvents: WritableSignal<OfficeHourEventOverview[]> = signal(
    []
  );

  constructor(
    private route: ActivatedRoute,
    protected myCoursesService: MyCoursesService
  ) {
    // Load information from the parent route
    let termId = this.route.parent!.snapshot.params['term_id'];
    let courseId = this.route.parent!.snapshot.params['course_id'];

    // Load office hour data
    this.myCoursesService
      .getCurrentOfficeHourEvents(termId, courseId)
      .subscribe((overview) => {
        this.currentOfficeHourEvents.set(overview);
      });
  }
}

export namespace OfficeHoursPageComponent {
  /** Enumeration for the view states */
  export enum ViewState {
    Scheduled,
    History,
    Data
  }
}
