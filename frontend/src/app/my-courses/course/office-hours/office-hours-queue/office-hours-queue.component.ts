import {
  Component,
  OnDestroy,
  OnInit,
  WritableSignal,
  signal
} from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Subscription, timer } from 'rxjs';
import { OfficeHourQueueOverview } from 'src/app/my-courses/my-courses.model';
import { MyCoursesService } from 'src/app/my-courses/my-courses.service';

@Component({
  selector: 'app-office-hours-queue',
  templateUrl: './office-hours-queue.component.html',
  styleUrl: './office-hours-queue.component.css'
})
export class OfficeHoursQueueComponent implements OnInit, OnDestroy {
  /** Route information to be used in the routing module */
  public static Route = {
    path: 'office-hours/:event_id/queue',
    title: 'Office Hours Queue',
    component: OfficeHoursQueueComponent
  };

  /** Office hour event ID to load the queue for */
  ohEventId: number;

  /** Encapsulated signal to store the queue data */
  queue: WritableSignal<OfficeHourQueueOverview | undefined> =
    signal(undefined);

  /** Stores subscription to the timer observable that refreshes data every 10s */
  timer!: Subscription;

  constructor(
    private route: ActivatedRoute,
    protected myCoursesService: MyCoursesService
  ) {
    // Load information from the parent route
    this.ohEventId = this.route.snapshot.params['event_id'];
  }

  ngOnInit(): void {
    // Create a timer subscription to poll office hour queue data at an interval
    this.timer = timer(0, 10000).subscribe(() => {
      // Set the data
      this.myCoursesService
        .getOfficeHoursQueue(this.ohEventId)
        .subscribe((queue) => {
          this.queue.set(queue);
        });
    });
  }

  ngOnDestroy(): void {
    this.timer.unsubscribe();
  }
}
