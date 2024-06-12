import { Component } from '@angular/core';

@Component({
  selector: 'app-course',
  templateUrl: './course.component.html',
  styleUrls: ['./course.component.css']
})
export class CourseComponent {
  /** Route information to be used in the routing module */
  public static Route = {
    path: 'course/:id',
    title: 'Course',
    component: CourseComponent
  };

  /** Links for the tab bar */
  public links = [
    {
      label: 'Office Hours',
      path: '/course/:id/office-hours',
      icon: 'person_raised_hand'
    },
    { label: 'Roster', path: '/course/:id/roster', icon: 'groups' },
    { label: 'Settings', path: '/course/:id/settings', icon: 'settings' }
  ];
}
