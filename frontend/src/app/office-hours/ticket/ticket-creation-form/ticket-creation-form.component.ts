/**
 * The Ticket Creation Form allows students to create a new ticket and join the current queue
 *
 * @author Sadie Amato, Madelyn Andrews, Bailey DeSouza, Meghan Sun
 * @copyright 2024
 * @license MIT
 */

import { Component, Input, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { OfficeHoursService } from '../../office-hours.service';
import {
  OfficeHoursEventDetails,
  TicketDraft,
  TicketType
} from '../../office-hours.models';
import { ChangeDetectorRef } from '@angular/core';
import { Location } from '@angular/common';
import {
  ActivatedRoute,
  ActivatedRouteSnapshot,
  ResolveFn,
  Router
} from '@angular/router';
import { HttpErrorResponse } from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ohSectionResolver } from '../../office-hours.resolver';

let titleResolver: ResolveFn<string> = (route: ActivatedRouteSnapshot) => {
  return route.parent!.data['section']?.title ?? 'Section Not Found';
};

@Component({
  selector: 'ticket-creation-form',
  templateUrl: './ticket-creation-form.component.html',
  styleUrls: ['./ticket-creation-form.component.css']
})
export class TicketCreationFormComponent implements OnInit {
  public static Route = {
    path: ':id/:event_id/create-new-ticket',
    component: TicketCreationFormComponent,
    canActivate: [],
    resolve: { section: ohSectionResolver },
    children: [
      {
        path: '',
        title: titleResolver,
        component: TicketCreationFormComponent
      }
    ]
  };
  /* Stores the AssignmentType chosen in the first part of stepper */
  assignmentType: String = '';

  /* Stores event that ticket is being created under */
  eventId: number;
  event: OfficeHoursEventDetails | undefined;

  /* Section ID for Office Hours Section ticket is associated with */
  sectionId: number;

  constructor(
    public officeHoursService: OfficeHoursService,
    protected formBuilder: FormBuilder,
    protected cdr: ChangeDetectorRef,
    private router: Router,
    private route: ActivatedRoute,
    protected snackBar: MatSnackBar
  ) {
    /* Gets section and event IDs from route parameters */
    this.sectionId = this.route.snapshot.params['id'];
    this.eventId = this.route.snapshot.params['event_id'];
  }

  ngOnInit(): void {
    this.getEvent();
  }

  /* Gets OH Event from ID */
  getEvent() {
    this.officeHoursService.getEvent(this.eventId).subscribe((event) => {
      this.event = event;
    });
  }
  /* TicketForm stores student's answers to ticket questionaire */
  public ticketForm = this.formBuilder.group({
    assignment_type: '',
    assignmentQ1: '',
    assignmentQ2: '',
    assignmentQ3: '',
    assignmentQ4: '',
    assignmentQ5: '',
    conceptualQ1: '',
    conceptualQ2: ''
  });

  /** Checks for assignment type in the form (accounts for user clicking back button and changing again)
   * @param value - newly selected assignment type selected */
  onAssignmentTypeChange(value: string) {
    this.assignmentType = value;
    this.cdr.detectChanges();
  }

  onSubmit() {
    let form_description: string = '';
    let form_type: TicketType;
    /* Below is logic for checking form values and assigning the correct
      TicketType and ticket description accordingly
    */
    if (this.assignmentType === 'conceptual_help') {
      form_description =
        'Conceptual: ' + (this.ticketForm.value.conceptualQ1 ?? '');
      if (this.event?.mode === 1) {
        form_description =
          form_description +
          ' \nLink: ' +
          (this.ticketForm.value.conceptualQ2 ?? '');
      }
      form_type = TicketType.CONCEPTUAL_HELP;
    } else {
      // Concatenates form description together and adds in new line characters
      form_description =
        'Assignment Part: ' +
        (this.ticketForm.value.assignmentQ1 ?? '') +
        ' \nGoal: ' +
        (this.ticketForm.value.assignmentQ2 ?? '') +
        ' \nConcepts: ' +
        (this.ticketForm.value.assignmentQ3 ?? '') +
        ' \nTried: ' +
        (this.ticketForm.value.assignmentQ4 ?? '');

      if (this.event?.mode === 1) {
        form_description =
          form_description +
          ' \nLink: ' +
          (this.ticketForm.value.assignmentQ5 ?? '');
      }

      form_type = TicketType.ASSIGNMENT_HELP;
    }
    if (this.event) {
      // Create ticket draft from inputted ticket information
      let ticket_draft: TicketDraft = {
        oh_event: this.event,
        description: form_description,
        type: form_type,
        // TODO: if adding multiple creators (group tickets), would add users here
        creators: []
      };
      this.officeHoursService.createTicket(ticket_draft).subscribe(
        (ticket) => {
          this.router.navigate([
            'office-hours/',
            this.sectionId,
            this.eventId,
            'ticket',
            ticket.id
          ]);
        },
        (err) => this.onError(err)
      );
    }
  }

  private onError(err: HttpErrorResponse): void {
    this.snackBar.open(err.error.detail, '', {
      duration: 5000
    });
  }

  formatEventModeType(typeNum: number) {
    return this.officeHoursService.formatEventModeType(typeNum);
  }
}
