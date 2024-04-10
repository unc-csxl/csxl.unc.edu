import { Component, Input } from '@angular/core';
import { flushMicrotasks } from '@angular/core/testing';
import {
  OfficeHoursEvent,
  OfficeHoursEventType
} from '../../office-hours.models';
import { RosterRole } from 'src/app/academics/academics.models';

@Component({
  selector: 'event-card-widget',
  templateUrl: './event-card-widget.html',
  styleUrls: ['./event-card-widget.css']
})
export class EventCard {
  @Input() event!: OfficeHoursEvent;
  // @Input() rosterRole!: RosterRole | null;
  constructor() {
    console.log('reached event card.');
  }

  formatEventType(typeNum: number) {
    if (typeNum === OfficeHoursEventType.OFFICE_HOURS) {
      return 'Office Hours';
    } else if (typeNum === OfficeHoursEventType.TUTORING) {
      return 'Tutoring';
    } else if (typeNum === OfficeHoursEventType.REVIEW_SESSION) {
      return 'Review Session';
    } else if (typeNum === OfficeHoursEventType.VIRTUAL_OFFICE_HOURS) {
      return 'Virtual Office Hours';
    } else if (typeNum === OfficeHoursEventType.VIRTUAL_TUTORING) {
      return 'Virtual Tutoring';
    } else if (typeNum === OfficeHoursEventType.VIRTUAL_REVIEW_SESSION) {
      return 'Virtual Review Session';
    } else {
      return 'error';
    }
  }
}
