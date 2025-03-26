import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { MyCoursesService } from '../../my-courses.service';
import { CourseMemberOverview } from '../../my-courses.model';

@Component({
  selector: 'dialog-student-summary',
  templateUrl: './student-summary.dialog.html',
  styleUrl: './student-summary.dialog.css'
})
export class StudentSummaryDialog {
  pid = 0;
  first_name = '';
  last_name = '';
  email = '';
  pronouns = '';
  section_number = '';
  github_avatar = '';

  constructor(
    protected dialogRef: MatDialogRef<StudentSummaryDialog>,
    @Inject(MAT_DIALOG_DATA)
    public data: { student: CourseMemberOverview },
    protected myCoursesService: MyCoursesService
  ) {}

  close(): void {
    this.dialogRef.close();
  }
}
