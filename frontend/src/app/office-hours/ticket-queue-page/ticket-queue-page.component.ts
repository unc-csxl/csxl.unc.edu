/**
 * The Ticket Queue Page allows TAs, GTAs, and Instructors to view an event queue, and
 * call and cancel tickets
 *
 * @author Sadie Amato, Madelyn Andrews, Bailey DeSouza, Meghan Sun
 * @copyright 2024
 * @license MIT
 */

import { Component, OnInit } from '@angular/core';
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

let titleResolver: ResolveFn<string> = (route: ActivatedRouteSnapshot) => {
  return route.parent!.data['section']?.title ?? 'Section Not Found';
};

@Component({
  selector: 'app-ticket-queue-page',
  templateUrl: './ticket-queue-page.component.html',
  styleUrls: ['./ticket-queue-page.component.css']
})
export class TicketQueuePageComponent implements OnInit {
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

  refresh: Subscription | undefined;

  constructor(
    private officeHoursService: OfficeHoursService,
    private route: ActivatedRoute
  ) {
    // Retrieves IDs from route parameters
    this.eventId = this.route.snapshot.params['event_id'];
    this.sectionId = this.route.snapshot.params['id'];
    this.queued_tickets = null;
    this.called_tickets = null;

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
      console.log('here');
    });
  }

  /* On initialization, get event, section, and ticket stats */
  ngOnInit() {
    this.getEvent();
    this.getSection();
    this.getTicketStats();
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

  unsubscribeRefresh() {
    if (this.refresh) {
      this.refresh.unsubscribe();
    }
  }
}
