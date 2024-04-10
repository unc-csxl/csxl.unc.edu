import { Component, OnInit } from '@angular/core';
import { OfficeHoursService } from '../office-hours.service';
import { ActivatedRoute } from '@angular/router';
import {
  OfficeHoursEvent,
  OfficeHoursEventDetails,
  OfficeHoursSectionDetails,
  TicketDetails
} from '../office-hours.models';

@Component({
  selector: 'app-current-ticket-page',
  templateUrl: './current-ticket-page.component.html',
  styleUrls: ['./current-ticket-page.component.css']
})
export class CurrentTicketPageComponent implements OnInit {
  public static Route = {
    path: 'spring-2024/:id/:event_id/ticket/:ticket_id',
    title: 'COMP 110: Intro to Programming',
    component: CurrentTicketPageComponent,
    canActivate: []
  };

  sectionId: number;
  eventId: number;
  ticketId: number;
  section: OfficeHoursSectionDetails | null = null;
  event: OfficeHoursEventDetails | null = null;
  ticket: TicketDetails | null = null;

  constructor(
    private officeHoursService: OfficeHoursService,
    private route: ActivatedRoute
  ) {
    this.sectionId = this.route.snapshot.params['id'];
    this.eventId = this.route.snapshot.params['event_id'];
    this.ticketId = this.route.snapshot.params['ticket_id'];
  }

  ngOnInit(): void {
    this.getSection();
    this.getEvent();
    this.getTicket();
  }
  getSection() {
    this.officeHoursService.getSection(this.sectionId).subscribe((section) => {
      this.section = section;
    });
  }

  getEvent() {
    this.officeHoursService.getEvent(this.eventId).subscribe((event) => {
      this.event = event;
    });
  }

  getTicket() {
    this.officeHoursService.getTicket(this.ticketId).subscribe((ticket) => {
      this.ticket = ticket;
    });
  }
}
