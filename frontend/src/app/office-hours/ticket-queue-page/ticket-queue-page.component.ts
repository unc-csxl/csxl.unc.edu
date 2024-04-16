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
  OfficeHoursEventType,
  OfficeHoursSectionDetails
} from '../office-hours.models';
import { OfficeHoursService } from '../office-hours.service';
import {
  ActivatedRoute,
  ActivatedRouteSnapshot,
  ResolveFn
} from '@angular/router';
import { interval } from 'rxjs';
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
  // TODO: Update this route later to not be hard-coded!
  public static Routes = [
    {
      path: 'ta/spring-2024/:section_id/:event_id/queue',
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
      path: 'instructor/spring-2024/:section_id/:event_id/queue',
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

  protected tickets: TicketDetails[] = [];
  // TODO: update this to get the eventId from the route!
  eventId: number;
  event: OfficeHoursEventDetails | null = null;
  sectionId: number;
  protected section: OfficeHoursSectionDetails | null = null;
  queued_tickets: number | null;
  called_tickets: number | null;
  // TODO: Store event details object and pass this in as input!

  constructor(
    private officeHoursService: OfficeHoursService,
    private route: ActivatedRoute
  ) {
    this.eventId = this.route.snapshot.params['event_id'];
    this.sectionId = this.route.snapshot.params['section_id'];
    this.queued_tickets = null;
    this.called_tickets = null;

    /** Initialize data from resolvers. */
    const data = this.route.snapshot.data as {
      section: OfficeHoursSectionDetails;
    };
    this.section = data.section;

    // subscribe to observable every 10 seconds and get tickets + stats
    let refresh = interval(10000).subscribe(() => {
      this.getTicketStats();
      this.getEvent();
    });
  }

  ngOnInit() {
    this.getEvent();
    this.getSection();
    this.getTicketStats();
  }

  getCurrentTickets() {
    if (this.event) {
      this.officeHoursService
        .getEventQueueTickets(this.event)
        .subscribe((tickets) => {
          this.tickets = tickets;
        });
    }
  }

  getEvent() {
    this.officeHoursService
      .getEvent(this.eventId)
      // .subscribe((event) => (this.event = event));
      .subscribe((event) => {
        (this.event = event), this.getCurrentTickets();
      });
  }

  getSection() {
    this.officeHoursService.getSection(this.sectionId).subscribe((section) => {
      this.section = section;
    });
  }

  formatEventType(typeNum: number) {
    return this.officeHoursService.formatEventType(typeNum);
  }

  getTicketStats() {
    this.officeHoursService
      .getQueuedAndCalledTicketCount(this.eventId)
      .subscribe((event_status) => {
        this.called_tickets = event_status.open_tickets_count;
        this.queued_tickets = event_status.queued_tickets_count;
      });
  }
}