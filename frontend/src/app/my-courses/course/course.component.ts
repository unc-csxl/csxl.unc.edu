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

@Component({
  selector: 'app-course',
  templateUrl: './course.component.html',
  styleUrls: ['./course.component.css']
})
export class CourseComponent {
  /** Links for the tab bar */
  isInstructor: WritableSignal<boolean> = signal(false);

  links = computed(() => {
    if (this.isInstructor()) {
      return [
        {
          label: 'Office Hours',
          path: `/course/${this.route.snapshot.params['course_site_id']}/office-hours`,
          icon: 'person_raised_hand'
        },
        {
          label: 'Roster',
          path: `/course/${this.route.snapshot.params['course_site_id']}/roster`,
          icon: 'groups'
        },
        {
          label: 'Settings',
          path: `/course/${this.route.snapshot.params['course_site_id']}/settings`,
          icon: 'settings'
        }
      ];
    } else {
      return [
        {
          label: 'Office Hours',
          path: `/course/${this.route.snapshot.params['course_site_id']}/office-hours`,
          icon: 'person_raised_hand'
        },
        {
          label: 'Roster',
          path: `/course/${this.route.snapshot.params['course_site_id']}/roster`,
          icon: 'groups'
        }
      ];
    }
  });

  constructor(
    private route: ActivatedRoute,
    protected myCoursesService: MyCoursesService,
    protected http: HttpClient
  ) {
    let id = +this.route.snapshot.params['course_site_id'];
    this.http
      .get<TermOverviewJson[]>('/api/my-courses')
      .pipe(map(parseTermOverviewJsonList))
      .subscribe((terms) => {
        let isInstructor =
          terms.flatMap((term) => term.sites).find((site) => site.id === id)
            ?.role == 'Instructor';

        this.isInstructor.set(isInstructor);
      });
  }
}
