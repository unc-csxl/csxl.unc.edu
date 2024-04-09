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
  @Input() queuePosition!: number;
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

  callTicket() {
    this.officeHoursService.callTicket(this.ticket).subscribe(() => {
      // remove this later!
      window.location.reload();
    });
  }

  closeTicket() {
    this.officeHoursService.closeTicket(this.ticket).subscribe(() => {
      window.location.reload();
    });
  }
}
