/**
 * The Event Creation Form allows TAs, GTAs, and Instructors to create new Office Hours Events.
 *
 * @author Sadie Amato, Madelyn Andrews, Bailey DeSouza, Meghan Sun
 * @copyright 2024
 * @license MIT
 */

import { Component, OnInit } from '@angular/core';
import { OfficeHoursService } from '../office-hours.service';
import {
  AbstractControl,
  FormBuilder,
  FormControl,
  FormGroup,
  ValidationErrors,
  ValidatorFn,
  Validators
} from '@angular/forms';
import {
  OfficeHoursEventDraft,
  OfficeHoursEventModeType,
  OfficeHoursEventType,
  OfficeHoursSectionDetails,
  Weekday
} from '../office-hours.models';
import { AcademicsService } from 'src/app/academics/academics.service';
import { Room, RosterRole } from 'src/app/academics/academics.models';
import {
  ActivatedRoute,
  ActivatedRouteSnapshot,
  ResolveFn,
  Router
} from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { sectionResolver } from '../office-hours.resolver';

let titleResolver: ResolveFn<string> = (route: ActivatedRouteSnapshot) => {
  return route.parent!.data['section']?.title ?? 'Section Not Found';
};

@Component({
  selector: 'app-event-creation-form',
  templateUrl: './event-creation-form.component.html',
  styleUrls: ['./event-creation-form.component.css']
})
export class EventCreationFormComponent implements OnInit {
  public static Routes = [
    {
      path: 'ta/:id/create-new-event',
      component: EventCreationFormComponent,
      canActivate: [],
      resolve: { section: sectionResolver },
      children: [
        {
          path: '',
          title: titleResolver,
          component: EventCreationFormComponent
        }
      ]
    },
    {
      path: 'instructor/:id/create-new-event',
      component: EventCreationFormComponent,
      canActivate: [],
      resolve: { section: sectionResolver },
      children: [
        {
          path: '',
          title: titleResolver,
          component: EventCreationFormComponent
        }
      ]
    }
  ];

  /* List of available rooms to hold Office Hours event */
  rooms: Room[] = [];

  weekdays = [
    Weekday.Monday,
    Weekday.Tuesday,
    Weekday.Wednesday,
    Weekday.Thursday,
    Weekday.Friday,
    Weekday.Saturday,
    Weekday.Sunday
  ];
  frequencyOptions = ['One Time', 'Daily', 'Weekly'];
  /* Section that the Office Hours event is being held for */
  sectionId: number;
  section: OfficeHoursSectionDetails | undefined;

  // RosterRole to determine if user can view this routed component
  rosterRole: RosterRole | undefined;
  eventForm: FormGroup;

  /* Holds Information About Virtual Room */
  virtualRoom: Room | undefined;

  /* Section that the Office Hours event is being held for */
  isVirtualOurLink: boolean = false;

  isStartAndEndDateFilledIn() {
    return (
      this.eventForm.value.recurring_start_date !== '' &&
      this.eventForm.value.recurring_end_date !== ''
    );
  }

  onFrequencyChange(event: any) {
    if (this.isFrequencyWeekly()) {
      // Set Validators
      this.eventForm.controls['event_date'].setValidators([]);
      this.eventForm.controls['recurring_start_date'].setValidators([
        Validators.required
      ]);
      this.eventForm.controls['recurring_end_date'].setValidators([
        Validators.required
      ]);

      this.eventForm.controls['selected_week_days'].setValidators([
        Validators.required
      ]);
    } else if (this.isFrequencyDaily()) {
      this.eventForm.controls['event_date'].setValidators([]);
      this.eventForm.controls['selected_week_days'].setValidators([]);

      // Set Validators
      this.eventForm.controls['recurring_start_date'].setValidators([
        Validators.required
      ]);
      this.eventForm.controls['recurring_end_date'].setValidators([
        Validators.required
      ]);
    } else {
      this.eventForm.controls['selected_week_days'].setValidators([]);

      this.eventForm.controls['recurring_start_date'].setValidators([]);

      this.eventForm.controls['recurring_end_date'].setValidators([]);

      this.eventForm.controls['event_date'].setValidators([
        Validators.required
      ]);
    }
    console.log(this.eventForm);
    this.eventForm.controls['selected_week_days'].updateValueAndValidity();
    this.eventForm.controls['recurring_start_date'].updateValueAndValidity();
    this.eventForm.controls['recurring_end_date'].updateValueAndValidity();
    this.eventForm.controls['event_date'].updateValueAndValidity();
  }

