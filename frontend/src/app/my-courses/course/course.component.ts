import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-course',
  templateUrl: './course.component.html',
  styleUrls: ['./course.component.css']
})
export class CourseComponent {
  /** Links for the tab bar */
  public links = [
    {
      label: 'Office Hours',
      path: '/course/:id/office-hours',
      icon: 'person_raised_hand'
    },
    {
      label: 'Roster',
      path: `/course/${this.route.snapshot.params['term_id']}/${this.route.snapshot.params['course_id']}/roster`,
      icon: 'groups'
    },
    { label: 'Settings', path: '/course/:id/settings', icon: 'settings' }
  ];

  constructor(private route: ActivatedRoute) {}
}
