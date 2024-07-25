/**
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { Component, Inject } from '@angular/core';
import {
  MAT_DIALOG_DATA,
  MatDialog,
  MatDialogRef
} from '@angular/material/dialog';
import { HiringService } from '../../hiring.service';
import { PublicProfile } from 'src/app/profile/profile.service';
import {
  ApplicationReviewOverview,
  HiringAssignmentDraft,
  HiringAssignmentOverview,
  HiringAssignmentStatus,
  HiringCourseSiteOverview,
  HiringLevel
} from '../../hiring.models';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ApplicationDialog } from '../application-dialog/application-dialog.dialog';

export interface EditAssignmentDialogData {
  assignment: HiringAssignmentOverview;
  termId: string;
  courseSite: HiringCourseSiteOverview;
}

@Component({
  selector: 'app-edit-assignment-dialog',
  templateUrl: './edit-assignment.dialog.html',
  styleUrl: './edit-assignment.dialog.css'
})
export class EditAssignmentDialog {
  hiringAssignmentStatus = HiringAssignmentStatus;

  /** Assignment form */
  users: PublicProfile[] = [];

  public editAssignmentForm = this.formBuilder.group({
    level: new FormControl<HiringLevel | undefined>(undefined, [
      Validators.required
    ]),
    status: new FormControl(HiringAssignmentStatus.DRAFT, [
      Validators.required
    ]),
    position_number: new FormControl(''),
    epar: new FormControl(''),
    i9: new FormControl(false),
    notes: new FormControl('')
  });

  /** Constructor */
  constructor(
    protected hiringService: HiringService,
    protected dialogRef: MatDialogRef<EditAssignmentDialog>,
    protected formBuilder: FormBuilder,
    private snackBar: MatSnackBar,
    protected dialog: MatDialog,
    @Inject(MAT_DIALOG_DATA) public data: EditAssignmentDialogData
  ) {
    this.editAssignmentForm.patchValue(data.assignment);
    const level = this.hiringService
      .hiringLevels()
      .find((level) => level.id === data.assignment.level.id);
    this.editAssignmentForm.get('level')?.setValue(level);
  }

  /** Determines if the form is valid and can be submitted. */
  formIsValid(): boolean {
    return this.editAssignmentForm.valid;
  }

  /**
   * Submits the form and creates a new course site.
   */
  submit(): void {
    if (this.formIsValid()) {
      // Create the new draft
      let assignmentDraft: HiringAssignmentDraft = {
        id: this.data.assignment.id,
        user_id: this.data.assignment.user.id,
        term_id: this.data.termId,
        course_site_id: this.data.courseSite.course_site_id,
        level: this.editAssignmentForm.get('level')!.value!,
        status: this.editAssignmentForm.get('status')!.value!,
        position_number:
          this.editAssignmentForm.get('position_number')!.value ?? '',
        epar: this.editAssignmentForm.get('epar')!.value ?? '',
        i9: this.editAssignmentForm.get('i9')!.value ?? false,
        notes: this.editAssignmentForm.get('notes')!.value ?? '',
        created: new Date(), // Will be overwritten anyway
        modified: new Date()
      };
      // Attempt to create the assignment
      this.hiringService.updateHiringAssignment(assignmentDraft).subscribe({
        next: (assignment) => {
          this.dialogRef.close(assignment);
          this.snackBar.open('Updated assignment.', '', {
            duration: 2000
          });
        },
        error: (err) => this.snackBar.open(err, '', { duration: 2000 })
      });
    }
  }

  /** Closes the dialog */
  close(): void {
    this.dialogRef.close();
  }

  getApplication(): ApplicationReviewOverview | undefined {
    return this.data.courseSite.reviews.find(
      (a) => a.applicant_id === this.data.assignment.user.id
    );
  }

  openApplicationDialog(): void {
    this.dialog.open(ApplicationDialog, {
      height: '600px',
      width: '800px',
      data: {
        courseSiteId: this.data.courseSite.course_site_id,
        review: this.getApplication()!,
        viewOnly: true
      }
    });
  }
}
