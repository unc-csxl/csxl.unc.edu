import { Component, Input, OnInit } from '@angular/core';
import { flushMicrotasks } from '@angular/core/testing';
import {
  OfficeHoursEvent,
  OfficeHoursSectionDetails
} from '../../office-hours.models';
import { MatDialog } from '@angular/material/dialog';
import { UpcomingHoursDialog } from '../upcoming-hours-dialog/upcoming-hours-dialog.widget';
import { OfficeHoursService } from '../../office-hours.service';

@Component({
  selector: 'course-card-widget',
  templateUrl: './course-card-widget.html',
  styleUrls: ['./course-card-widget.css']
})
export class CourseCard implements OnInit {
  /** The course to show */
  @Input() section!: OfficeHoursSectionDetails;
  currentEvents: OfficeHoursEvent[] = [];

  constructor(
    public dialog: MatDialog,
    private officeHoursService: OfficeHoursService
  ) {}

  ngOnInit() {
    this.getCurrentEvents();
  }

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

  getCurrentEvents() {
    this.officeHoursService
      .getCurrentEventsBySection(this.section.id)
      .subscribe((events) => {
        this.currentEvents = events;
      });
  }
}
