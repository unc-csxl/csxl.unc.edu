/**
 * The Event Creation Form allows TAs, GTAs, and Instructors to create new Office Hours Events.
 *
 * @author Sadie Amato, Madelyn Andrews, Bailey DeSouza, Meghan Sun
 * @copyright 2024
 * @license MIT
 */

import { Component, OnInit } from '@angular/core';
import { OfficeHoursService } from '../office-hours.service';
import { FormBuilder, FormControl, FormGroup } from '@angular/forms';
import {
  OfficeHoursEventDraft,
  OfficeHoursEventModeType,
  OfficeHoursEventType,
  OfficeHoursSectionDetails,
  Weekday
} from '../office-hours.models';
import { AcademicsService } from 'src/app/academics/academics.service';
import { Room } from 'src/app/academics/academics.models';
import { ActivatedRoute, Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-event-creation-form',
  templateUrl: './event-creation-form.component.html',
  styleUrls: ['./event-creation-form.component.css']
})
export class EventCreationFormComponent implements OnInit {
  public static Routes = [
    {
      path: 'ta/:id/create-new-event',
      title: 'COMP 110: Intro to Programming',
      component: EventCreationFormComponent,
      canActivate: []
    },
    {
      path: 'instructor/:id/create-new-event',
      title: 'COMP 110: Intro to Programming',
      component: EventCreationFormComponent,
      canActivate: []
    }
  ];

  selected = [];
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
  eventForm: FormGroup;

  /* Holds Information About Virtual Room */
  virtualRoom: Room | undefined;

  /* Section that the Office Hours event is being held for */
  isVirtualOurLink: boolean = false;
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
    this.eventForm = this.formBuilder.group({
      event_type: '',
      event_mode: '',
      description: '',
      event_date: '',
      start_time: '',
      end_time: '',
      recurring_start_date: '',
      recurring_end_date: '',
      selected_week_days: [],
      frequency: 'One Time',
      location: '',
      location_description: ''
    });
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
    // Logic for assigning the correct OfficeHoursEventType enum
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
  mapEventType(eventType: string): OfficeHoursEventType {
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

  mapEventMode(eventMode: string): OfficeHoursEventModeType {
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

  buildStartTime(frequency_type: string): string {
    return (
      (frequency_type === 'One Time'
        ? this.eventForm.value.event_date
        : this.eventForm.value.recurring_start_date) +
      'T' +
      this.eventForm.value.start_time
    );
  }

  buildEndTime(frequency_type: string): string {
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