  dateRangeValidator(): ValidatorFn {
    return (form: AbstractControl): ValidationErrors | null => {
      // If One Time, Ignore this Validator
      const frequency = form.root.get('frequency')?.value;
      if (frequency == 'One Time') {
        return null;
      }
      const startDateValue = form.root.get('recurring_start_date')?.value;
      const endDateValue = form.root.get('recurring_end_date')?.value;

      // Check if either start date or end date is null
      if (
        startDateValue === '' ||
        endDateValue === '' ||
        !startDateValue ||
        !endDateValue
      ) {
        return null; // Return null if one of the dates is not set
      }

      const startDate = new Date(startDateValue);
      const endDate = new Date(endDateValue);

      // Check If Start Date is Before End Date
      if (startDate > endDate) {
        return { invalidDateRange: true };
      }
      // Calculate the difference in milliseconds
      const differenceMs = Math.abs(endDate.getTime() - startDate.getTime());

      // Convert the difference to weeks
      const differenceWeeks = differenceMs / (1000 * 60 * 60 * 24 * 7);

      // Check if the difference is less than or equal to 16 weeks
      return differenceWeeks <= 16 ? null : { rangeExceedsLimit: true };
    };
  }

  // TODO: Check for Date Range of Greater than 4 monthss
  isValidDateRange() {
    const parsedTime1 = new Date(this.eventForm.value.recurring_start_date);
    const parsedTime2 = new Date(this.eventForm.value.recurring_end_date);

    // Compare the parsed times
    return parsedTime1 <= parsedTime2;
  }

  isDateRangeWithinFourMonths(): boolean {
    const startDate = new Date(this.eventForm.value.recurring_start_date);
    const endDate = new Date(this.eventForm.value.recurring_end_date);
    // Calculate the difference in milliseconds
    const differenceMs = Math.abs(endDate.getTime() - startDate.getTime());

    // Convert the difference to weeks
    const differenceWeeks = differenceMs / (1000 * 60 * 60 * 24 * 7);

    // Check if the difference is less than 16 weeks
    if (differenceWeeks > 16) {
      // Return validation error if the range is more than 16 weeks
      return false;
    }

    // Return null if validation passes
    return true;
  }

  constructor(
    public officeHoursService: OfficeHoursService,
    protected formBuilder: FormBuilder,
    public academicsService: AcademicsService,
    private route: ActivatedRoute,
    protected snackBar: MatSnackBar,
    private router: Router,
    private activatedRoute: ActivatedRoute
  ) {
    this.sectionId = this.route.snapshot.params['id'];
    this.getRosterRole();
    this.eventForm = this.formBuilder.group(
      {
        event_type: ['', Validators.required],
        event_mode: ['', Validators.required],
        description: '',
        event_date: ['', Validators.required],
        start_time: ['', Validators.required],
        end_time: ['', Validators.required],
        recurring_start_date: [''],
        recurring_end_date: '',
        selected_week_days: [],
        frequency: ['One Time', Validators.required],
        location: ['', Validators.required],
        location_description: ''
      },
      { validators: [this.dateRangeValidator()] }
    );
  }

  /* Get rooms and associated section upon initialization */
  ngOnInit() {
    this.getRooms();
    this.getSection();

    // Prevent Chrome From Crashing In Form Dropdown
    document.addEventListener('DOMNodeInserted', function () {
      const elements = document.querySelectorAll('[aria-owns]');

      elements.forEach((element) => {
        element.removeAttribute('aria-owns');
      });
    });
  }

  // user selects Monday and Sunday

  isFrequencyWeekly(): boolean {
    return this.eventForm.value.frequency === 'Weekly';
  }

  isFrequencyDaily(): boolean {
    return this.eventForm.value.frequency === 'Daily';
  }

  isFrequencyOneTime(): boolean {
    return this.eventForm.value.frequency === 'One Time';
  }

  getAbbreviatedName(day: Weekday): string {
    switch (day) {
      case Weekday.Monday:
        return 'Mon';
      case Weekday.Tuesday:
        return 'Tue';
      case Weekday.Wednesday:
        return 'Wed';
      case Weekday.Thursday:
        return 'Thu';
      case Weekday.Friday:
        return 'Fri';
      case Weekday.Saturday:
        return 'Sat';
      case Weekday.Sunday:
        return 'Sun';
      default:
        return '';
    }
  }
  /* EventForm contains data pertaining to event that is being created/modified */

  getRosterRole() {
    this.academicsService
      .getMembershipBySection(this.sectionId)
      .subscribe((role) => (this.rosterRole = role.member_role));
  }

  // Handles Room Location Value According to Event Mode Selection Changes
  onEventModeChange(event: any) {
    // CASE: If Event Mode is Virtual, Will Set Default Room Location to Virtual
    if (event.value.includes('virtual')) {
      if (this.virtualRoom) {
        (this.eventForm.get('location') as FormControl).setValue(
          this.virtualRoom.id
        );
      }
      // CASE: If Location has been selected but switch to In-Person, will reset selection for Room Location
    } else if (
      event.value.includes('in_person') &&
      this.eventForm.value.location !== ''
    ) {
      (this.eventForm.get('location') as FormControl).setValue(null);
    }

    this.isVirtualOurLink = event.value.includes('our_link');
  }

