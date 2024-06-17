/**
 * The Called Ticket Card widget defines the UI card for
 * a queued ticket in an OH queue.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { Component, Input, WritableSignal, signal } from '@angular/core';
import { OfficeHourTicketOverview } from '../../../../my-courses.model';

@Component({
  selector: 'queued-ticket-card',
  templateUrl: './queued-ticket-card.widget.html',
  styleUrls: ['./queued-ticket-card.widget.scss']
})
export class QueuedTicketCardWidget {
  @Input() ticket!: OfficeHourTicketOverview;
}
