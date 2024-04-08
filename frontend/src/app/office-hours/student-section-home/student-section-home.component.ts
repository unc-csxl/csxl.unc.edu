/**
 * The Student Section Home Component serves as a hub for students to view office hours events, see upcoming schedules, and view their ticket history
 *
 *
 * @author Madelyn Andrews, Bailey DeSouza, Meghan Sun, Sadie Amato
 * @copyright 2024
 * @license MIT
 */

import { Component, Input, OnInit } from '@angular/core';
import { ActivatedRoute, RouteConfigLoadEnd } from '@angular/router';
import { OfficeHoursEvent } from '../office-hours.models';
import { OfficeHoursService } from '../office-hours.service';

@Component({
  selector: 'app-student-section-home',
  templateUrl: './student-section-home.component.html',
  styleUrls: ['./student-section-home.component.css']
})
export class StudentSectionHomeComponent implements OnInit {
  public static Route = {
    // TODO: replace this route + title to be un-hardcoded
    path: 'spring-2024/:id',
    title: 'COMP 110: Intro to Programming',
    component: StudentSectionHomeComponent,
    canActivate: []
  };
  currentEvents: OfficeHoursEvent[] = [];
  sectionId: number;
  navLinks: any;

  constructor(
    private route: ActivatedRoute,
    private officeHoursService: OfficeHoursService
  ) {
    let navLinks = [
      { path: '/events', label: 'Events' },
      { path: '/history', label: 'History' }
    ];
    this.sectionId = this.route.snapshot.params['id'];
  }

  ngOnInit(): void {
    this.getCurrentEvents();
  }

  getCurrentEvents() {
    this.officeHoursService
      .getCurrentEventsBySection(this.sectionId)
      .subscribe((events) => {
        this.currentEvents = events;
      });
  }
}
