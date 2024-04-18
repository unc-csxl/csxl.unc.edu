/**
 * The Current Ticket widget abstracts the implementation of a student's current ticket
 * information card away from the Current Ticket Page
 *
 * @author Sadie Amato, Madelyn Andrews, Bailey DeSouza, Meghan Sun
 * @copyright 2024
 * @license MIT
 */

import { Component, Input, OnInit } from '@angular/core';
import {
  OfficeHoursEvent,
  OfficeHoursEventType,
  TicketDetails
} from '../../office-hours.models';
import { OfficeHoursService } from '../../office-hours.service';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatDialog } from '@angular/material/dialog';
import { DeleteTicketDialog } from '../delete-ticket-dialog/delete-ticket-dialog.widget';

@Component({
  selector: 'current-ticket-card-widget',
  templateUrl: './current-ticket-card.widget.html',
  styleUrls: ['./current-ticket-card.widget.css']
})
export class CurrentTicketCard implements OnInit {
  @Input() ticket!: Ticket;
  @Input() event!: OfficeHoursEvent;
  /* Ticket queue stats */
  queued_tickets: number | null;
  called_tickets: number | null;
  queue_spot: number | null;

  constructor(
    private officeHoursService: OfficeHoursService,
    private router: Router,
    private snackBar: MatSnackBar,
    public dialog: MatDialog
  ) {
    this.queued_tickets = null;
    this.called_tickets = null;
    this.queue_spot = null;
  }

  ngOnInit(): void {
    this.getTicketStats();
  }

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

  /* Helper function that formats event type enum as string */
  formatEventType(eventType: OfficeHoursEventType) {
    return this.officeHoursService.formatEventType(eventType);
  }

  /* Helper function that navigates back to course home */
  navToHome() {
    this.router.navigate([
      'office-hours/spring-2024/',
      this.event.oh_section.id
    ]);
  }

  /* Displays snackbar message if ticket has been canceled */
  displayCanceledMessage() {
    this.snackBar.open('Your ticket has been canceled.', '', {
      duration: 2000
    });
  }

  /* Displays snackbar message if ticket has been closed */
  displayClosedMessage() {
    this.snackBar.open('This ticket has been closed.', '', {
      duration: 2000
    });
  }

  /* Helper function that gets ticket queue stats */
  getTicketStats() {
    this.officeHoursService
      .getQueueStatsForStudent(this.event.id, this.ticket.id)
      .subscribe((stats) => {
        this.called_tickets = stats.open_tickets_count;
        this.queued_tickets = stats.queued_tickets_count;
        this.queue_spot = stats.ticket_position;
      });
  }
}
