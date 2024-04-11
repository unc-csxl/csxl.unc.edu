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
import { ActivatedRoute } from '@angular/router';

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
    private route: ActivatedRoute
  ) {
    this.sectionId = this.route.snapshot.params['id'];
  }

  ngOnInit() {
    this.getRooms();
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
    // Date validation for the dates entered in the form; default date is the current date
    let event_date_start_time: Date;
    if (this.eventForm.value.start_time) {
      event_date_start_time = new Date(this.eventForm.value.start_time);
    } else {
      event_date_start_time = new Date();
    }
    let end_time: Date;
    if (this.eventForm.value.end_time) {
      end_time = new Date(this.eventForm.value.end_time);
    } else {
      end_time = new Date();
    }
    if (this.section) {
      let event_draft: OfficeHoursEventDraft = {
        // TODO: Un-hard code section
        oh_section: this.section,
        room: { id: this.eventForm.value.location ?? '' },
        type: event_type,
        description: this.eventForm.value.description ?? '',
        location_description: this.eventForm.value.location_description ?? '',
        event_date: event_date_start_time.toISOString().slice(0, 10),
        start_time: event_date_start_time,
        end_time: end_time
      };
      this.officeHoursService.createEvent(event_draft).subscribe({
        next: (event) => console.log(event) // remove console.log later -> for demo/debug purposes
      });
      this.eventForm.reset();
    }
    // TODO: bring user to new location
  }
}
