/**
 * The Current Ticket widget abstracts the implementation of a student's current ticket
 * information card away from the Current Ticket Page
 *
 * @author Sadie Amato, Madelyn Andrews, Bailey DeSouza, Meghan Sun
 * @copyright 2024
 * @license MIT
 */

import { Component, Input } from '@angular/core';
import { OfficeHoursEvent, TicketDetails } from '../../office-hours.models';
import { OfficeHoursService } from '../../office-hours.service';
import { MatDialog } from '@angular/material/dialog';
import { DeleteTicketDialog } from '../delete-ticket-dialog/delete-ticket-dialog.widget';

@Component({
  selector: 'current-ticket-card-widget',
  templateUrl: './current-ticket-card.widget.html',
  styleUrls: ['./current-ticket-card.widget.css']
})
export class CurrentTicketCard {
  /* TicketDetails and Event to display on widget */
  @Input() ticket!: TicketDetails;
  @Input() event!: OfficeHoursEvent;

  constructor(
    private officeHoursService: OfficeHoursService,
    public dialog: MatDialog
  ) {}

  /* Helper function that formats ticket type enum */
  formatTicketType(typeNum: number) {
    return this.officeHoursService.formatTicketType(typeNum);
  }

  /* Helper function that formats ticket state enum */
  formatTicketState(typeNum: number) {
    return this.officeHoursService.formatTicketState(typeNum);
  }

  /* Cancels ticket and navigates user back to section home */
  cancelTicket() {
    const dialogRef = this.dialog.open(DeleteTicketDialog, {
      height: 'auto',
      width: 'auto',
      data: { ticket: this.ticket, event: this.event }
    });
  }
}
