/**
 * The Student Section Home Component serves as a hub for students to view office hours events, see upcoming schedules, and view their ticket history
 *
 *
 * @author Madelyn Andrews, Bailey DeSouza, Meghan Sun, Sadie Amato
 * @copyright 2024
 * @license MIT
 */

import { Component, OnInit } from '@angular/core';
import { OfficeHoursService } from '../office-hours.service';
import { TicketDetails } from '../office-hours.models';

@Component({
  selector: 'app-student-section-home',
  templateUrl: './student-section-home.component.html',
  styleUrls: ['./student-section-home.component.css']
})
export class StudentSectionHomeComponent implements OnInit {
  public static Route = {
    // placeholder route
    path: 'spring-2024/comp110',
    title: 'COMP 110: Intro to Programming',
    component: StudentSectionHomeComponent,
    canActivate: []
  };
  navLinks: any;
  pendingTicket: TicketDetails | null = null;

  constructor(public officeHoursService: OfficeHoursService) {
    this.navLinks = [
      { path: '/events', label: 'Events' },
      { path: '/history', label: 'History' }
    ];
  }

  ngOnInit() {
    this.pendingTicket = this.officeHoursService.getCurrentTicket();

    console.log(this.pendingTicket);
  }
}
