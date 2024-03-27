import { Component, Input } from '@angular/core';
import { flushMicrotasks } from '@angular/core/testing';
import { OfficeHoursSectionDetails } from '../../office-hours.models';

@Component({
  selector: 'course-card-widget',
  templateUrl: './course-card-widget.html',
  styleUrls: ['./course-card-widget.css']
})
export class CourseCard {
  /** The course to show */
  @Input() section!: OfficeHoursSectionDetails;
  constructor() {}

  openDialog() {
    console.log('hi');
  }
}
