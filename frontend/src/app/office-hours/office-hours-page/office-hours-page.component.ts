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
import { OfficeHoursSectionDetails } from '../office-hours.models';
import { AcademicsService } from 'src/app/academics/academics.service';
import { SectionMember, Term } from 'src/app/academics/academics.models';
import { ActivatedRoute } from '@angular/router';
import {
  currentTermResolver,
  termsResolver
} from 'src/app/academics/academics.resolver';
import { FormControl } from '@angular/forms';
import { OfficeHoursService } from '../office-hours.service';

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
    canActivate: [],
    resolve: {
      currentTerm: currentTermResolver,
      terms: termsResolver
    }
  };

  /* List of all sections where user has membership */
  protected userSections: OfficeHoursSectionDetails[] = [];

  /* List of all instances where the user is an instructor of a course */
  protected instructorCourses: SectionMember[] = [];
  protected currentTerm: Term;
  protected terms: Term[];

  /** Store the currently selected term from the form */
  public displayTerm: FormControl<Term> = new FormControl();

  constructor(
    public dialog: MatDialog,
    private officeHoursService: OfficeHoursService,
    private academicsService: AcademicsService,
    private route: ActivatedRoute
  ) {
    /** Initialize data from resolvers. */
    const data = this.route.snapshot.data as {
      currentTerm: Term;
      terms: Term[];
    };
    this.currentTerm = data.currentTerm;
    this.displayTerm.setValue(data.currentTerm);
    this.terms = data.terms;
    this.getSectionsByTerm(this.currentTerm.id);
  }

  /* Opens dialog panel that contains form to create new OH sections */
  openSectionCreationFormDialog() {
    const dialogRef = this.dialog.open(SectionCreationDialog, {
      height: 'auto',
      width: 'auto'
    });

    dialogRef.afterClosed().subscribe((open) => {
      if (!open) {
        window.location.reload();
      }
    });
  }

  /* Opens dialog panel that contains form to join OH sections */
  openJoinSectionDialog() {
    const dialogRef = this.dialog.open(JoinSectionDialog, {
      height: 'auto',
      width: 'auto',
      data: { displayTerm: this.displayTerm.value }
    });

    dialogRef.afterClosed().subscribe((open) => {
      if (!open) {
        window.location.reload();
      }
    });
  }

  ngOnInit(): void {
    this.checkInstructorship();
  }

  /* Checks instructorship by seeing if user has any Instructor Courses */
  checkInstructorship() {
    this.academicsService.checkInstructorship().subscribe((section_members) => {
      this.instructorCourses = section_members;
    });
  }

  getSectionsByTerm(term_id: string) {
    this.officeHoursService
      .getUserSectionsByTerm(term_id)
      .subscribe((sections) => {
        this.userSections = sections;
      });
  }

  onTermChange(value: Term) {
    this.officeHoursService
      .getUserSectionsByTerm(value.id)
      .subscribe((sections) => {
        this.userSections = sections;
      });
  }
}
