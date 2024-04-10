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
import { OfficeHoursEvent, TicketDetails } from '../office-hours.models';
import { OfficeHoursService } from '../office-hours.service';
import { AcademicsService } from 'src/app/academics/academics.service';
import { RosterRole } from 'src/app/academics/academics.models';

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
  rosterRole: RosterRole | null;
  userTickets: TicketDetails[] = [];

  constructor(
    private route: ActivatedRoute,
    private officeHoursService: OfficeHoursService,
    private academicsService: AcademicsService
  ) {
    let navLinks = [
      { path: '/events', label: 'Events' },
      { path: '/history', label: 'History' }
    ];
    this.sectionId = this.route.snapshot.params['id'];
    this.rosterRole = null;
  }

  ngOnInit(): void {
    this.getCurrentEvents();
    this.checkRosterRole();
  }

  getCurrentEvents() {
    this.officeHoursService
      .getCurrentEventsBySection(this.sectionId)
      .subscribe((events) => {
        this.currentEvents = events;
      });
  }

  checkRosterRole() {
    this.academicsService
      .getMembershipBySection(this.sectionId)
      .subscribe((section_member) => {
        this.rosterRole = section_member.member_role;
        return section_member;
      });
  }
}
