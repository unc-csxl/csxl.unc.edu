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
import { Title } from '@angular/platform-browser';

/** Store both possible titles as strings to flash between them easily */
const ORIGINAL_TITLE: string = 'Office Hours Get Help';
const NOTIFICATION_TITLE: string = 'Ticket Called!';

/** Store notification audio */
const CHIME = new Audio('assets/office-hours-notif.wav');

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

  /** Stores subscription to a timer observable for flashing the title for notifications */
  titleFlashTimer: Subscription | undefined;

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
    protected myCoursesService: MyCoursesService,
    private titleService: Title
  ) {
    // Load information from the parent route
    this.ohEventId = this.route.snapshot.params['event_id'];
    // Load the web socket connection
    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const url = `${protocol}://${window.location.host}/ws/office-hours/${this.ohEventId}/get-help?token=${localStorage.getItem('bearerToken')}`;
    this.webSocketSubject$ = webSocket({
      url: url
    });
  }

  ngOnInit(): void {
    console.log('Attempt to connect');
    this.webSocketSubject$.subscribe({
      next: (value) => {
        const json: OfficeHourGetHelpOverviewJson = JSON.parse(value);
        const overview = parseOfficeHourGetHelpOverviewJson(json);
        console.log(overview);
        this.handleNotification(overview);
        this.data.set(overview);
      }
    });
  }

  /** Remove the timer subscriptions when the view is destroyed so polling/flashing does not persist on other pages */
  ngOnDestroy(): void {
    this.webSocketSubject$.complete();
    this.titleFlashTimer?.unsubscribe();
  }

  /** Sends a notification if necessary on each pollData call */
  handleNotification(getHelpData: OfficeHourGetHelpOverview): void {
    /**
     * If a ticket exists in the new data, and its state is Called, and if the
     * ticket existed in the old data and its state was Queued, send a
     * notification to the student. If not, stop the flashing subscription
     * (if the flashing existed).
     */
    let notify: boolean = false;
    /* Test notification condition and store result in notify */
    if (
      getHelpData.ticket &&
      getHelpData.ticket.state === 'Called' &&
      this.data() &&
      this.data()!.ticket &&
      this.data()!.ticket!.state === 'Queued'
    ) {
      notify = true;
    }
    /* Notification behavior based on result stored in notify */
    if (notify) {
      CHIME.play();
      this.titleFlashTimer = timer(0, 1000).subscribe(() => {
        this.titleService.setTitle(
          this.titleService.getTitle() === NOTIFICATION_TITLE
            ? ORIGINAL_TITLE
            : NOTIFICATION_TITLE
        );
      });
    } else {
      this.titleFlashTimer?.unsubscribe();
      this.titleService.setTitle(ORIGINAL_TITLE);
    }
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
