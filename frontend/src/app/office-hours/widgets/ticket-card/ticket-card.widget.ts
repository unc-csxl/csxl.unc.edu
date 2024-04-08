import { Component, Input } from '@angular/core';
import { Ticket, TicketDetails, TicketType } from '../../office-hours.models';
import { OfficeHoursService } from '../../office-hours.service';

@Component({
  selector: 'ticket-card-widget',
  templateUrl: './ticket-card.widget.html',
  styleUrls: ['./ticket-card.widget.css']
})
export class TicketCard {
  @Input() ticket!: TicketDetails;
  constructor(private officeHoursService: OfficeHoursService) {}

  formatTicketType(typeNum: number) {
    return this.officeHoursService.formatTicketType(typeNum);
  }

  formatTicketState(typeNum: number) {
    return this.officeHoursService.formatTicketState(typeNum);
  }
}
