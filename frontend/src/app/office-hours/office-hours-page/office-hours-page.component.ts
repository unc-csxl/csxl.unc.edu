/**
 * The Office Hours Page Component serves as the home page for the Office Hours feature.
 * The Office Hours Page is a hub for students to join Office Hours Sections, and for instructors to
 * create new Office Hours Sections
 *
 * @author Madelyn Andrews, Bailey DeSouza, Meghan Sun, Sadie Amato
 * @copyright 2024
 * @license MIT
 */

import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { SectionCreationDialog } from '../widgets/section-creation-dialog/section-creation-dialog.widget';
import { JoinSectionDialog } from '../widgets/join-section-dialog/join-section-dialog.widget';
import { OfficeHoursService } from '../office-hours.service';
import { OfficeHoursSectionDetails } from '../office-hours.models';
import { AcademicsService } from 'src/app/academics/academics.service';
import { SectionMember } from 'src/app/academics/academics.models';

@Component({
  selector: 'app-office-hours-page',
  templateUrl: './office-hours-page.component.html',
  styleUrls: ['./office-hours-page.component.css']
})
export class OfficeHoursPageComponent implements OnInit {
  public static Route = {
    path: '',
    title: 'Office Hours',
    component: OfficeHoursPageComponent,
    canActivate: []
  };

  protected userSections: OfficeHoursSectionDetails[] = [];
  // List of all instances where the user is an instructor of a course
  protected instructorCourses: SectionMember[] = [];

  constructor(
    public dialog: MatDialog,
    private officeHoursService: OfficeHoursService,
    private academicsService: AcademicsService
  ) {}

  openSectionCreationFormDialog() {
    const dialogRef = this.dialog.open(SectionCreationDialog, {
      height: 'auto',
      width: 'auto'
    });
  }

  openJoinSectionDialog() {
    const dialogRef = this.dialog.open(JoinSectionDialog, {
      height: 'auto',
      width: 'auto'
    });

    dialogRef.afterClosed().subscribe((open) => {
      if (!open) {
        window.location.reload();
      }
    });
  }

  //TODO: Un-hardcode 'F23'
  ngOnInit(): void {
    this.getUserSectionsByTerm('F23');
    this.checkInstructorship();
  }

  getUserSectionsByTerm(term_id: string) {
    this.officeHoursService
      .getUserSectionsByTerm(term_id)
      .subscribe((sections) => {
        (this.userSections = sections), console.log(sections);
      });
  }

  checkInstructorship() {
    this.academicsService.checkInstructorship().subscribe((section_members) => {
      this.instructorCourses = section_members;
    });
  }
}
