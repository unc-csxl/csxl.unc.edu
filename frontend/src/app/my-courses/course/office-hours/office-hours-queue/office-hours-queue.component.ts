/**
 * Office hours queue for instructors.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import {
  Component,
  OnDestroy,
  OnInit,
  WritableSignal,
  signal
} from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ActivatedRoute } from '@angular/router';
import { Subscription, timer } from 'rxjs';
import {
  OfficeHourQueueOverview,
  OfficeHourQueueOverviewJson,
  OfficeHourTicketOverview,
  parseOfficeHourQueueOverview,
  QueueWebSocketAction,
  QueueWebSocketData
} from 'src/app/my-courses/my-courses.model';
import { MyCoursesService } from 'src/app/my-courses/my-courses.service';
import { officeHourPageGuard } from '../office-hours.guard';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { Title } from '@angular/platform-browser';
import { MatDialog } from '@angular/material/dialog';
import { CloseTicketDialog } from '../widgets/close-ticket-dialog/close-ticket.dialog';

/** Store both possible titles as strings to flash between them easily */
const ORIGINAL_TITLE: string = 'Office Hours Queue';
const NOTIFICATION_TITLE: string = 'Queued Ticket!';

/** Store notification audio */
const CHIME = new Audio('assets/office-hours-notif.wav');

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
    component: OfficeHoursQueueComponent,
    canActivate: [officeHourPageGuard(['UTA', 'GTA', 'Instructor'])]
  };

  /** Office hour event ID to load the queue for */
  ohEventId: number;

  /** Encapsulated signal to store the queue data */
  queue: WritableSignal<OfficeHourQueueOverview | undefined> =
    signal(undefined);

  /** Stores subscription to the timer observable that refreshes data every 10s */
  timer!: Subscription;

  /** Connection to the office hours get help websocket */
  webSocketSubject$: WebSocketSubject<any>;
  /** Stores subscription to a timer observable for flashing the title for notifications */
  titleFlashTimer: Subscription | undefined;

  constructor(
    private route: ActivatedRoute,
    private snackBar: MatSnackBar,
    protected myCoursesService: MyCoursesService,
    private titleService: Title,
    protected dialog: MatDialog
  ) {
    // Load information from the parent route
    this.ohEventId = this.route.snapshot.params['event_id'];
    // Load the web socket
    const url = `wss://${window.location.host}/ws/office-hours/${this.ohEventId}/queue?token=${localStorage.getItem('bearerToken')}`;
    this.webSocketSubject$ = webSocket({
      url: url
    });
  }

  ngOnInit(): void {
    this.webSocketSubject$.subscribe((value) => {
      const json: OfficeHourQueueOverviewJson = JSON.parse(value);
      const overview = parseOfficeHourQueueOverview(json);
      this.queue.set(overview);
    });
  }

  /** Create a timer subscription to poll office hour queue data at an interval at view initalization */
  // ngOnInit(): void {
  //   this.timer = timer(0, 10000).subscribe(() => {
  //     this.pollQueue();
  //   });
  // }

  /** Remove the timer subscriptions when the view is destroyed so polling/flashing does not persist on other pages */
  ngOnDestroy(): void {
    this.webSocketSubject$.complete();
    this.timer.unsubscribe();
    this.titleFlashTimer?.unsubscribe();
  }

  /** Sends a notification if necessary on each pollQueue call */
  handleNotification(queue: OfficeHourQueueOverview): void {
    /**
     * If you have no active/called ticket and the new queue has some ticket
     * queued and either the old queue doesn't exist, it has a length of zero,
     * or the new queue has a ticket that wasn't in the old queue, then send
     * a notification. If not, stop the flashing subscription (if it exists).
     */
    let notify: boolean = false;
    /* Test notification condition and store result in notify */
    if (!queue.active && queue.queue.length > 0) {
      if (!this.queue() || this.queue()!.queue.length === 0) {
        notify = true;
      } else {
        for (const new_ticket of queue.queue) {
          if (
            !this.queue()!.queue.some(
              (old_ticket) => new_ticket.id === old_ticket.id
            )
          ) {
            notify = true;
            break;
          }
        }
      }
    }
    /* Notification behavior based on result stored in notify */

    if (notify) {
      CHIME.play();
      this.titleFlashTimer = timer(0, 1000).subscribe(() => {
        this.titleService.setTitle(
          this.titleService.getTitle() === NOTIFICATION_TITLE
            ? ORIGINAL_TITLE
            : NOTIFICATION_TITLE
        );
      });
    } else {
      this.titleFlashTimer?.unsubscribe();
      this.titleService.setTitle(ORIGINAL_TITLE);
    }
  }

  /** Loads office hours queue data */
  pollQueue(): void {
    this.myCoursesService
      .getOfficeHoursQueue(this.ohEventId)
      .subscribe((queue) => {
        this.handleNotification(queue);
        this.queue.set(queue);
      });
  }

  /** Calls a ticket and reloads the queue data */
  callTicket(ticket: OfficeHourTicketOverview): void {
    // Create the web socket object
    const action: QueueWebSocketData = {
      action: QueueWebSocketAction.CALL,
      id: ticket.id
    };
    this.webSocketSubject$.next(action);

    // this.myCoursesService.callTicket(ticket.id).subscribe({
    //   next: (_) => this.pollQueue(),
    //   error: (err) => this.snackBar.open(err, '', { duration: 2000 })
    // });
  }

  /** Cancels a ticket and reloads the queue data */
  cancelTicket(ticket: OfficeHourTicketOverview): void {
    // Create the web socket object
    const action: QueueWebSocketData = {
      action: QueueWebSocketAction.CANCEL,
      id: ticket.id
    };
    this.webSocketSubject$.next(action);

    // this.myCoursesService.cancelTicket(ticket.id).subscribe({
    //   next: (_) => this.pollQueue(),
    //   error: (err) => this.snackBar.open(err, '', { duration: 2000 })
    // });
  }

  /** Closes a ticket and reloads the queue data */
  closeTicket(ticket: OfficeHourTicketOverview): void {
    // Create the web socket object
    const action: QueueWebSocketData = {
      action: QueueWebSocketAction.CLOSE,
      id: ticket.id
    };
    this.webSocketSubject$.next(action);

    // this.myCoursesService.closeTicket(ticket.id).subscribe({
    //   next: (_) => this.pollQueue(),
    //   error: (err) => this.snackBar.open(err, '', { duration: 2000 })
    // });

    // let dialogRef = this.dialog.open(CloseTicketDialog, {
    //   height: '400px',
    //   width: '500px',
    //   data: ticket.id
    // });
    // dialogRef.afterClosed().subscribe((_) => {
    //   // Update the data.
    //   this.pollQueue();
    // });
  }
}
