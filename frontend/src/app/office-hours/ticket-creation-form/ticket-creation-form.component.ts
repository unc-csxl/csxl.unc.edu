import { Component } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';

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

  constructor() {}
}
