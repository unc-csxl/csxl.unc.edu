import { Component, Input, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { OfficeHoursService } from '../office-hours.service';
import {
  OfficeHoursEventDetails,
  TicketDraft,
  TicketType
} from '../office-hours.models';
import { ChangeDetectorRef } from '@angular/core';
import { Location } from '@angular/common';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'ticket-creation-form',
  templateUrl: './ticket-creation-form.component.html',
  styleUrls: ['./ticket-creation-form.component.css']
})
export class TicketCreationFormComponent implements OnInit {
  public static Route = {
    // TODO: un-hardcode this route
    path: 'spring-2024/:id/:event_id/create-new-ticket',
    title: 'COMP 110: Intro to Programming',
    component: TicketCreationFormComponent,
    canActivate: []
  };
  // Stores the AssignmentType chosen in the first part of stepper
  assignmentType: String = '';
  eventId: number;
  event: OfficeHoursEventDetails | undefined;

  constructor(
    public officeHoursService: OfficeHoursService,
    protected formBuilder: FormBuilder,
    protected cdr: ChangeDetectorRef,
    private location: Location,
    private route: ActivatedRoute
  ) {
    this.eventId = this.route.snapshot.params['event_id'];
  }

  ngOnInit(): void {
    this.getEvent();
  }

  getEvent() {
    this.officeHoursService.getEvent(this.eventId).subscribe((event) => {
      this.event = event;
    });
  }
  public ticketForm = this.formBuilder.group({
    assignment_type: '',
    assignmentQ1: '',
    assignmentQ2: '',
    assignmentQ3: '',
    assignmentQ4: '',
    conceptualQ1: ''
  });

  onAssignmentTypeChange(value: string) {
    /* checks for assignment type in the form (accounts for user 
      clicking back button and changing again) */
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
      form_description = this.ticketForm.value.conceptualQ1 ?? '';
      form_type = TicketType.CONCEPTUAL_HELP;
    } else {
      // Concatenates form description together and adds in new line characters
      form_description =
        (this.ticketForm.value.assignmentQ1 ?? '') +
        ' \n' +
        (this.ticketForm.value.assignmentQ2 ?? '') +
        ' \n' +
        (this.ticketForm.value.assignmentQ3 ?? '') +
        ' \n' +
        (this.ticketForm.value.assignmentQ4 ?? '');

      form_type = TicketType.ASSIGNMENT_HELP;
    }
    if (this.event) {
      let ticket_draft: TicketDraft = {
        // TODO: un-hardcode event information
        oh_event: this.event,
        description: form_description,
        type: form_type,
        // TODO: un-hardcode creators
        creators: [{ id: 3 }]
      };
      this.officeHoursService.createTicket(ticket_draft).subscribe({
        next: (ticket) => console.log(ticket) //remove console.log later -> for demo purposes
      });
      this.ticketForm.reset();
      // brings user to previous page (the course Office Hours home page)
      this.location.back();
    }
  }
}
