/**
 * The Ticket Queue Page allows TAs, GTAs, and Instructors to view an event queue, and
 * call and cancel tickets
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
import {
  TicketDetails,
  OfficeHoursEventDetails,
  OfficeHoursSectionDetails
} from '../office-hours.models';
import { OfficeHoursService } from '../office-hours.service';
import {
  ActivatedRoute,
  ActivatedRouteSnapshot,
  ResolveFn
} from '@angular/router';
import { Subscription, interval } from 'rxjs';
import { sectionResolver } from '../office-hours.resolver';
import { Title } from '@angular/platform-browser';
import { RosterRole } from 'src/app/academics/academics.models';
import { AcademicsService } from 'src/app/academics/academics.service';

let titleResolver: ResolveFn<string> = (route: ActivatedRouteSnapshot) => {
  return route.parent!.data['section']?.title ?? 'Section Not Found';
};

@Component({
  selector: 'app-ticket-queue-page',
  templateUrl: './ticket-queue-page.component.html',
  styleUrls: ['./ticket-queue-page.component.css']
})
export class TicketQueuePageComponent implements OnInit, OnDestroy {
  @ViewChild('officeHoursNotif') audioPlayerRef: ElementRef | undefined;
  public static Routes = [
    {
      path: 'ta/:id/:event_id/queue',
      component: TicketQueuePageComponent,
      canActivate: [],
      resolve: { section: sectionResolver },
      children: [
        {
          path: '',
          title: titleResolver,
          component: TicketQueuePageComponent
        }
      ]
    },
    {
      path: 'instructor/:id/:event_id/queue',
      component: TicketQueuePageComponent,
      canActivate: [],
      resolve: { section: sectionResolver },
      children: [
        {
          path: '',
          title: titleResolver,
          component: TicketQueuePageComponent
        }
      ]
    }
  ];

  /* Tickets currently in the TicketQueue */
  protected tickets: TicketDetails[] = [];

  /* Office Hours Event queue is associated with */
  eventId: number;
  event: OfficeHoursEventDetails | null = null;

  /* Office Hours Section that event belongs to */
  sectionId: number;
  protected section: OfficeHoursSectionDetails | null = null;
  queued_tickets: number | null;
  called_tickets: number | null;

  /* Stores refresh interval subscription so that it can be unsubscribed from */
  refresh: Subscription | undefined;

  /* Stores title interval subscription so that it can be unsubscribed from */
  titleNotif: Subscription | undefined;

  /* Stores default tab title to revert when no new tickets are in queue */
  defaultTabTitle: string = '';

  /* Highest ticket ID in most recent refresh */
  prevHighestTicketId: number = Number.MAX_VALUE;

  // Stores the user's RosterRole (to determine if they should be allowed to view the queue page)
  rosterRole: RosterRole | undefined;

  constructor(
    private officeHoursService: OfficeHoursService,
    private academicsService: AcademicsService,
    private route: ActivatedRoute,
    protected tabTitle: Title
  ) {
    // Retrieves IDs from route parameters
    this.eventId = this.route.snapshot.params['event_id'];
    this.sectionId = this.route.snapshot.params['id'];
    this.queued_tickets = null;
    this.called_tickets = null;

    // checks rosterRole
    this.getRosterRole();

    /** Initialize data from resolvers. */
    const data = this.route.snapshot.data as {
      section: OfficeHoursSectionDetails;
    };
    this.section = data.section;

    // Subscribe to observable every 10 seconds and get tickets + stats
    this.refresh = interval(10000).subscribe(() => {
      this.getCurrentTickets();
      this.getEvent();
      this.getTicketStats();

      // If there are no queued tickets, set tab title back to default
      if (this.queued_tickets === 0) {
        if (this.titleNotif) {
          this.titleNotif.unsubscribe();
        }
        this.tabTitle.setTitle(this.defaultTabTitle);
      }

      // If there are new tickets in the queue, change tab title on an interval
      if (this.getHighestTicketId() > this.prevHighestTicketId) {
        // Play the notif sound if a new ticket has been added to the queue
        this.playQueueNotifSound();
        this.titleNotif = interval(1500).subscribe((tick) => {
          if (tick % 2 === 0) {
            this.tabTitle.setTitle('• New Ticket •');
          } else {
            this.tabTitle.setTitle(this.defaultTabTitle);
          }
        });
      }

      // Set new highest ticket ID
      this.prevHighestTicketId = this.getHighestTicketId();
    });
  }

  /* On initialization, get event, section, and ticket stats */
  ngOnInit() {
    this.getEvent();
    this.getSection();
    this.getTicketStats();
    // Store default tab title
    this.defaultTabTitle = this.tabTitle.getTitle();
  }

  ngOnDestroy(): void {
    this.unsubscribeObservables();
  }

  /* Helper function that plays the audio from the officeHoursNotif html element */
  playQueueNotifSound() {
    if (this.audioPlayerRef) {
      this.audioPlayerRef.nativeElement.play();
    }
  }

  getRosterRole() {
    this.academicsService
      .getMembershipBySection(this.sectionId)
      .subscribe((role) => (this.rosterRole = role.member_role));
  }

  /* Gets current tickets that are in the queue */
  getCurrentTickets() {
    if (this.event) {
      this.officeHoursService
        .getEventQueueTickets(this.event)
        .subscribe((tickets) => {
          this.tickets = tickets;
        });
    }
  }

  /* Gets ongoing event that the ticket queue belongs to */
  getEvent() {
    this.officeHoursService
      .getEvent(this.eventId)
      // .subscribe((event) => (this.event = event));
      .subscribe((event) => {
        (this.event = event), this.getCurrentTickets();
      });
  }

  /* Gets section that is holding the OH Event */
  getSection() {
    this.officeHoursService.getSection(this.sectionId).subscribe((section) => {
      this.section = section;
    });
  }

  /** Helper function which formats event type enum to a string
   * @param typeNum: OfficeHoursEventType enum value
   * @returns formatted event type (string)
   */
  formatEventType(typeNum: number) {
    return this.officeHoursService.formatEventType(typeNum);
  }

  /* Gets queue stats, including # of tickets being helped and # of tickets waiting in queue */
  getTicketStats() {
    this.officeHoursService
      .getQueuedAndCalledTicketCount(this.eventId)
      .subscribe((event_status) => {
        this.called_tickets = event_status.open_tickets_count;
        this.queued_tickets = event_status.queued_tickets_count;
      });
  }

  unsubscribeObservables() {
    if (this.refresh) {
      this.refresh.unsubscribe();
    }
    if (this.titleNotif) {
      this.titleNotif.unsubscribe();
    }
  }

  getHighestTicketId(): number {
    return this.tickets.at(this.tickets.length - 1)?.id ?? -1;
  }
}
