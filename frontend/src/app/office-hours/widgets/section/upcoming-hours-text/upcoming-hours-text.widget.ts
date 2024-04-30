/**
 * The Upcoming Hours Text makes it easy to reuse upcoming hours information
 * across different parts on the Office Hours Feature
 *
 * @author Sadie Amato, Madelyn Andrews, Bailey DeSouza, Meghan Sun
 * @copyright 2024
 * @license MIT
 */

import { Component, Input, OnInit } from '@angular/core';
import { OfficeHoursService } from '../../../office-hours.service';
import {
  OfficeHoursEvent,
  OfficeHoursEventType
} from '../../../office-hours.models';

@Component({
  selector: 'upcoming-hours-text-widget',
  templateUrl: './upcoming-hours-text.widget.html',
  styleUrls: ['./upcoming-hours-text.widget.css']
})
export class UpcomingHoursText implements OnInit {
  @Input() sectionId!: number;
  upcomingHours: OfficeHoursEvent[] = [];

  constructor(private officeHoursService: OfficeHoursService) {}

  ngOnInit(): void {
    this.getUpcomingHours();
  }

  getUpcomingHours() {
    this.officeHoursService
      .getUpcomingEventsBySection(this.sectionId)
      .subscribe((hours) => {
        this.upcomingHours = hours.sort(
          (a, b) =>
            new Date(a.start_time).getTime() - new Date(b.start_time).getTime()
        );
      });
  }

  formatEventType(typeNum: number) {
    if (typeNum === OfficeHoursEventType.OFFICE_HOURS) {
      return 'Office Hours';
    } else if (typeNum === OfficeHoursEventType.TUTORING) {
      return 'Tutoring';
    } else if (typeNum === OfficeHoursEventType.REVIEW_SESSION) {
      return 'Review Session';
    } else {
      return 'error';
    }
  }
}
