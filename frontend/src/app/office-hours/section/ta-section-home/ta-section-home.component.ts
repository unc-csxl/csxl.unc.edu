/**
 * The TA Section Home Component serves as a hub for TAs to view office hours events, see upcoming schedules,
 * check-in to event queues, see ticket history, and view people in the office hours section
 *
 * @author Madelyn Andrews, Bailey DeSouza, Meghan Sun, Sadie Amato
 * @copyright 2024
 * @license MIT
 */

import { Component, OnInit } from '@angular/core';
import {
  ActivatedRoute,
  ActivatedRouteSnapshot,
  ResolveFn,
  Router
} from '@angular/router';
import { OfficeHoursService } from '../../office-hours.service';
import {
  OfficeHoursEvent,
  OfficeHoursSectionDetails
} from '../../office-hours.models';
import { AcademicsService } from 'src/app/academics/academics.service';
import { RosterRole } from 'src/app/academics/academics.models';
import { ohSectionResolver } from '../../office-hours.resolver';

let titleResolver: ResolveFn<string> = (route: ActivatedRouteSnapshot) => {
  return route.parent!.data['section']?.title ?? 'Section Not Found';
};

@Component({
  selector: 'app-ta-section-home',
  templateUrl: './ta-section-home.component.html',
  styleUrls: ['./ta-section-home.component.css']
})
export class TaSectionHomeComponent implements OnInit {
  public static Route = {
    path: 'ta/:id',
    component: TaSectionHomeComponent,
    canActivate: [],
    resolve: { section: ohSectionResolver },
    children: [
      {
        path: '',
        title: titleResolver,
        component: TaSectionHomeComponent
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
    this.navLinks = [
      { path: '/events', label: 'Events' },
      { path: '/history', label: 'History' },
      { path: '/people', label: 'People' }
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

  /* Fuction that navigates to Event Editor component */
  navToCreateForm() {
    // TODO: Unhard code this later
    this.router.navigate([
      '/office-hours/ta/',
      this.sectionId,
      'create-new-event'
    ]);
  }
}
