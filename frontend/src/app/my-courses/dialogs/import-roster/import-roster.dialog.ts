import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import {
  CourseSiteOverview,
  SectionOverview,
  TermOverview
} from '../../my-courses.model';
import { MyCoursesService } from '../../my-courses.service';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { FormControl } from '@angular/forms';

@Component({
  selector: 'dialog-import-roster',
  templateUrl: './import-roster.dialog.html',
  styleUrl: './import-roster.dialog.css'
})
export class ImportRosterDialog {
  file: File | null = null;
  selectedSection: FormControl<SectionOverview | null>;

  constructor(
    protected dialogRef: MatDialogRef<ImportRosterDialog>,
    @Inject(MAT_DIALOG_DATA) public data: CourseSiteOverview,
    protected myCoursesService: MyCoursesService,
    private router: Router,
    private snackBar: MatSnackBar
  ) {
    this.selectedSection = new FormControl(data.sections[0]);
  }

  /** Handles the uploading of the file. */
  uploadFile(event: any) {
    let uploadedFile: File = event.target.files[0];
    if (uploadedFile) {
      this.file = uploadedFile;
    }
  }

  /** Removes the currently selected file. */
  clearFile() {
    this.file = null;
  }

  /** Closes the dialog */
  close(): void {
    this.dialogRef.close();
  }

  /**
   * Submits the form and creates a new course site.
   */
  submit(): void {
    if (this.file && this.selectedSection) {
      // Read the file
      var reader = new FileReader();
      reader.readAsText(this.file, 'UTF-8');
      reader.onload = (event) => {
        let csvData = (event.target?.result as string) ?? '';

        // Attempt to create the roster
        this.myCoursesService
          .importRosterFromCanvasCSV(this.selectedSection.value!.id, csvData)
          .subscribe({
            next: (count) => {
              this.snackBar.open(`Imported ${count.uploaded} students.`, '', {
                duration: 5000
              });
              // Close the dialog
              this.close();
            },
            error: (err) => this.snackBar.open(err, '', { duration: 2000 })
          });
      };
      reader.onerror = (_) => {
        this.snackBar.open('Error reading the CSV file.', '', {
          duration: 2000
        });
      };
    }
  }
}
