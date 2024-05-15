/**
 * The Ticket Card widget abstracts ticket details and implementation
 * away from the ticket queue component
 *
 * @author Sadie Amato, Madelyn Andrews, Bailey DeSouza, Meghan Sun
 * @copyright 2024
 * @license MIT
 */

import { Component, Input } from '@angular/core';
import {
  Ticket,
  TicketDetails,
  TicketType
} from '../../../office-hours.models';
import { OfficeHoursService } from '../../../office-hours.service';
import { MatDialog } from '@angular/material/dialog';
import { TicketFeedbackDialog } from '../ticket-feedback-dialog/ticket-feedback-dialog.widget';

@Component({
  selector: 'ticket-card-widget',
  templateUrl: './ticket-card.widget.html',
  styleUrls: ['./ticket-card.widget.css']
})
export class TicketCard {
  @Input() ticket!: TicketDetails;
  @Input() queuePosition!: number;
  constructor(
    private officeHoursService: OfficeHoursService,
    public dialog: MatDialog
  ) {}

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

  openTicketFeedbackFormDialog() {
    const dialogRef = this.dialog.open(TicketFeedbackDialog, {
      height: 'auto',
      width: 'auto',
      data: { ticket: this.ticket }
    });

    dialogRef.afterClosed().subscribe((open) => {
      if (!open) {
        window.location.reload();
      }
    });
  }
}
