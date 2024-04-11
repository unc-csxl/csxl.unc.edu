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
import { ActivatedRoute } from '@angular/router';
import { interval } from 'rxjs';

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
      title: 'COMP 110: Intro to Programming',
      component: TicketQueuePageComponent,
      canActivate: []
    },
    {
      path: 'instructor/spring-2024/:section_id/:event_id/queue',
      title: 'COMP 110: Intro to Programming',
      component: TicketQueuePageComponent,
      canActivate: []
    }
  ];

  protected tickets: TicketDetails[] = [];
  // TODO: update this to get the eventId from the route!
  eventId: number;
  event: OfficeHoursEventDetails | null = null;
  sectionId: number;
  section: OfficeHoursSectionDetails | null = null;
  // TODO: Store event details object and pass this in as input!

  constructor(
    private officeHoursService: OfficeHoursService,
    private route: ActivatedRoute
  ) {
    this.eventId = this.route.snapshot.params['event_id'];
    this.sectionId = this.route.snapshot.params['section_id'];
  }

  ngOnInit() {
    this.getEvent();
    this.getSection();
  }

  getCurrentTickets() {
    if (this.event) {
      this.officeHoursService
        .getEventQueueTickets(this.event)
        .subscribe((tickets) => {
          this.tickets = tickets;
          console.log(tickets);
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
}
