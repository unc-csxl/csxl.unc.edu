/**
 * The Event Creation Form allows TAs, GTAs, and Instructors to create new Office Hours Events
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
  // TODO: Un-hardcode this route
  public static Routes = [
    {
      path: 'ta/spring-2024/:id/create-new-event',
      title: 'COMP 110: Intro to Programming',
      component: EventCreationFormComponent,
      canActivate: []
    },
    {
      path: 'instructor/spring-2024/:id/create-new-event',
      title: 'COMP 110: Intro to Programming',
      component: EventCreationFormComponent,
      canActivate: []
    }
  ];

  rooms: Room[] = [];
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

  ngOnInit() {
    this.getRooms();
    this.getSection();
  }

  public eventForm = this.formBuilder.group({
    event_type: '',
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
    // Below is logic for assigning the correct OfficeHoursEventtype
    let event_type: OfficeHoursEventType;
    switch (this.eventForm.value.event_type) {
      case 'office_hours':
        event_type = OfficeHoursEventType.OFFICE_HOURS;
        break;
      case 'office_hours_virtual':
        event_type = OfficeHoursEventType.VIRTUAL_OFFICE_HOURS;
        break;
      case 'tutoring':
        event_type = OfficeHoursEventType.TUTORING;
        break;
      case 'virtual_tutoring':
        event_type = OfficeHoursEventType.VIRTUAL_TUTORING;
        break;
      case 'review_session':
        event_type = OfficeHoursEventType.REVIEW_SESSION;
        break;
      case 'review_session_virtual':
        event_type = OfficeHoursEventType.VIRTUAL_REVIEW_SESSION;
        break;
      default:
        event_type = OfficeHoursEventType.OFFICE_HOURS;
    }
    if (!this.eventForm.value.start_time) {
      this.eventForm.value.start_time = '';
    }
    if (!this.eventForm.value.end_time) {
      this.eventForm.value.end_time = '';
    }
    if (this.section) {
      let event_draft: OfficeHoursEventDraft = {
        // TODO: Un-hard code section
        oh_section: this.section,
        room: { id: this.eventForm.value.location ?? '' },
        type: event_type,
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
    // TODO: bring user to new location
  }

  private onSuccess(): void {
    this.snackBar.open('You have created a new event!', '', {
      duration: 3000
    });
    this.router.navigate(['../'], { relativeTo: this.activatedRoute });
    this.eventForm.reset();
  }

  private onError(err: any): void {
    this.snackBar.open('Error: Unable to create event', '', {
      duration: 2000
    });
  }
}
