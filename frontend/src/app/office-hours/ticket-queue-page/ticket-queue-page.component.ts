import { Component, OnInit } from '@angular/core';
import {
  TicketDetails,
  OfficeHoursEventDetails,
  OfficeHoursEventType
} from '../office-hours.models';
import { OfficeHoursService } from '../office-hours.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-ticket-queue-page',
  templateUrl: './ticket-queue-page.component.html',
  styleUrls: ['./ticket-queue-page.component.css']
})
export class TicketQueuePageComponent implements OnInit {
  // TODO: Update this route later to not be hard-coded!
  public static Route = {
    path: 'spring-2024/1/:event_id/queue',
    title: 'COMP 110: Intro to Programming',
    component: TicketQueuePageComponent,
    canActivate: []
  };

  protected tickets: TicketDetails[] = [];
  // TODO: update this to get the eventId from the route!
  eventId: number;
  event: OfficeHoursEventDetails | null = null;
  // TODO: Store event details object and pass this in as input!

  constructor(
    private officeHoursService: OfficeHoursService,
    private route: ActivatedRoute
  ) {
    this.eventId = this.route.snapshot.params['event_id'];
  }

  ngOnInit() {
    this.getEvent();
  }

  getCurrentTickets() {
    if (this.event) {
      this.officeHoursService
        .getEventQueueTickets(this.event)
        .subscribe((tickets) => (this.tickets = tickets));
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

  formatEventType(typeNum: number) {
    if (typeNum === OfficeHoursEventType.OFFICE_HOURS) {
      return 'Office Hours';
    } else if (typeNum === OfficeHoursEventType.TUTORING) {
      return 'Tutoring';
    } else if (typeNum === OfficeHoursEventType.REVIEW_SESSION) {
      return 'Review Session';
    } else if (typeNum === OfficeHoursEventType.VIRTUAL_OFFICE_HOURS) {
      return 'Virtual Office Hours';
    } else if (typeNum === OfficeHoursEventType.VIRTUAL_TUTORING) {
      return 'Virtual Tutoring';
    } else if (typeNum === OfficeHoursEventType.VIRTUAL_REVIEW_SESSION) {
      return 'Virtual Review Session';
    } else {
      return 'error';
    }
  }
}
