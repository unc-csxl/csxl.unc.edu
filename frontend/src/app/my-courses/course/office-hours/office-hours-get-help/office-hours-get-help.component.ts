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
  OfficeHourTicketOverview
} from 'src/app/my-courses/my-courses.model';
import { Subscription, timer } from 'rxjs';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import {
  TicketDraft,
  TicketType
} from 'src/app/office-hours/office-hours.models';
import { MatSnackBar } from '@angular/material/snack-bar';

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
    type: new FormControl('Assignment Help', [Validators.required]),
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
    protected myCoursesService: MyCoursesService
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

  /** Remove the timer subscription when the view is destroyed so polling does not persist on other pages */
  ngOnDestroy(): void {
    this.timer.unsubscribe();
  }

  /** Loads office hours data */
  pollData(): void {
    this.myCoursesService
      .getOfficeHoursHelpOverview(this.ohEventId)
      .subscribe((getHelpData) => {
        this.data.set(getHelpData);
      });
  }

  isFormValid(): boolean {
    let contentFieldsValid =
      this.ticketForm.controls['type'].value === 'Assignment Help'
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
    let form_type: string = this.ticketForm.controls['type'].value!;

    /* Below is logic for checking form values and assigning the correct
      TicketType and ticket description accordingly
    */
    if (this.ticketForm.controls['type'].value === 'Conceptual Help') {
      form_description =
        'Conceptual: ' + (this.ticketForm.controls['description'].value ?? '');
    } else {
      // Concatenates form description together and adds in new line characters
      form_description =
        'Assignment Part: ' +
        (this.ticketForm.controls['assignmentSection'].value ?? '') +
        ' \nGoal: ' +
        (this.ticketForm.controls['codeSection'].value ?? '') +
        ' \nConcepts: ' +
        (this.ticketForm.controls['conceptsSection'].value ?? '') +
        ' \nTried: ' +
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
      oh_event: { id: this.ohEventId },
      description: form_description,
      type: form_type,
      // TODO: if adding multiple creators (group tickets), would add users here
      creators: []
    };

    this.myCoursesService.createTicket(ticketDraft).subscribe({
      next: (_) => {
        this.pollData();
      },
      error: (err) => {
        /** */
      }
    });
  }
}
