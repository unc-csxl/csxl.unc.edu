import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { TermOverview } from '../../my-courses.model';
import { MyCoursesService } from '../../my-courses.service';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'dialog-import-roster',
  templateUrl: './import-roster.dialog.html',
  styleUrl: './import-roster.dialog.css'
})
export class ImportRosterDialog {
  file: File | null = null;
  constructor(
    protected dialogRef: MatDialogRef<ImportRosterDialog>,
    @Inject(MAT_DIALOG_DATA) public data: TermOverview[],
    protected myCoursesService: MyCoursesService,
    private router: Router,
    private snackBar: MatSnackBar
  ) {}

  /** Handles the uploading of the file. */
  uploadFile(event: any) {
    let uploadedFile: File = event.target.files[0];
    if (uploadedFile) {
      this.file = uploadedFile;
    }
  }

  /** Closes the dialog */
  close(): void {
    this.dialogRef.close();
  }
}
