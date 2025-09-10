import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { MyCoursesService } from '../../my-courses.service';
import { OfficeHourTicketOverview } from '../../my-courses.model';

@Component({
    selector: 'dialog-ticket-details',
    templateUrl: './ticket-details.dialog.html',
    styleUrl: './ticket-details.dialog.css',
    standalone: false
})
export class TicketDetailsDialog {
  studentWaitTime = 0;
  ticketDuration = 0;

  constructor(
    protected dialogRef: MatDialogRef<TicketDetailsDialog>,
    @Inject(MAT_DIALOG_DATA)
    public data: { ticket: OfficeHourTicketOverview },
    protected myCoursesService: MyCoursesService
  ) {
    let createdAt = new Date(data.ticket.created_at);
    let calledAt = new Date(data.ticket.called_at!);
    let closedAt = new Date(data.ticket.closed_at!);
    this.studentWaitTime =
      (calledAt.getTime() - createdAt.getTime()) / 1000 / 60;

    this.ticketDuration = (closedAt.getTime() - calledAt.getTime()) / 1000 / 60;
  }

  close(): void {
    this.dialogRef.close();
  }
}
