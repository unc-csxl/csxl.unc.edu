/**
 * The Ticket Feedback Form Component allows TAs to express concerns for a student
 *
 * Note: In the future this form could also be used on the student side for students to leave
 * ratings + reviews on TAs.
 *
 * @author Sadie Amato, Madelyn Andrews, Bailey DeSouza, Meghan Sun
 * @copyright 2024
 * @license MIT
 */

import { Component, Input } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { TicketDetails } from '../office-hours.models';
import { OfficeHoursService } from '../office-hours.service';
import { MatDialogRef } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { map, mergeMap, switchMap } from 'rxjs';

@Component({
  selector: 'ticket-feedback-form',
  templateUrl: './ticket-feedback-form.component.html',
  styleUrls: ['./ticket-feedback-form.component.css']
})
export class TicketFeedbackFormComponent {
  @Input() ticket!: TicketDetails;
  constructor(
    protected formBuilder: FormBuilder,
    private officeHoursService: OfficeHoursService,
    public dialogRef: MatDialogRef<TicketFeedbackFormComponent>,
    protected snackBar: MatSnackBar
  ) {}

  /* Form Group for ticket feedback fields */
  public ticketFeedbackForm = this.formBuilder.group({
    have_concerns: '',
    notes: ''
  });

  onSubmit() {
    // If TicketFeedbackForm is valid, add feedback to ticket's data
    if (this.ticketFeedbackForm.valid) {
      if (this.ticketFeedbackForm.value.have_concerns === 'Yes') {
        console.log('concerns');
        this.ticket.have_concerns = true;
      }
      if (
        this.ticketFeedbackForm.value.notes &&
        this.ticketFeedbackForm.value.notes !== ''
      ) {
        this.ticket.caller_notes = this.ticketFeedbackForm.value.notes;
      }
      console.log(this.ticket);
      this.officeHoursService.closeTicket(this.ticket).subscribe(() =>
        this.officeHoursService.addFeedback(this.ticket).subscribe((ticket) => {
          this.ticketFeedbackForm.reset();
          this.dialogRef.close();
        })
      );
    }
  }
}
