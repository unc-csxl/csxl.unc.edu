import { Component, Input } from '@angular/core';
import {
  OfficeHoursEventDetails,
  Ticket,
  TicketDetails,
  TicketType
} from '../../office-hours.models';
import { OfficeHoursService } from '../../office-hours.service';

@Component({
  selector: 'current-ticket-card-widget',
  templateUrl: './current-ticket-card.widget.html',
  styleUrls: ['./current-ticket-card.widget.css']
})
export class CurrentTicketCard {
  @Input() ticket!: TicketDetails;
  @Input() event!: OfficeHoursEventDetails;
  constructor(private officeHoursService: OfficeHoursService) {}

  formatTicketType(typeNum: number) {
    return this.officeHoursService.formatTicketType(typeNum);
  }

  formatTicketState(typeNum: number) {
    return this.officeHoursService.formatTicketState(typeNum);
  }

  cancelTicket() {
    this.officeHoursService.cancelTicket(this.ticket).subscribe(() => {
      // remove this later!
      window.location.reload();
    });
  }
}
