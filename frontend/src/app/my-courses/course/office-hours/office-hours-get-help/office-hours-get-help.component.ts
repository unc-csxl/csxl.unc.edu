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
  OfficeHourGetHelpOverview,
  OfficeHourTicketOverview,
  TicketDraft
} from 'src/app/my-courses/my-courses.model';
import { Subscription, timer } from 'rxjs';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Title } from '@angular/platform-browser';

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

  /** Stores subscription to a timer observable for flashing the title for notifications */
  titleFlashTimer: Subscription | undefined;

  /** Store both possible titles as strings to flash between them easily */
  originalTitle: string = 'Office Hours Get Help';
  notificationTitle: string = 'Ticket Called!';

  /** Store notification audio */
  chime = new Audio('assets/office-hours-notif.wav');

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

  constructor(
    private route: ActivatedRoute,
    protected formBuilder: FormBuilder,
    private snackBar: MatSnackBar,
    protected myCoursesService: MyCoursesService,
    private titleService: Title
  ) {
    // Load information from the parent route
    this.ohEventId = this.route.snapshot.params['event_id'];
  }

  /** Create a timer subscription to poll office hour data at an interval at view initalization */
  ngOnInit(): void {
    this.timer = timer(0, 10000).subscribe(() => {
      this.pollData();
    });
  }

  /** Remove the timer subscriptions when the view is destroyed so polling/flashing does not persist on other pages */
  ngOnDestroy(): void {
    this.timer.unsubscribe();
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
    if (getHelpData.ticket && getHelpData.ticket.state === 'Called') {
      if (this.data() && this.data()!.ticket &&
        this.data()!.ticket!.state === 'Queued') {
        notify = true;
      }
    }
    if (notify) {
      this.chime.play();
      this.titleFlashTimer = timer(0, 1000).subscribe(() => {
        this.titleService.setTitle(
          this.titleService.getTitle() === this.notificationTitle ?
            this.originalTitle : this.notificationTitle);
      })
    } else {
      this.titleFlashTimer?.unsubscribe();
      this.titleService.setTitle(this.originalTitle);
    }
  }

  /** Loads office hours data */
  pollData(): void {
    this.myCoursesService
      .getOfficeHoursHelpOverview(this.ohEventId)
      .subscribe((getHelpData) => {
        this.handleNotification(getHelpData);
        this.data.set(getHelpData);
      });
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
    this.myCoursesService.cancelTicket(ticket.id).subscribe({
      next: (_) => {
        this.pollData();
        this.snackBar.open('Ticket cancelled', '', { duration: 5000 });
      },
      error: (err) => this.snackBar.open(err, '', { duration: 2000 })
    });
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

    this.myCoursesService.createTicket(ticketDraft).subscribe({
      next: (_) => {
        this.pollData();
      },
      error: (_) => {
        this.snackBar.open(`Could not create a ticket at this time.`, '', {
          duration: 2000
        });
      }
    });
  }
}
