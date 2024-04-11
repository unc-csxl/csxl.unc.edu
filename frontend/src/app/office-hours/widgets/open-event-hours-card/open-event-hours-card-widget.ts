/**
 * The Open Event Hours Card is used on the Office Hours Home page and shows
 * what events are currently open + their location and times
 *
 * @author Sadie Amato, Madelyn Andrews, Bailey DeSouza, Meghan Sun
 * @copyright 2024
 * @license MIT
 */

import { Component, Input } from '@angular/core';
import { flushMicrotasks } from '@angular/core/testing';
import {
  OfficeHoursEvent,
  OfficeHoursEventType
} from '../../office-hours.models';

@Component({
  selector: 'open-event-hours-card-widget',
  templateUrl: './open-event-hours-card-widget.html',
  styleUrls: ['./open-event-hours-card-widget.css']
})
export class OpenEventHoursCard {
  @Input() event!: OfficeHoursEvent;

  constructor() {}

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
