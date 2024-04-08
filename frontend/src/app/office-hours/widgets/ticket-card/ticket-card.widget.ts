import { Component, Input } from '@angular/core';
import { Ticket, TicketType } from '../../office-hours.models';

@Component({
  selector: 'ticket-card-widget',
  templateUrl: './ticket-card.widget.html',
  styleUrls: ['./ticket-card.widget.css']
})
export class TicketCard {
  @Input() ticket!: Ticket;
  constructor() {}

  formatTicketType(typeNum: number) {
    if (typeNum === TicketType.ASSIGNMENT_HELP) {
      return 'Assignment Help';
    } else return 'Conceptual Help';
  }
}
