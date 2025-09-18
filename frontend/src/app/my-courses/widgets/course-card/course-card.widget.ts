/**
 * The Course Card widget defines the UI card on the My Courses
 * page that shows enrolled courses.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { Component, Input } from '@angular/core';
import { CourseOverview, CourseSiteOverview } from '../../my-courses.model';

@Component({
    selector: 'course-card',
    templateUrl: './course-card.widget.html',
    styleUrls: ['./course-card.widget.scss'],
    standalone: false
})
export class CourseCardWidget {
  /** Term for the course */
  @Input() termId!: string;
  /** The course to show */
  @Input() course!: CourseSiteOverview;

  constructor() {}
}
