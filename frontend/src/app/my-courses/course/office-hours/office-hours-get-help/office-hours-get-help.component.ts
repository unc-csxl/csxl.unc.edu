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
import { OfficeHourGetHelpOverview } from 'src/app/my-courses/my-courses.model';
import { Subscription, timer } from 'rxjs';
import { FormBuilder, FormControl, Validators } from '@angular/forms';

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
  submitTicketForm() {}
}
