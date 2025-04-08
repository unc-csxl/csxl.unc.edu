/**
 * Tab navigation controller for courses.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import {
  Component,
  computed,
  OnInit,
  signal,
  WritableSignal
} from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MyCoursesService } from '../my-courses.service';
import {
  parseTermOverviewJsonList,
  TermOverviewJson
} from '../my-courses.model';
import { map } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { NagivationAdminGearService } from 'src/app/navigation/navigation-admin-gear.service';

@Component({
  selector: 'app-course',
  templateUrl: './course.component.html',
  styleUrls: ['./course.component.css']
})
export class CourseComponent {
  /** Links for the tab bar */
  isStaff: WritableSignal<boolean> = signal(false);
  isInstructor: WritableSignal<boolean> = signal(false);

  officeHoursLink = {
    label: 'Office Hours',
    path: `/course/${this.route.snapshot.params['course_site_id']}/office-hours`,
    icon: 'person_raised_hand'
  };

  statisticsLink = {
    label: 'Statistics',
    path: `/course/${this.route.snapshot.params['course_site_id']}/statistics`,
    icon: 'analytics'
  };

  rosterLink = {
    label: 'Roster',
    path: `/course/${this.route.snapshot.params['course_site_id']}/roster`,
    icon: 'groups'
  };

  settingsLink = {
    label: 'Settings',
    path: `/course/${this.route.snapshot.params['course_site_id']}/settings`,
    icon: 'settings'
  };

  links = computed(() => {
    if (this.isInstructor()) {
      return [
        this.officeHoursLink,
        this.statisticsLink,
        this.rosterLink,
        this.settingsLink
      ];
    } else if (this.isStaff()) {
      return [this.officeHoursLink, this.statisticsLink, this.rosterLink];
    } else {
      return [this.officeHoursLink, this.rosterLink];
    }
  });

  constructor(
    private route: ActivatedRoute,
    protected myCoursesService: MyCoursesService,
    protected http: HttpClient,
    protected gearService: NagivationAdminGearService
  ) {
    let id = +this.route.snapshot.params['course_site_id'];
    this.http
      .get<TermOverviewJson[]>('/api/my-courses')
      .pipe(map(parseTermOverviewJsonList))
      .subscribe((terms) => {
        const termRole = terms
          .flatMap((term) => term.sites)
          .find((site) => site.id === id)?.role;

        this.isStaff.set(
          termRole == 'UTA' || termRole == 'GTA' || termRole == 'Instructor'
        );
        this.isInstructor.set(termRole == 'Instructor');

        if (this.isInstructor()) {
          this.gearService.showAdminGear(
            'Course Settings',
            `/course/${id}/settings`
          );
        }
      });
  }
}
