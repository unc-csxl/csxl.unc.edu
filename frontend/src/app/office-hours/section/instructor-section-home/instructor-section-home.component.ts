/**
 * The Instructor Section Home Component serves as a hub for Instructors and GTAs to view office hours events, see upcoming schedules,
 * check-in to event queues, see ticket history, view people in the office hours section, elevate rosterRoles, and see Data
 *
 * @author Madelyn Andrews, Bailey DeSouza, Meghan Sun, Sadie Amato
 * @copyright 2024
 * @license MIT
 */

import { Component, OnInit } from '@angular/core';
import {
  OfficeHoursEvent,
  OfficeHoursSectionDetails
} from '../../office-hours.models';
import { RosterRole } from 'src/app/academics/academics.models';
import {
  ActivatedRoute,
  ActivatedRouteSnapshot,
  ResolveFn,
  Router
} from '@angular/router';
import { OfficeHoursService } from '../../office-hours.service';
import { AcademicsService } from 'src/app/academics/academics.service';
import { sectionResolver } from '../../office-hours.resolver';

let titleResolver: ResolveFn<string> = (route: ActivatedRouteSnapshot) => {
  return route.parent!.data['section']?.title ?? 'Section Not Found';
};

@Component({
  selector: 'app-instructor-section-home',
  templateUrl: './instructor-section-home.component.html',
  styleUrls: ['./instructor-section-home.component.css']
})
export class InstructorSectionHomeComponent implements OnInit {
  public static Route = {
    path: 'instructor/:id',
    component: InstructorSectionHomeComponent,
    canActivate: [],
    resolve: { section: sectionResolver },
    children: [
      {
        path: '',
        title: titleResolver,
        component: InstructorSectionHomeComponent
      }
    ]
  };
  protected section: OfficeHoursSectionDetails;
  currentEvents: OfficeHoursEvent[] = [];
  sectionId: number;
  navLinks: any;
  rosterRole: RosterRole | null;

  constructor(
    private route: ActivatedRoute,
    private officeHoursService: OfficeHoursService,
    private academicsService: AcademicsService,
    private router: Router
  ) {
    // TODO: check if we need this?
    this.navLinks = [
      { path: '/events', label: 'Events' },
      { path: '/history', label: 'History' },
      { path: '/data', label: 'Data' },
      { path: '/people', label: 'People' }
    ];
    // Assign section ID to route parameter
    this.sectionId = this.route.snapshot.params['id'];
    this.rosterRole = null;
    // Check RosterRole
    this.checkRosterRole();
    /** Initialize data from resolvers. */
    const data = this.route.snapshot.data as {
      section: OfficeHoursSectionDetails;
    };
    this.section = data.section;
  }

  /* On initialization, get section's events and checks user's roster role */
  ngOnInit(): void {
    this.getCurrentEvents();
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

  /* Fuction that navigates to Event Editor component */
  navToCreateForm() {
    this.router.navigate([
      '/office-hours/instructor/',
      this.sectionId,
      'create-new-event'
    ]);
  }
}
