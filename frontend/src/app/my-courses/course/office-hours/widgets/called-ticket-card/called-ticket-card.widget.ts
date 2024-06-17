/**
 * The Called Ticket Card widget defines the UI card for
 * a called ticket in an OH queue.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import {
  Component,
  EventEmitter,
  Input,
  Output,
  WritableSignal,
  signal
} from '@angular/core';
import { OfficeHourTicketOverview } from '../../../../my-courses.model';

@Component({
  selector: 'called-ticket-card',
  templateUrl: './called-ticket-card.widget.html',
  styleUrls: ['./called-ticket-card.widget.scss']
})
export class CalledTicketCardWidget {
  @Input() ticket!: OfficeHourTicketOverview;
  @Input() calledByUser: boolean = false;
  @Output() closeButtonPressed = new EventEmitter<OfficeHourTicketOverview>();

  expanded: WritableSignal<boolean> = signal(false);

  constructor() {}

  toggleExpanded() {
    this.expanded.set(!this.expanded());
  }

  closeButtonEvent() {
    this.closeButtonPressed.emit(this.ticket);
  }
}
