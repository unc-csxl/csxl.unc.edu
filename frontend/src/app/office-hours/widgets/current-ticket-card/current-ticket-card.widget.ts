/**
 * The Current Ticket widget abstracts the implementation of a student's current ticket
 * information card away from the Current Ticket Page
 *
 * @author Sadie Amato, Madelyn Andrews, Bailey DeSouza, Meghan Sun
 * @copyright 2024
 * @license MIT
 */

import { Component, Input } from '@angular/core';
import {
  OfficeHoursEvent,
  OfficeHoursEventDetails,
  OfficeHoursEventType,
  Ticket,
  TicketDetails,
  TicketType
} from '../../office-hours.models';
import { OfficeHoursService } from '../../office-hours.service';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { config } from 'rxjs';

@Component({
  selector: 'current-ticket-card-widget',
  templateUrl: './current-ticket-card.widget.html',
  styleUrls: ['./current-ticket-card.widget.css']
})
export class CurrentTicketCard {
  @Input() ticket!: TicketDetails;
  @Input() event!: OfficeHoursEvent;
  constructor(
    private officeHoursService: OfficeHoursService,
    private router: Router,
    private snackBar: MatSnackBar
  ) {}

  formatTicketType(typeNum: number) {
    return this.officeHoursService.formatTicketType(typeNum);
  }

  formatTicketState(typeNum: number) {
    return this.officeHoursService.formatTicketState(typeNum);
  }

  cancelTicket() {
    this.officeHoursService.cancelTicket(this.ticket).subscribe(() => {
      this.displayCanceledMessage();
      this.navToHome();
    });
  }

  formatEventType(eventType: OfficeHoursEventType) {
    return this.officeHoursService.formatEventType(eventType);
  }

  navToHome() {
    this.router.navigate([
      'office-hours/spring-2024/',
      this.event.oh_section.id
    ]);
  }

  displayCanceledMessage() {
    this.snackBar.open('Your ticket has been canceled.', '', {
      duration: 2000
    });
  }
}
