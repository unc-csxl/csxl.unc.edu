/**
 * Ticket Feedback Dialog
 *
 * @author Sadie Amato, Madelyn Andrews, Bailey DeSouza, Meghan Sun
 * @copyright 2024
 * @license MIT
 */

import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'ticket-feedback-dialog',
  templateUrl: './ticket-feedback-dialog.widget.html',
  styleUrls: ['./ticket-feedback-dialog.widget.css']
})
export class TicketFeedbackDialog {
  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    public dialogRef: MatDialogRef<TicketFeedbackDialog>
  ) {}

  onNoClick(): void {
    this.dialogRef.close();
  }
}
