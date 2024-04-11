/**
 * The Join Section Dialog allows a user to join an office hours section
 *
 * @author Sadie Amato, Madelyn Andrews, Bailey DeSouza, Meghan Sun
 * @copyright 2024
 * @license MIT
 */

import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { AcademicsService } from 'src/app/academics/academics.service';
import { OfficeHoursService } from '../../office-hours.service';
import {
  OfficeHoursSection,
  OfficeHoursSectionDetails,
  OfficeHoursSectionPartial
} from '../../office-hours.models';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Section, SectionMember } from 'src/app/academics/academics.models';

@Component({
  selector: 'join-section-dialog',
  templateUrl: './join-section-dialog.widget.html',
  styleUrls: ['./join-section-dialog.widget.css']
})
export class JoinSectionDialog implements OnInit {
  protected officeHoursSections: OfficeHoursSection[] = [];

  constructor(
    public dialogRef: MatDialogRef<JoinSectionDialog>,
    protected formBuilder: FormBuilder,
    private academicsService: AcademicsService,
    private officeHoursService: OfficeHoursService,
    protected snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.getOfficeHoursSection();
  }

  public joinSectionForm = this.formBuilder.group({
    oh_section: []
  });

  onNoClick(): void {
    this.dialogRef.close();
  }

  getOfficeHoursSection() {
    // TODO: change 'F23' to the current term using the academics service (this has a method to get current term)
    this.officeHoursService
      .getSectionsByTerm('F23')
      .subscribe((oh_sections) => {
        this.officeHoursSections = oh_sections;
      });
  }

  onSubmit() {
    console.log(this.joinSectionForm.value.oh_section);
    if (this.joinSectionForm.valid) {
      let oh_sections: OfficeHoursSectionDetails[] =
        this.joinSectionForm.value.oh_section ?? [];
      console.log(oh_sections);
      console.log(oh_sections[0]);
      this.officeHoursService.joinSection(oh_sections).subscribe({
        next: () => this.onSuccess(),
        error: (err) => this.onError(err)
      });
    }
  }

  private onError(err: any): void {
    this.snackBar.open('Error: Unable to join Office Hours Section', '', {
      duration: 2000
    });
  }

  private onSuccess(): void {
    this.snackBar.open('You have joined an office hours section!', '', {
      duration: 3000
    });
    this.joinSectionForm.reset();
  }
}
