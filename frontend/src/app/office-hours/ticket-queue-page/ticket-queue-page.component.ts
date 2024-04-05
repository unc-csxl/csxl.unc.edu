import { Component, OnInit } from '@angular/core';
import { TicketDetails, OfficeHoursEventDetails } from '../office-hours.models';
import { OfficeHoursService } from '../office-hours.service';

@Component({
  selector: 'app-ticket-queue-page',
  templateUrl: './ticket-queue-page.component.html',
  styleUrls: ['./ticket-queue-page.component.css']
})
export class TicketQueuePageComponent implements OnInit {
  // TODO: Update this route later to not be hard-coded!
  public static Route = {
    path: 'spring-2024/1/event_id/queue',
    title: 'COMP 110: Intro to Programming',
    component: TicketQueuePageComponent,
    canActivate: []
  };

  protected tickets: TicketDetails[] = [];
  // TODO: update this to get the eventId from the route!
  eventId: number = 1;
  // TODO: Store event details object and pass this in as input!

  constructor(private officeHoursService: OfficeHoursService) {}

  ngOnInit() {
    this.getCurrentTickets();
  }

  getCurrentTickets() {}
}
