/**
 * The Current Ticket Page displays a student's current ticket in the queue
 * - Student can edit/delete ticket
 * - Student can see current place in the queue
 * - Student can see upcoming Office Hours Events for that section
 *
 * @author Sadie Amato, Madelyn Andrews, Bailey DeSouza, Meghan Sun
 * @copyright 2024
 * @license MIT
 */

import {
  Component,
  ElementRef,
  OnDestroy,
  OnInit,
  ViewChild
} from '@angular/core';
import { OfficeHoursService } from '../../office-hours.service';
import {
  ActivatedRoute,
  ActivatedRouteSnapshot,
  ResolveFn,
  Router
} from '@angular/router';
import {
  OfficeHoursEvent,
  OfficeHoursEventType,
  OfficeHoursSection,
  Ticket,
  TicketState
} from '../../office-hours.models';
import { Subscription, interval } from 'rxjs';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ohSectionResolver } from '../../office-hours.resolver';

let titleResolver: ResolveFn<string> = (route: ActivatedRouteSnapshot) => {
  return route.parent!.data['section']?.title ?? 'Section Not Found';
};

@Component({
  selector: 'app-current-ticket-page',
  templateUrl: './current-ticket-page.component.html',
  styleUrls: ['./current-ticket-page.component.css']
})
export class CurrentTicketPageComponent implements OnInit, OnDestroy {
  @ViewChild('officeHoursNotif') audioPlayerRef: ElementRef | undefined;
  public static Route = {
    path: ':id/:event_id/ticket/:ticket_id',
    component: CurrentTicketPageComponent,
    canActivate: [],
    resolve: { section: ohSectionResolver },
    children: [
      {
        path: '',
        title: titleResolver,
        component: CurrentTicketPageComponent
      }
    ]
  };

  /* IDs and data relating to a student's current ticket, including the OH section and event */
  sectionId: number;
  eventId: number;
  ticketId: number;
  section: OfficeHoursSection | null = null;
  event!: OfficeHoursEvent;
  ticket!: Ticket;
  refresh: Subscription | undefined;
  called: boolean = false; // used to track when to play a notif sound

  /* Ticket queue stats */
  queued_tickets: number | null;
  called_tickets: number | null;
  queue_spot: number | null;

  constructor(
    private officeHoursService: OfficeHoursService,
    private route: ActivatedRoute,
    private snackBar: MatSnackBar,
    private router: Router
  ) {
    // Get IDs from the route parameters
    this.sectionId = this.route.snapshot.params['id'];
    this.eventId = this.route.snapshot.params['event_id'];
    this.ticketId = this.route.snapshot.params['ticket_id'];

    // Initialize queue stats
    this.queued_tickets = null;
    this.called_tickets = null;
    this.queue_spot = null;

    // Subscribe to observable every 10 seconds and get tickets + stats
    this.refresh = interval(10000).subscribe(() => {
      this.getTicketInfo();
      this.getTicketStats();
    });
  }

  /* On initialization, get the ticket information */
  ngOnInit(): void {
    this.getTicketInfo();
  }

  /* On destruction, unsubscribe from refresh observable */
  ngOnDestroy(): void {
    this.unsubscribeObservables();
  }

  /* Gets ticket information including the associated event and section */
  getTicketInfo() {
    this.officeHoursService.getTicket(this.ticketId).subscribe((ticket) => {
      this.ticket = ticket;
      this.event = ticket.oh_event;
      this.section = ticket.oh_event.oh_section;

      this.getTicketStats();

      // Checks if the ticket state has been changed to called -> plays notif sound
      if (!this.called && this.ticket.state === TicketState.CALLED) {
        this.called = true;
        this.playQueueNotifSound();
      }

      if (this.formatTicketState(this.ticket.state) === 'Closed') {
        this.displayClosedMessage();
        this.navToHome();
        if (this.refresh) {
          this.refresh.unsubscribe();
        }
      }

      if (this.formatTicketState(this.ticket.state) === 'Canceled') {
        this.displayCanceledMessage();
        this.navToHome();
        if (this.refresh) {
          this.refresh.unsubscribe();
        }
      }
    });
  }

  /* Helper function that plays the audio from the officeHoursNotif html element */
  playQueueNotifSound() {
    if (this.audioPlayerRef) {
      this.audioPlayerRef.nativeElement.play();
    }
  }

  formatTicketState(state: number) {
    return this.officeHoursService.formatTicketState(state);
  }

  /* Helper function that navigates back to course home */
  navToHome() {
    this.router.navigate(['office-hours/', this.event.oh_section.id]);
  }

  /* Displays snackbar message if ticket has been canceled */
  displayCanceledMessage() {
    this.snackBar.open('Your ticket has been canceled.', '', {
      duration: 2000
    });
  }

  /* Displays snackbar message if ticket has been closed */
  displayClosedMessage() {
    this.snackBar.open('This ticket has been closed.', '', {
      duration: 2000
    });
  }

  /* Helper function that formats event type enum as string */
  formatEventType(eventType: OfficeHoursEventType) {
    return this.officeHoursService.formatEventType(eventType);
  }

  /* Helper function that gets ticket queue stats */
  getTicketStats() {
    this.officeHoursService
      .getQueueStatsForStudent(this.event.id, this.ticket.id)
      .subscribe((stats) => {
        this.called_tickets = stats.open_tickets_count;
        this.queued_tickets = stats.queued_tickets_count;
        this.queue_spot = stats.ticket_position;
      });
  }

  unsubscribeObservables() {
    if (this.refresh) {
      this.refresh.unsubscribe();
    }
  }
}
