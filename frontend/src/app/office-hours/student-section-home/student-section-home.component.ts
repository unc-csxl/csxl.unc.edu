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
  ResolveFn,
  RouteConfigLoadEnd
} from '@angular/router';
import {
  OfficeHoursEvent,
  OfficeHoursSectionDetails,
  TicketDetails
} from '../office-hours.models';
import { OfficeHoursService } from '../office-hours.service';
import { AcademicsService } from 'src/app/academics/academics.service';
import { RosterRole } from 'src/app/academics/academics.models';
import { sectionResolver } from '../office-hours.resolver';

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
    // TODO: replace this route + title to be un-hardcoded
    path: 'spring-2024/:id',
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

  protected section: OfficeHoursSectionDetails;
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

    /** Initialize data from resolvers. */
    const data = this.route.snapshot.data as {
      section: OfficeHoursSectionDetails;
    };
    this.section = data.section;
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
