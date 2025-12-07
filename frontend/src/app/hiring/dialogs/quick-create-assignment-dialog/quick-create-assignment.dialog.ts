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
  ConflictCheck,
  HiringAdminCourseOverview,
  HiringAssignmentDraft,
  HiringAssignmentStatus,
  HiringCourseSiteOverview,
  HiringLevel
} from '../../hiring.models';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ApplicationDialog } from '../application-dialog/application-dialog.dialog';
import { filter, map } from 'rxjs';

export interface QuickCreateAssignmentDialogData {
  user: PublicProfile;
  termId: string;
  courseSite: HiringCourseSiteOverview;
  courseAdmin: HiringAdminCourseOverview;
}

@Component({
    selector: 'app-quick-create-assignment-dialog',
    templateUrl: './quick-create-assignment.dialog.html',
    styleUrl: './quick-create-assignment.dialog.css',
    standalone: false
})
export class QuickCreateAssignmentDialog {
  hiringAssignmentStatus = HiringAssignmentStatus;
  public conflictCheck: ConflictCheck = {
    application_id: 0,
    assignments: [],
    priorities: []
  };

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
    protected dialog: MatDialog,
    @Inject(MAT_DIALOG_DATA) public data: QuickCreateAssignmentDialogData
  ) {
    this.user = data.user;

    // Simple hack to automatically populate the level...
    let review = data.courseAdmin.reviews.find(
      (r) => r.applicant_id == data.user.id
    )!;
    
    let level: HiringLevel | undefined;
    
    // Try to use the instructor's preferred level
    if (review.level?.id) {
      level = this.hiringService.getHiringLevel(review.level.id);
    }
    
    // Fall back to title-based search if no preferred level is set or found
    if (!level) {
      let program = review.application.program_pursued!;
      let defaultLevelSearch: string | null;
      switch (program) {
        case 'PhD':
          defaultLevelSearch = '1.0 PhD TA';
          break;
        case 'PhD (ABD)':
          defaultLevelSearch = '1.0 PhD (ABD) TA';
          break;
        case 'BS/MS':
        case 'MS':
          defaultLevelSearch = '1.0 MS TA';
          break;
        default:
          defaultLevelSearch = '10h UTA';
          break;
      }

      level = this.hiringService
        .hiringLevels()
        .find((level) => level.title == defaultLevelSearch);
    }
    
    if (level) {
      this.createAssignmentForm.get('level')?.setValue(level);
    }

    this.hiringService
      .conflictCheck(review.application_id)
      // .pipe(
      //   map((conflictCheck) => {
      //     let thisPriority = conflictCheck.priorities.find(
      //       (priority) =>
      //         priority.course_site_id == data.courseSite.course_site_id
      //     );
      //     if (thisPriority) {
      //       let minStudentPriority
      //     }
      //     return conflictCheck;
      //   })
      // )
      .subscribe((result) => (this.conflictCheck = result));
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
        application_review_id: this.getApplication()?.id ?? null,
        level: this.createAssignmentForm.get('level')!.value!,
        status: this.createAssignmentForm.get('status')!.value!,
        position_number:
          this.createAssignmentForm.get('position_number')!.value ?? '',
        epar: this.createAssignmentForm.get('epar')!.value ?? '',
        i9: this.createAssignmentForm.get('i9')!.value ?? false,
        notes: this.createAssignmentForm.get('notes')!.value ?? '',
        flagged: false,
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

  getApplication(): ApplicationReviewOverview | undefined {
    return this.data.courseAdmin.reviews.find(
      (a) => a.applicant_id === this.data.user.id
    );
  }

  /** Returns true if the given level matches the instructor's preferred level for this applicant. */
  isInstructorPreferred(level: HiringLevel): boolean {
    const app = this.getApplication();
    const preferredId = app?.level?.id ?? null;
    return preferredId != null && level.id === preferredId;
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
