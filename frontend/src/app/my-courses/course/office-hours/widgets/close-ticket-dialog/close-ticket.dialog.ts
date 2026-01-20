import { Component, Inject, signal, WritableSignal } from '@angular/core';
import { FormControl } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { MyCoursesService } from 'src/app/my-courses/my-courses.service';

@Component({
  selector: 'dialog-close-ticket',
  templateUrl: './close-ticket.dialog.html',
  standalone: false
})
export class CloseTicketDialog {
  hasConcerns = new FormControl(false);
  notes = new FormControl('');

  constructor(
    protected dialogRef: MatDialogRef<CloseTicketDialog>,
    @Inject(MAT_DIALOG_DATA) public ticketId: number,
    protected myCoursesService: MyCoursesService,
    private router: Router,
    private snackBar: MatSnackBar
  ) {}

  /**
   * Submits the form and closes a ticket.
   */
  submit(): void {
    this.myCoursesService
      .closeTicket(
        this.ticketId,
        this.hasConcerns.value ?? false,
        this.notes.value ?? ''
      )
      .subscribe({
        next: () => {
          this.close();
        },
        error: (err) => this.snackBar.open(err, '', { duration: 2000 })
      });
  }

  /** Closes the dialog */
  close(): void {
    this.dialogRef.close();
  }
}
