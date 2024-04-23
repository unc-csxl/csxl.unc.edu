/**
 * The Event Creation Form allows TAs, GTAs, and Instructors to create new Office Hours Events.
 *
 * @author Sadie Amato, Madelyn Andrews, Bailey DeSouza, Meghan Sun
 * @copyright 2024
 * @license MIT
 */

import { Component, OnInit } from '@angular/core';
import { OfficeHoursService } from '../office-hours.service';
import { FormBuilder } from '@angular/forms';
import {
  OfficeHoursEventDraft,
  OfficeHoursEventModeType,
  OfficeHoursEventType,
  OfficeHoursSectionDetails
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

  /* List of available rooms to hold Office Hours event */
  rooms: Room[] = [];

  /* Section that the Office Hours event is being held for */
  sectionId: number;
  section: OfficeHoursSectionDetails | undefined;

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
  }

  /* Get rooms and associated section upon initialization */
  ngOnInit() {
    this.getRooms();
    this.getSection();
  }

  /* EventForm contains data pertaining to event that is being created/modified */
  public eventForm = this.formBuilder.group({
    event_type: '',
    event_mode: '',
    description: '',
    start_time: '',
    end_time: '',
    location: '',
    location_description: ''
  });

  getRooms() {
    this.academicsService.getRooms().subscribe((rooms) => {
      this.rooms = rooms;
    });
  }

  getSection() {
    this.officeHoursService
      .getSection(this.sectionId)
      .subscribe((section) => (this.section = section));
  }

  onSubmit() {
    // Logic for assigning the correct OfficeHoursEventType enum
    let event_type: OfficeHoursEventType;
    switch (this.eventForm.value.event_type) {
      case 'office_hours':
        event_type = OfficeHoursEventType.OFFICE_HOURS;
        break;
      case 'tutoring':
        event_type = OfficeHoursEventType.TUTORING;
        break;
      case 'review_session':
        event_type = OfficeHoursEventType.REVIEW_SESSION;
        break;
      default:
        event_type = OfficeHoursEventType.OFFICE_HOURS;
    }

    let event_mode: OfficeHoursEventModeType;
    switch (this.eventForm.value.event_mode) {
      case 'in_person':
        event_mode = OfficeHoursEventModeType.IN_PERSON;
        break;
      case 'virtual_our_link':
        event_mode = OfficeHoursEventModeType.VIRTUAL_OUR_LINK;
        break;
      case 'virtual_student_link':
        event_mode = OfficeHoursEventModeType.VIRTUAL_STUDENT_LINK;
        break;
      default:
        event_mode = OfficeHoursEventModeType.IN_PERSON;
    }

    // Ensure start and end times aren't none
    if (!this.eventForm.value.start_time) {
      this.eventForm.value.start_time = '';
    }
    if (!this.eventForm.value.end_time) {
      this.eventForm.value.end_time = '';
    }

    // Ensure that section must not be null to create/edit event
    if (this.section) {
      // Create event draft model from form values
      let event_draft: OfficeHoursEventDraft = {
        oh_section: this.section,
        room: { id: this.eventForm.value.location ?? '' },
        type: event_type,
        mode: event_mode,
        description: this.eventForm.value.description ?? '',
        location_description: this.eventForm.value.location_description ?? '',
        event_date: this.eventForm.value.start_time.slice(0, 10),
        start_time: this.eventForm.value.start_time,
        end_time: this.eventForm.value.end_time
      };
      this.officeHoursService.createEvent(event_draft).subscribe({
        next: () => this.onSuccess(),
        error: (err) => this.onError(err)
      });
    }
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
  }
}
