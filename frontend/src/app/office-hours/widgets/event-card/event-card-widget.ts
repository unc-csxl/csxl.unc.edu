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
import { flushMicrotasks } from '@angular/core/testing';
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
  @Input() event!: OfficeHoursEvent;
  @Input() rosterRole!: RosterRole | null;
  queued_tickets: number | null;
  called_tickets: number | null;

  constructor(
    private officeHoursService: OfficeHoursService,
    public dialog: MatDialog
  ) {
    console.log('reached event card.');
    this.queued_tickets = null;
    this.called_tickets = null;
  }

  ngOnInit(): void {
    this.getTicketStats();
  }

  formatEventType(typeNum: number) {
    if (typeNum === OfficeHoursEventType.OFFICE_HOURS) {
      return 'Office Hours';
    } else if (typeNum === OfficeHoursEventType.TUTORING) {
      return 'Tutoring';
    } else if (typeNum === OfficeHoursEventType.REVIEW_SESSION) {
      return 'Review Session';
    } else if (typeNum === OfficeHoursEventType.VIRTUAL_OFFICE_HOURS) {
      return 'Virtual Office Hours';
    } else if (typeNum === OfficeHoursEventType.VIRTUAL_TUTORING) {
      return 'Virtual Tutoring';
    } else if (typeNum === OfficeHoursEventType.VIRTUAL_REVIEW_SESSION) {
      return 'Virtual Review Session';
    } else {
      return 'error';
    }
  }

  getTicketStats() {
    this.officeHoursService
      .getQueuedAndCalledTicketCount(this.event.id)
      .subscribe((event_status) => {
        this.called_tickets = event_status.open_tickets_count;
        this.queued_tickets = event_status.queued_tickets_count;
      });
  }

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
