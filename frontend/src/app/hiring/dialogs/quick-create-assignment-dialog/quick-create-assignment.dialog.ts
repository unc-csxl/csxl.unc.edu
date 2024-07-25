/**
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { HiringService } from '../../hiring.service';
import { PublicProfile } from 'src/app/profile/profile.service';
import {
  HiringAssignmentDraft,
  HiringAssignmentStatus,
  HiringCourseSiteOverview,
  HiringLevel
} from '../../hiring.models';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';

export interface QuickCreateAssignmentDialogData {
  user: PublicProfile;
  termId: string;
  courseSite: HiringCourseSiteOverview;
}

@Component({
  selector: 'app-quick-create-assignment-dialog',
  templateUrl: './quick-create-assignment.dialog.html',
  styleUrl: './quick-create-assignment.dialog.css'
})
export class QuickCreateAssignmentDialog {
  hiringAssignmentStatus = HiringAssignmentStatus;

  /** Assignment form */
  user: PublicProfile;

  public createAssignmentForm = this.formBuilder.group({
    level: new FormControl<HiringLevel | null>(null, [Validators.required]),
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
    protected dialogRef: MatDialogRef<QuickCreateAssignmentDialog>,
    protected formBuilder: FormBuilder,
    private snackBar: MatSnackBar,
    @Inject(MAT_DIALOG_DATA) public data: QuickCreateAssignmentDialogData
  ) {
    this.user = data.user;
  }

  /** Determines if the form is valid and can be submitted. */
  formIsValid(): boolean {
    return this.createAssignmentForm.valid;
  }

  /**
   * Submits the form and creates a new course site.
   */
  submit(): void {
    if (this.formIsValid()) {
      // Create the new draft
      let assignmentDraft: HiringAssignmentDraft = {
        id: null,
        user_id: this.user.id,
        term_id: this.data.termId,
        course_site_id: this.data.courseSite.course_site_id,
        level: this.createAssignmentForm.get('level')!.value!,
        status: this.createAssignmentForm.get('status')!.value!,
        position_number:
          this.createAssignmentForm.get('position_number')!.value ?? '',
        epar: this.createAssignmentForm.get('epar')!.value ?? '',
        i9: this.createAssignmentForm.get('i9')!.value ?? false,
        notes: this.createAssignmentForm.get('notes')!.value ?? '',
        created: new Date(),
        modified: new Date()
      };
      // Attempt to create the assignment
      this.hiringService.createHiringAssignment(assignmentDraft).subscribe({
        next: (assignment) => {
          this.dialogRef.close(assignment);
          this.snackBar.open('Created a new assignment.', '', {
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
}
