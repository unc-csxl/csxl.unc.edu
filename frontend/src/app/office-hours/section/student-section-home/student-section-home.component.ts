/**
 * The Student Section Home Component serves as a hub for students to view office hours events,
 * see upcoming schedules, and view their ticket history
 *
 * @author Madelyn Andrews, Bailey DeSouza, Meghan Sun, Sadie Amato
 * @copyright 2024
 * @license MIT
 */

import { Component, Input, OnInit } from '@angular/core';
import {
  ActivatedRoute,
  ActivatedRouteSnapshot,
  ResolveFn
} from '@angular/router';
import {
  OfficeHoursEvent,
  OfficeHoursSectionDetails,
  TicketDetails
} from '../../office-hours.models';
import { OfficeHoursService } from '../../office-hours.service';
import { AcademicsService } from 'src/app/academics/academics.service';
import { RosterRole } from 'src/app/academics/academics.models';
import { sectionResolver } from '../../office-hours.resolver';

/* Resolves title to display Section as the page header */
let titleResolver: ResolveFn<string> = (route: ActivatedRouteSnapshot) => {
  return route.parent!.data['section']?.title ?? 'Section Not Found';
};

@Component({
  selector: 'app-student-section-home',
  templateUrl: './student-section-home.component.html',
  styleUrls: ['./student-section-home.component.css']
})
export class StudentSectionHomeComponent implements OnInit {
  public static Route = {
    path: ':id',
    component: StudentSectionHomeComponent,
    canActivate: [],
    resolve: { section: sectionResolver },
    children: [
      {
        path: '',
        title: titleResolver,
        component: StudentSectionHomeComponent
      }
    ]
  };

  /* Office Hours Section being displayed, along with its events and current user's tickets*/
  protected section: OfficeHoursSectionDetails;
  sectionId: number;
  currentEvents: OfficeHoursEvent[] = [];
  userTickets: TicketDetails[] = [];
  rosterRole: RosterRole | null;
  navLinks: any;

  constructor(
    private route: ActivatedRoute,
    private officeHoursService: OfficeHoursService,
    private academicsService: AcademicsService
  ) {
    let navLinks = [
      { path: '/events', label: 'Events' },
      { path: '/history', label: 'History' }
    ];
    // Get section ID from route parameter
    this.sectionId = this.route.snapshot.params['id'];
    this.rosterRole = null;

    /** Initialize data from resolvers. */
    const data = this.route.snapshot.data as {
      section: OfficeHoursSectionDetails;
    };
    this.section = data.section;
  }

  /* On initialization, get section's events and checks user's roster role */
  ngOnInit(): void {
    this.getCurrentEvents();
    this.checkRosterRole();
  }

  /* Gets ongoing events for the section being viewed */
  getCurrentEvents() {
    this.officeHoursService
      .getCurrentEventsBySection(this.sectionId)
      .subscribe((events) => {
        this.currentEvents = events;
      });
  }

  /* Returns roster role of user accessing the page */
  checkRosterRole() {
    this.academicsService
      .getMembershipBySection(this.sectionId)
      .subscribe((section_member) => {
        this.rosterRole = section_member.member_role;
        return section_member;
      });
  }
}
