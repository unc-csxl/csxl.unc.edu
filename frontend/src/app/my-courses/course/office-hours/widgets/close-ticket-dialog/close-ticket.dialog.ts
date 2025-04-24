import { Component, Inject, signal, WritableSignal } from '@angular/core';
import { FormControl } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { WebSocketSubject } from 'rxjs/webSocket';
import {
  QueueWebSocketAction,
  QueueWebSocketData
} from 'src/app/my-courses/my-courses.model';
import { MyCoursesService } from 'src/app/my-courses/my-courses.service';

interface CloseTicketDialogData {
  ticketId: number;
  socketConnection: WebSocketSubject<any>;
}

@Component({
  selector: 'dialog-close-ticket',
  templateUrl: './close-ticket.dialog.html',
  styleUrl: './close-ticket.dialog.css'
})
export class CloseTicketDialog {
  hasConcerns = new FormControl(false);
  notes = new FormControl('');

  constructor(
    protected dialogRef: MatDialogRef<CloseTicketDialog>,
    @Inject(MAT_DIALOG_DATA) public data: CloseTicketDialogData,
    protected myCoursesService: MyCoursesService,
    private router: Router,
    private snackBar: MatSnackBar
  ) {}

  /**
   * Submits the form and closes a ticket.
   */
  submit(): void {
    const action: QueueWebSocketData = {
      action: QueueWebSocketAction.CLOSE,
      close_payload: {
        has_concerns: this.hasConcerns.value ?? false,
        caller_notes: this.notes.value ?? ''
      },
      id: this.data.ticketId
    };
    this.data.socketConnection.next(action);
    this.close();
  }

  /** Closes the dialog */
  close(): void {
    this.dialogRef.close();
  }
}
