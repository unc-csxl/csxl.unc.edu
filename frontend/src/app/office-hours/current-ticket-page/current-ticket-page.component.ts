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

import { Component, OnInit } from '@angular/core';
import { OfficeHoursService } from '../office-hours.service';
import { ActivatedRoute } from '@angular/router';
import {
  OfficeHoursEvent,
  OfficeHoursSection,
  Ticket
} from '../office-hours.models';
import { interval } from 'rxjs';

@Component({
  selector: 'app-current-ticket-page',
  templateUrl: './current-ticket-page.component.html',
  styleUrls: ['./current-ticket-page.component.css']
})
export class CurrentTicketPageComponent implements OnInit {
  // TODO: Un-hardcode 'spring-2024'
  public static Route = {
    path: 'spring-2024/:id/:event_id/ticket/:ticket_id',
    title: 'COMP 110: Intro to Programming',
    component: CurrentTicketPageComponent,
    canActivate: []
  };

  sectionId: number;
  eventId: number;
  ticketId: number;
  section: OfficeHoursSection | null = null;
  event: OfficeHoursEvent | null = null;
  ticket: Ticket | null = null;

  constructor(
    private officeHoursService: OfficeHoursService,
    private route: ActivatedRoute
  ) {
    this.sectionId = this.route.snapshot.params['id'];
    this.eventId = this.route.snapshot.params['event_id'];
    this.ticketId = this.route.snapshot.params['ticket_id'];
    let refresh = interval(10000).subscribe(() => {
      let prevState = this.ticket;
      this.getTicketInfo();
      if (this.ticket !== prevState) {
        this.ngOnInit();
      }
    });
  }

  ngOnInit(): void {
    this.getTicketInfo();
  }

  getTicketInfo() {
    this.officeHoursService.getTicket(this.ticketId).subscribe((ticket) => {
      this.ticket = ticket;
      this.event = ticket.oh_event;
      this.section = ticket.oh_event.oh_section;
    });
  }
}
