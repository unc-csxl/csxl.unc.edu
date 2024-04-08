import { Component, Input, OnInit } from '@angular/core';
import { OfficeHoursService } from '../../office-hours.service';
import {
  OfficeHoursEvent,
  OfficeHoursEventType
} from '../../office-hours.models';

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
