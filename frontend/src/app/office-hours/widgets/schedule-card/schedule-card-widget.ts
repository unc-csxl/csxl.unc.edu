/**
 * The Schedule Card abstracts the implementation of getting
 * upcoming events away from other components
 *
 * @author Sadie Amato, Madelyn Andrews, Bailey DeSouza, Meghan Sun
 * @copyright 2024
 * @license MIT
 */

import { Component, Input, OnInit } from '@angular/core';
import { OfficeHoursService } from '../../office-hours.service';
import {
  OfficeHoursEvent,
  OfficeHoursEventType
} from '../../office-hours.models';
import { RosterRole } from 'src/app/academics/academics.models';
import { DeleteEventDialog } from '../delete-event-dialog/delete-event-dialog.widget';
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'schedule-card-widget',
  templateUrl: './schedule-card-widget.html',
  styleUrls: ['./schedule-card-widget.css']
})
export class ScheduleCard implements OnInit {
  @Input() sectionId!: number;
  @Input() rosterRole!: RosterRole | null;
  upcomingHours: OfficeHoursEvent[] = [];

  constructor(
    private officeHoursService: OfficeHoursService,
    public dialog: MatDialog
  ) {}

  ngOnInit(): void {
    this.getUpcomingHours();
  }

  getUpcomingHours() {
    this.officeHoursService
      .getUpcomingEventsBySection(this.sectionId)
      .subscribe((hours) => {
        this.upcomingHours = hours.sort(
          (a, b) =>
            new Date(a.start_time).getTime() - new Date(b.start_time).getTime()
        );
      });
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

  openDeleteEventDialog() {
    const dialogRef = this.dialog.open(DeleteEventDialog, {
      height: 'auto',
      width: 'auto',
      data: { isCurrent: false, events: this.upcomingHours }
    });

    dialogRef.afterClosed().subscribe((open) => {
      if (!open) {
        window.location.reload();
      }
    });
  }
}
