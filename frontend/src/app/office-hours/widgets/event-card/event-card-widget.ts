/**
 * The Event Card Widget displays the following about an ongoing event:
 * - Queue stats
 * - Location
 * - How long the event is open until
 *
 * @author Sadie Amato, Madelyn Andrews, Bailey DeSouza, Meghan Sun
 * @copyright 2024
 * @license MIT
 */

import { Component, Input, OnInit } from '@angular/core';
import {
  OfficeHoursEvent,
  OfficeHoursEventType
} from '../../office-hours.models';
import { RosterRole } from 'src/app/academics/academics.models';
import { OfficeHoursService } from '../../office-hours.service';
import { DeleteEventDialog } from '../delete-event-dialog/delete-event-dialog.widget';
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'event-card-widget',
  templateUrl: './event-card-widget.html',
  styleUrls: ['./event-card-widget.css']
})
export class EventCard implements OnInit {
  /* Inputted  event to display and roster role to use */
  @Input() event!: OfficeHoursEvent;
  @Input() rosterRole!: RosterRole | null;
  /* Ticket queue stats */
  queued_tickets: number | null;
  called_tickets: number | null;

  constructor(
    private officeHoursService: OfficeHoursService,
    public dialog: MatDialog
  ) {
    this.queued_tickets = null;
    this.called_tickets = null;
  }

  ngOnInit(): void {
    this.getTicketStats();
    console.log(this.event);
  }

  /* Helper function that formats event type */
  formatEventType(typeNum: number) {
    if (typeNum === OfficeHoursEventType.OFFICE_HOURS) {
      return 'Office Hours';
    } else if (typeNum === OfficeHoursEventType.TUTORING) {
      return 'Tutoring';
    } else if (typeNum === OfficeHoursEventType.REVIEW_SESSION) {
      return 'Review Session';
    } else {
      return 'error';
    }
  }

  /* Gets current ticket queue information to display */
  getTicketStats() {
    this.officeHoursService
      .getQueuedAndCalledTicketCount(this.event.id)
      .subscribe((event_status) => {
        this.called_tickets = event_status.open_tickets_count;
        this.queued_tickets = event_status.queued_tickets_count;
      });
  }

  /* Opens dialog to confirm event deletion */
  openDeleteEventDialog() {
    const dialogRef = this.dialog.open(DeleteEventDialog, {
      height: 'auto',
      width: 'auto',
      data: { isCurrent: true, events: [this.event] }
    });

    dialogRef.afterClosed().subscribe((open) => {
      if (!open) {
        window.location.reload();
      }
    });
  }
}