  getRooms() {
    this.academicsService.getRooms().subscribe((rooms) => {
      this.rooms = rooms;
      this.virtualRoom = rooms.find((room) => room.id === 'Virtual');
    });
  }

  getSection() {
    this.officeHoursService
      .getSection(this.sectionId)
      .subscribe((section) => (this.section = section));
  }

  onSubmit() {
    // Logic for assigning the correct OfficeHoursEventType and OfficeHoursEventMode enum
    let event_type: OfficeHoursEventType = this.mapEventType(
      this.eventForm.value.event_type
    );

    let event_mode: OfficeHoursEventModeType = this.mapEventMode(
      this.eventForm.value.event_mode
    );

    // Ensure start and end times aren't none
    if (!this.eventForm.value.start_time) {
      this.eventForm.value.start_time = '';
    }
    if (!this.eventForm.value.end_time) {
      this.eventForm.value.end_time = '';
    }

    // Ensure that section must not be null to create/edit event
    if (this.section) {
      let start_time = this.buildStartTime(this.eventForm.value.frequency);
      let end_time = this.buildEndTime(this.eventForm.value.frequency);

      var event_draft: OfficeHoursEventDraft = {
        oh_section: this.section,
        room: { id: this.eventForm.value.location ?? '' },
        type: event_type,
        mode: event_mode,
        description: this.eventForm.value.description ?? '',
        location_description: this.eventForm.value.location_description ?? '',
        event_date: this.eventForm.value.event_date,
        start_time: start_time,
        end_time: end_time
      };

      // Recurring Event Variable Indicators
      let recurring_start_date = this.eventForm.value.recurring_start_date;
      let recurring_end_date = this.eventForm.value.recurring_end_date;
      let selected_week_days = this.eventForm.value.selected_week_days;

      switch (this.eventForm.value.frequency) {
        case 'One Time':
          this.officeHoursService.createEvent(event_draft).subscribe({
            next: () => this.onSuccess(),
            error: (err) => this.onError(err)
          });
          break;

        case 'Daily':
          // Set Event Date to First Start Date
          event_draft.event_date = recurring_start_date;

          this.officeHoursService
            .createEventsDaily(
              event_draft,
              recurring_start_date,
              recurring_end_date
            )
            .subscribe({
              next: () => this.onSuccess(),
              error: (err) => this.onError(err)
            });
          break;

        case 'Weekly':
          // Set Event Date to First Start Date
          event_draft.event_date = recurring_start_date;

          this.officeHoursService
            .createEventsWeekly(
              event_draft,
              recurring_start_date,
              recurring_end_date,
              selected_week_days
            )
            .subscribe({
              next: () => this.onSuccess(),
              error: (err) => this.onError(err)
            });
          break;

        default:
      }
    }
  }
  private mapEventType(eventType: string): OfficeHoursEventType {
    switch (eventType) {
      case 'office_hours':
        return OfficeHoursEventType.OFFICE_HOURS;
      case 'tutoring':
        return OfficeHoursEventType.TUTORING;
      case 'review_session':
        return OfficeHoursEventType.REVIEW_SESSION;
      default:
        return OfficeHoursEventType.OFFICE_HOURS;
    }
  }

  private mapEventMode(eventMode: string): OfficeHoursEventModeType {
    switch (eventMode) {
      case 'in_person':
        return OfficeHoursEventModeType.IN_PERSON;
      case 'virtual_our_link':
        return OfficeHoursEventModeType.VIRTUAL_OUR_LINK;
      case 'virtual_student_link':
        return OfficeHoursEventModeType.VIRTUAL_STUDENT_LINK;
      default:
        return OfficeHoursEventModeType.IN_PERSON;
    }
  }

  private buildStartTime(frequency_type: string): string {
    return (
      (frequency_type === 'One Time'
        ? this.eventForm.value.event_date
        : this.eventForm.value.recurring_start_date) +
      'T' +
      this.eventForm.value.start_time
    );
  }

  private buildEndTime(frequency_type: string): string {
    return (
      (frequency_type === 'One Time'
        ? this.eventForm.value.event_date
        : this.eventForm.value.recurring_start_date) +
      'T' +
      this.eventForm.value.end_time
    );
  }

  /* On successful event creation, navigate back to section home */
  private onSuccess(): void {
    this.snackBar.open('You have created a new event!', '', {
      duration: 3000
    });
    this.router.navigate(['../'], { relativeTo: this.activatedRoute });
    this.eventForm.reset();
  }

  /* On error, display message informing user */
  private onError(err: any): void {
    this.snackBar.open('Error: Unable to create event', '', {
      duration: 2000
    });
    console.log(err.description);
  }
}
