import { Component, Input } from '@angular/core';
import { flushMicrotasks } from '@angular/core/testing';
import { OfficeHoursSectionDetails } from '../../office-hours.models';
import { MatDialog } from '@angular/material/dialog';
import { UpcomingHoursDialog } from '../upcoming-hours-dialog/upcoming-hours-dialog.widget';

@Component({
  selector: 'course-card-widget',
  templateUrl: './course-card-widget.html',
  styleUrls: ['./course-card-widget.css']
})
export class CourseCard {
  /** The course to show */
  @Input() section!: OfficeHoursSectionDetails;
  constructor(public dialog: MatDialog) {}

  openDialog() {
    const dialogRef = this.dialog.open(UpcomingHoursDialog, {
      height: 'auto',
      width: 'auto',
      data: { sectionId: this.section.id }
    });
  }

  navToOfficeHours() {
    console.log('test');
  }
}
