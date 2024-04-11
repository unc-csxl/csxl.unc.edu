/**
 * The Upcoming Hours Dialog
 *
 * @author Sadie Amato, Madelyn Andrews, Bailey DeSouza, Meghan Sun
 * @copyright 2024
 * @license MIT
 */

import { Component, Inject, Input, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { OfficeHoursService } from '../../office-hours.service';
import { OfficeHoursEvent } from '../../office-hours.models';
import { OfficeHoursEventType } from '../../office-hours.models';

@Component({
  selector: 'upcoming-hours-dialog',
  templateUrl: './upcoming-hours-dialog.widget.html',
  styleUrls: ['./upcoming-hours-dialog.widget.css']
})
export class UpcomingHoursDialog implements OnInit {
  @Input() sectionId!: number;
  upcomingHours: OfficeHoursEvent[] = [];
  constructor(
    @Inject(MAT_DIALOG_DATA)
    public data: { sectionId: number },
    public dialogRef: MatDialogRef<UpcomingHoursDialog>,
    private officeHoursService: OfficeHoursService
  ) {
    this.sectionId = data.sectionId;
  }

  onNoClick(): void {
    this.dialogRef.close();
  }

  ngOnInit(): void {
    this.getUpcomingHours();
  }

  getUpcomingHours() {
    this.officeHoursService
      .getUpcomingEventsBySection(this.sectionId)
      .subscribe((hours) => {
        this.upcomingHours = hours;
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
}
