/**
 * The Course Card Widget abstracts the implementation of the detail course
 * card away from the Office Hours Home Page
 *
 * @author Sadie Amato, Madelyn Andrews, Bailey DeSouza, Meghan Sun
 * @copyright 2024
 * @license MIT
 */

import { Component, Input, OnInit } from '@angular/core';
import {
  OfficeHoursEvent,
  OfficeHoursSectionDetails
} from '../../office-hours.models';
import { MatDialog } from '@angular/material/dialog';
import { UpcomingHoursDialog } from '../upcoming-hours-dialog/upcoming-hours-dialog.widget';
import { OfficeHoursService } from '../../office-hours.service';
import { Router } from '@angular/router';
import { AcademicsService } from 'src/app/academics/academics.service';
import { RosterRole } from 'src/app/academics/academics.models';

@Component({
  selector: 'course-card-widget',
  templateUrl: './course-card-widget.html',
  styleUrls: ['./course-card-widget.css']
})
export class CourseCard implements OnInit {
  /** The course to show */
  @Input() section!: OfficeHoursSectionDetails;
  currentEvents: OfficeHoursEvent[] = [];
  /* Roster role in the course */
  rosterRole: RosterRole | null;

  constructor(
    public dialog: MatDialog,
    private officeHoursService: OfficeHoursService,
    private academicsService: AcademicsService,
    private router: Router
  ) {
    this.rosterRole = null;
  }

  ngOnInit() {
    this.getCurrentEvents();
    this.checkRosterRole();
  }

  /* Opens upcoming hours dialog to display schedule */
  openDialog() {
    const dialogRef = this.dialog.open(UpcomingHoursDialog, {
      height: 'auto',
      width: 'auto',
      data: { sectionId: this.section.id }
    });
  }

  /* Navigates to section page based on roster role */
  navToOfficeHours() {
    // TODO: replace this route later
    if (this.rosterRole === RosterRole.STUDENT) {
      this.router.navigate(['/office-hours/spring-2024/', this.section.id]);
    } else if (this.rosterRole === RosterRole.UTA) {
      this.router.navigate(['/office-hours/ta/spring-2024/', this.section.id]);
    } else {
      // RosterRole is GTA or Instructor
      this.router.navigate([
        '/office-hours/instructor/spring-2024/',
        this.section.id
      ]);
    }
  }

  /* Gets ongoing events for the section being displayed */
  getCurrentEvents() {
    this.officeHoursService
      .getCurrentEventsBySection(this.section.id)
      .subscribe((events) => {
        this.currentEvents = events;
      });
  }

  /* Returns roster role of user accessing the page */
  checkRosterRole() {
    this.academicsService
      .getMembershipBySection(this.section.id)
      .subscribe((section_member) => {
        this.rosterRole = section_member.member_role;
        return section_member;
      });
  }
}
