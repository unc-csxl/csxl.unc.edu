import { Component } from '@angular/core';
import { flushMicrotasks } from '@angular/core/testing';

@Component({
  selector: 'course-card-widget',
  templateUrl: './course-card-widget.html',
  styleUrls: ['./course-card-widget.css']
})
export class CourseCard {
  constructor() {}

  openDialog() {
    console.log('hi');
  }
}
