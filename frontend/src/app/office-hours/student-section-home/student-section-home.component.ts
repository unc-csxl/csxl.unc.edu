/**
 * The Student Section Home Component serves as a hub for students to view office hours events, see upcoming schedules, and view their ticket history
 * 
 *
 * @author Madelyn Andrews, Bailey DeSouza, Meghan Sun, Sadie Amato
 * @copyright 2024
 * @license MIT
 */

import { Component } from '@angular/core';

@Component({
  selector: 'app-student-section-home',
  templateUrl: './student-section-home.component.html',
  styleUrls: ['./student-section-home.component.css']
})
export class StudentSectionHomeComponent {
  public static Route = {
    // placeholder route
    path: 'spring-2024/comp110',
    title: 'COMP 110: Intro to Programming',
    component: StudentSectionHomeComponent,
    canActivate: []
  };
  navLinks: any;

  constructor() {
    let navLinks = [
      { path: '/events', label: 'Events' },
      { path: '/history', label: 'History' }
    ];
  }
}
