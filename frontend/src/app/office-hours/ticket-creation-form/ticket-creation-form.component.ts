import { Component } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { OfficeHoursService } from '../office-hours.service';
import { TicketDraft, TicketType } from '../office-hours.models';

@Component({
  selector: 'ticket-creation-form',
  templateUrl: './ticket-creation-form.component.html',
  styleUrls: ['./ticket-creation-form.component.css']
})
export class TicketCreationFormComponent {
  public static Route = {
    // placeholder route
    path: 'spring-2024/comp110/create-new-ticket',
    title: 'COMP 110: Intro to Programming',
    component: TicketCreationFormComponent,
    canActivate: []
  };
  assignmentType: String = '';

  constructor(
    public officeHoursService: OfficeHoursService,
    protected formBuilder: FormBuilder
  ) {}

  public ticketForm = this.formBuilder.group({
    assignment_type: '',
    assignmentQ1: '',
    assignmentQ2: '',
    assignmentQ3: '',
    assignmentQ4: '',
    conceptualQ1: ''
  });

  onSubmit() {
    let form_description: string = '';
    let form_type: TicketType;
    if (this.assignmentType === 'conceptual_help') {
      form_description = this.ticketForm.value.conceptualQ1 ?? '';
      form_type = TicketType.CONCEPTUAL_HELP;
    } else {
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

    let ticket_draft: TicketDraft = {
      oh_event: {
        id: 1,
        oh_section: null,
        room: null,
        description: null,
        location_description: null,
        type: null,
        event_date: null,
        start_time: null,
        end_time: null
      },
      description: form_description,
      type: form_type,
      creators: [{ id: 3 }]
    };
    this.officeHoursService.createTicket(ticket_draft).subscribe({
      next: (ticket) => console.log(ticket)
    });
  }
}
