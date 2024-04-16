/**
 * The Delete Ticket Dialog allows a user to delete a queued ticket
 *
 * @author Sadie Amato, Madelyn Andrews, Bailey DeSouza, Meghan Sun
 * @copyright 2024
 * @license MIT
 */

import { Component, Inject } from '@angular/core';
import { OfficeHoursService } from '../../office-hours.service';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';

@Component({
  selector: 'delete-ticket-dialog',
  templateUrl: './delete-ticket-dialog.widget.html',
  styleUrls: ['./delete-ticket-dialog.widget.css']
})
export class DeleteTicketDialog {
  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private officeHoursService: OfficeHoursService,
    private snackBar: MatSnackBar,
    private router: Router
  ) {}

  cancelTicket() {
    this.officeHoursService.cancelTicket(this.data.ticket).subscribe({
      next: () => this.onSuccess(),
      error: (err) => this.onError(err)
    });
  }

  private onSuccess() {
    this.snackBar.open('Your ticket has been canceled.', '', {
      duration: 2000
    });
    this.router.navigate([
      'office-hours/spring-2024/',
      this.data.event.oh_section.id
    ]);
  }

  private onError(err: any) {
    this.snackBar.open('Unable to cancel ticket', '', { duration: 4000 });
  }
}
