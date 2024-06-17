import { Component } from '@angular/core';
import { officeHourPageGuard } from '../office-hours.guard';
import { ActivatedRoute } from '@angular/router';
import { MyCoursesService } from 'src/app/my-courses/my-courses.service';

@Component({
  selector: 'app-office-hours-get-help',
  templateUrl: './office-hours-get-help.component.html',
  styleUrl: './office-hours-get-help.component.css'
})
export class OfficeHoursGetHelpComponent {
  /** Route information to be used in the routing module */
  public static Route = {
    path: 'office-hours/:event_id/get-help',
    title: 'Office Hours Get Help',
    component: OfficeHoursGetHelpComponent,
    canActivate: [officeHourPageGuard(['STUDENT'])]
  };

  /** Office hour event ID to load the queue for */
  ohEventId: number;

  /** Encapsulated signal to store the queue data */
  // queue: WritableSignal<OfficeHourQueueOverview | undefined> =
  //   signal(undefined);

  /** Stores subscription to the timer observable that refreshes data every 10s */
  // timer!: Subscription;

  constructor(
    private route: ActivatedRoute,
    protected myCoursesService: MyCoursesService
  ) {
    // Load information from the parent route
    this.ohEventId = this.route.snapshot.params['event_id'];
  }
}
