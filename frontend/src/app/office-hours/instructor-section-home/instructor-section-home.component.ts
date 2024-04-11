/**
 * The Instructor Section Home Component serves as a hub for Instructors and GTAs to view office hours events, see upcoming schedules,
 * check-in to event queues, see ticket history, and view people in the office hours section, elevate rosterRoles, and see Data
 *
 * @author Madelyn Andrews, Bailey DeSouza, Meghan Sun, Sadie Amato
 * @copyright 2024
 * @license MIT
 */

import { Component } from '@angular/core';
import { OfficeHoursEvent } from '../office-hours.models';
import { RosterRole } from 'src/app/academics/academics.models';
import { ActivatedRoute, Router } from '@angular/router';
import { OfficeHoursService } from '../office-hours.service';
import { AcademicsService } from 'src/app/academics/academics.service';

@Component({
  selector: 'app-instructor-section-home',
  templateUrl: './instructor-section-home.component.html',
  styleUrls: ['./instructor-section-home.component.css']
})
export class InstructorSectionHomeComponent {
  public static Route = {
    // TODO: replace spring-2024 in this route!
    path: 'instructor/spring-2024/:id',
    title: 'COMP 110: Intro to Programming',
    component: InstructorSectionHomeComponent,
    canActivate: []
  };
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
    this.navLinks = [
      { path: '/events', label: 'Events' },
      { path: '/history', label: 'History' },
      { path: '/data', label: 'Data' },
      { path: '/people', label: 'People' }
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

  navToCreateForm() {
    // TODO: Unhard code this later
    this.router.navigate([
      '/office-hours/instructor/spring-2024/',
      this.sectionId,
      'create-new-event'
    ]);
  }
}
