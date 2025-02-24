/**
 * Office hours page for students that enables them to create tickets and get help.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import {
  Component,
  OnDestroy,
  OnInit,
  WritableSignal,
  signal
} from '@angular/core';
import { officeHourPageGuard } from '../office-hours.guard';
import { ActivatedRoute } from '@angular/router';
import { MyCoursesService } from 'src/app/my-courses/my-courses.service';
import {
  GetHelpWebSocketAction,
  GetHelpWebSocketData,
  OfficeHourGetHelpOverview,
  OfficeHourGetHelpOverviewJson,
  OfficeHourTicketOverview,
  parseOfficeHourGetHelpOverviewJson,
  TicketDraft
} from 'src/app/my-courses/my-courses.model';
import { Subscription, timer } from 'rxjs';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { LocationStrategy } from '@angular/common';

@Component({
  selector: 'app-office-hours-get-help',
  templateUrl: './office-hours-get-help.component.html',
  styleUrl: './office-hours-get-help.component.css'
})
export class OfficeHoursGetHelpComponent implements OnInit, OnDestroy {
  /** Route information to be used in the routing module */
  public static Route = {
    path: 'office-hours/:event_id/get-help',
    title: 'Office Hours Get Help',
    component: OfficeHoursGetHelpComponent,
    canActivate: [officeHourPageGuard(['Student'])]
  };

  /** Office hour event ID to load the queue for */
  ohEventId: number;

  /** Encapsulated signal to store the data */
  data: WritableSignal<OfficeHourGetHelpOverview | undefined> =
    signal(undefined);

  /** Stores subscription to the timer observable that refreshes data every 10s */
  timer!: Subscription;

  /** Office Hour Ticket Editor Form */
  public ticketForm = this.formBuilder.group({
    type: new FormControl(0, [Validators.required]),
    assignmentSection: new FormControl('', [Validators.required]),
    codeSection: new FormControl('', [Validators.required]),
    conceptsSection: new FormControl('', [Validators.required]),
    attemptSection: new FormControl('', [Validators.required]),
    description: new FormControl('', [Validators.required]),
    link: new FormControl('', [Validators.required])
  });

  /** Connection to the office hours get help websocket */
  webSocketSubject$: WebSocketSubject<any>;

  constructor(
    private route: ActivatedRoute,
    protected formBuilder: FormBuilder,
    private snackBar: MatSnackBar,
    protected myCoursesService: MyCoursesService
  ) {
    // Load information from the parent route
    this.ohEventId = this.route.snapshot.params['event_id'];
    // Load the web socket connection
    const url = `wss://${window.location.host}/ws/office-hours/${this.ohEventId}/get-help?token=${localStorage.getItem('bearerToken')}`;
    this.webSocketSubject$ = webSocket({
      url: url
    });
  }

  ngOnInit(): void {
    this.webSocketSubject$.subscribe((value) => {
      const json: OfficeHourGetHelpOverviewJson = JSON.parse(value);
      const overview = parseOfficeHourGetHelpOverviewJson(json);
      this.data.set(overview);
    });
  }

  ngOnDestroy(): void {
    this.webSocketSubject$.complete();
  }

  isFormValid(): boolean {
    let contentFieldsValid =
      this.ticketForm.controls['type'].value === 1
        ? this.ticketForm.controls['assignmentSection'].value !== '' &&
          this.ticketForm.controls['codeSection'].value !== '' &&
          this.ticketForm.controls['conceptsSection'].value !== '' &&
          this.ticketForm.controls['attemptSection'].value !== ''
        : this.ticketForm.controls['description'].value !== '';

    let linkFieldValid =
      this.data()!.event_mode !== 'Virtual - Student Link' ||
      this.ticketForm.controls['link'].value !== '';

    return contentFieldsValid && linkFieldValid;
  }

  /** Cancels a ticket and reloads the queue data */
  cancelTicket(ticket: OfficeHourTicketOverview): void {
    let action: GetHelpWebSocketData = {
      action: GetHelpWebSocketAction.CANCEL,
      id: ticket.id,
      new_ticket: null
    };
    this.webSocketSubject$.next(action);
  }

  submitTicketForm() {
    let form_description: string = '';
    let form_type: number = this.ticketForm.controls['type'].value!;

    /* Below is logic for checking form values and assigning the correct
      TicketType and ticket description accordingly
    */
    if (this.ticketForm.controls['type'].value === 0) {
      form_description =
        '**Conceptual Question**:  \n' +
        (this.ticketForm.controls['description'].value ?? '');
    } else {
      // Concatenates form description together and adds in new line characters
      // NOTE: Two spaces in front of \n is required.
      form_description =
        '**Assignment Part**:  \n' +
        (this.ticketForm.controls['assignmentSection'].value ?? '') +
        '  \n  \n**Goal**:  \n' +
        (this.ticketForm.controls['codeSection'].value ?? '') +
        '  \n  \n**Concepts**:  \n' +
        (this.ticketForm.controls['conceptsSection'].value ?? '') +
        '  \n  \n**Tried**:  \n' +
        (this.ticketForm.controls['attemptSection'].value ?? '');
    }

    if (this.data()!.event_mode === 'Virtual - Student Link') {
      form_description =
        form_description +
        ' \nLink: ' +
        (this.ticketForm.controls['link'].value ?? '');
    }

    // Create ticket draft from inputted ticket information
    let ticketDraft: TicketDraft = {
      office_hours_id: this.ohEventId,
      description: form_description,
      type: form_type
    };

    // Create the web socket object
    const action: GetHelpWebSocketData = {
      action: GetHelpWebSocketAction.CREATE,
      id: null,
      new_ticket: ticketDraft
    };

    this.webSocketSubject$.next(action);
  }
}
